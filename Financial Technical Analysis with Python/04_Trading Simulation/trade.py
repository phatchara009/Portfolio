## Assumptions
## 1. Budget for each buy = 100,000.00 Baht งบประมาณเรามี 1 แสนบาท
## 2. Buy at the open (ATO) of the next day after buy signals appear. # หลังจากมีสัญญาณจะซื้อที่ราคาเปิดของวันถัดไป
## 3. Commission and other fees for each buy or sell = 0.17%

import numpy as np
from math import floor

def tradeSim(df,signal,filename): # ตั้ง function tradeSim มี paramiter 3 ตัว ส่งมาที่ tradeSim เพื่อจำลองการซื้อขาย
    Open = df['Open']
    rows = len(Open)
    num = 0
    total = 0
    Cost = 0
    # ทุกๆค่าต่อไปนี้เริ่มต้น ตั้งเป็นค่าว่างทุกๆแถว
    numBuy = [np.nan]*rows # คือปริมาณการซื้อ ว่าเราจะซื้อกี่หุ้น เริ่มต้นให้ทุกๆค่าแต่ละแถวเป็น nan
    cost = [np.nan]*rows # ต้นทุนที่ใช้ในการซื้อ ให้เป็นค่าว่างทุกแถว
    numSell = [np.nan]*rows # จำนวนหลักทรัพย์หรือจำนวนหุ้นที่มีการขาย
    income = [np.nan]*rows # รายรับ
    profit = [np.nan]*rows # กำไรในแต่ละรอบการซื้อขาย
##  Buy & Sell Simulation เริ่มจำลองระบบการซื้อขาย   
    for i in range(1,rows-1): # เริ่มวันที่สองเพราะวันแรกจะไม่เกิดสัญญาณ
        if (signal[i-1] == -1) and (signal[i] == 1): # นี่คือเกิดสัญญาณซื้อ
            # floor(คำนวณปริมาณหุ้นที่จะซื้อ เอาเงินที่เรามี[100000] / (ราคาเปิดวันรุ่งขึ้น[i+1] * ค่าคอมมิชชั่น [1.0017]))/100)*100
            # หลังจาก หาร 100แล้วใช้คำสั่ง floor ที่ import เข้ามาปัดเศษทิ้งเพราะหุ้นซื้อต้องเป็นเลขลงตัว
            # จะซื้อในวันถัดไปที่มีสัญญาณซื้อ
            numBuy[i+1] = floor((100000/(Open[i+1]*1.0017))/100)*100 # คำนวณปริมาณการซื้อจากเงินต้นของเรา โดยเกิดวันที่ i+1 ซื้อเป็น boardlot ที่หาร 100ลงตัว
            num = numBuy[i+1] # เป็นตัวแปรที่เก็บค่าจำนวนหลักทรัพย์ที่มีการซื้อล่าสุด เราก็รับค่าจาก numBuy เพื่อให้รู้ว่าหุ้นที่เราซื้อมีอยู่เท่าไหร่ 
            cost[i+1] = -numBuy[i+1]*Open[i+1]*1.0017 # ต้นทุน = -1 * จำนวนหุ้น * ราคาเปิด * 1.0017คือ ค่าคอมมิชชั่น มี -1 เพราะเราเสียเงินไป
            Cost = cost[i+1]
        elif (signal[i-1] == 1) and (signal[i] == -1): # นี่คือเกิดสัญญาณขาย เกิดเมื่อสัญญาณวันก่อน(i-1)เป็น 1 แล้วเปลี่ยนเป็น -1 ในวันปัจจุบัน(i)
            numSell[i+1] = -num # เวลาขายเราเสียห0ลักทรัพย์ออกจากพอร์ตไป จำนวนจึงเป็นค่าติดลบ ก็คือ -num
            # numSell ค่าเป็นติดลบ เอา - มาคูณข้างหน้าให้เป็น + เพื่อให้ income เป็นค่า +
            income[i+1] = -numSell[i+1]*Open[i+1]*0.9983 # 0.9983 อัตราส่วนหลังจากเสียค่าธรรมเนียมแล้ว
            profit[i+1] = income[i+1]+Cost; # เอาincome หัก cost แต่ที่เห็นเป็นบวกเพราะ cost มีค่าเป็นลบในตอนแรก ถ้า profit เป็น + คือกำไร or ค่าเป็น - คือขาดทุน
            total = total + profit[i+1] # total คือผลกำไรขาดทุนรวมของการซื้อขายทุุกครั้ง
    filename = 'tradesim/' + filename # หลังจากที่คำนวณทุกอย่างแล้ว
    df['Signal'] = signal
    df['NumBuy'] = numBuy
    df['Cost'] = cost
    df['NumSell'] = numSell
    df['Income'] = income
    df['Profit'] = profit
    df.to_csv(filename)
    total = total/100000/3*100 # คำนวณผลตอบแทน หาร 3 คือเนื่องจากมีข้อมูลของปี 2013 ถึง 2015 ซึ่งมี 3 ปี แต่เราต้องการกำไรแต่ละปีเฉลี่ยเป็น % จึงหาร 3
    return total # ส่งผลตอบแทนเฉลี่ยกลับไป ณ จุดที่เรียกใช้เพิ้อแสดงผลอัตราตอบแทนแต่ละปี
