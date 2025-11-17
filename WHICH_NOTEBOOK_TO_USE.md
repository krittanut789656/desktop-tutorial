# 📔 คู่มือเลือกใช้ Jupyter Notebook

มี Notebooks หลายไฟล์ในโปรเจคนี้ - ใช้ไฟล์ไหนดี?

---

## 🎯 แนะนำ: ใช้ไฟล์นี้!

### ✅ **`Simple_Run_All.ipynb`** - แนะนำสำหรับทุกคน!

**ใช้เมื่อไร:**
- ดูข้อมูล Portfolios, ETFs, Prices
- วิเคราะห์ข้อมูลด้วย Pandas
- สร้าง charts พื้นฐาน
- **ไม่มีปัญหา import error เลย!**

**ข้อดี:**
- ✅ Run cell ไหนก่อนก็ได้
- ✅ Functions ฝังอยู่ในตัวแล้ว
- ✅ ไม่ต้อง import external files
- ✅ ใช้งานง่ายที่สุด

**ข้อจำกัด:**
- ไม่มี Analytics 3 Insights
- ไม่มี Backtesting แบบเต็ม
- แค่ดูข้อมูลและวิเคราะห์พื้นฐาน

**เริ่มต้น:**
```bash
cd desktop-tutorial
jupyter notebook Simple_Run_All.ipynb
```

---

## 📊 สำหรับงาน Advanced

### **`jupyter_interface.py` + Custom Notebook**

**ใช้เมื่อไร:**
- ต้องการ Analytics 3 Insights
- ต้องการ Backtesting เต็มรูปแบบ
- ต้องการ flexibility สูง

**วิธีใช้:**
```python
# สร้าง notebook ใหม่
import sys
sys.path.insert(0, '.')

import jupyter_interface as etf

# ใช้ functions
etf.show_portfolios(DB_CONFIG)
etf.run_risk_analysis(portfolio_ids=[1,2,3], db_config=DB_CONFIG)
etf.run_backtest(portfolio_id=1, strategy='buy_hold', db_config=DB_CONFIG)
```

**ข้อควรระวัง:**
- ต้องรัน import ก่อน
- ถ้ามี import error ให้ restart kernel

---

## 🔧 สำหรับ Setup ครั้งแรก

### **`Complete_Setup_and_Run.ipynb`**

**ใช้เมื่อไร:**
- ครั้งแรกที่ใช้งาน
- ต้องการ setup database
- ต้องการ download ข้อมูล ETFs

**ทำอะไร:**
- สร้าง database และ tables
- เพิ่มข้อมูล ETFs ตัวอย่าง 40 ตัว
- Download ข้อมูลราคาย้อนหลัง 2009-2025
- สร้าง portfolios ตัวอย่าง

**เวลาที่ใช้:**
- 15-20 นาที (ส่วนใหญ่เป็น download ราคา)

**หมายเหตุ:**
- ใช้แค่ครั้งเดียวตอน setup
- หลังจากนั้นใช้ `Simple_Run_All.ipynb` แทน

---

## 📋 สรุป - ควรใช้อะไร?

| สถานการณ์ | Notebook ที่แนะนำ | เวลา |
|-----------|------------------|------|
| **ครั้งแรก - ยังไม่มีข้อมูล** | Complete_Setup_and_Run.ipynb | 15-20 นาที |
| **ดูข้อมูล + วิเคราะห์พื้นฐาน** | Simple_Run_All.ipynb | ทันที |
| **Analytics + Backtesting เต็ม** | jupyter_interface.py + Custom | ตามต้องการ |

---

## 🚀 Quick Start Guide

### สำหรับมือใหม่:

**Day 1:**
```bash
# 1. Setup database (ครั้งเดียว)
jupyter notebook Complete_Setup_and_Run.ipynb
# → Run All แล้วรอ 15-20 นาที
```

**Day 2 onwards:**
```bash
# 2. ใช้งานปกติ
jupyter notebook Simple_Run_All.ipynb
# → Run cells ที่ต้องการ
```

---

## ❓ FAQ

**Q: ทำไมมีหลาย notebooks?**
A: แต่ละไฟล์ทำงานต่างกัน:
- Complete_Setup_and_Run = setup ครั้งแรก
- Simple_Run_All = ใช้งานประจำวัน (ง่ายที่สุด)
- ETF_Backtesting_Notebook = advanced (ต้อง import)

**Q: ไฟล์ไหนง่ายที่สุด?**
A: `Simple_Run_All.ipynb` - ใช้ได้เลย ไม่มีปัญหา import

**Q: จะใช้ Analytics ยังไง?**
A: ต้องใช้ `jupyter_interface.py` หรือเขียน code เอง

**Q: Error: No module named 'etf' หรือ 'crud_operations'**
A: ใช้ `Simple_Run_All.ipynb` แทน - ไม่มีปัญหานี้!

**Q: ข้อมูลหายไปไหน?**
A: อยู่ใน MySQL database ชื่อ `etf_backtesting`

---

## 💡 Tips

1. **เริ่มต้นด้วย Simple_Run_All.ipynb เสมอ**
2. ถ้าต้องการ advanced features ค่อยไปที่ jupyter_interface.py
3. Run Complete_Setup_and_Run.ipynb แค่ครั้งเดียวตอน setup
4. ถ้ามีปัญหา import error → ใช้ Simple_Run_All.ipynb แทน

---

**Happy Analyzing! 📊**
