# 🎬 วิธี Demo บนเครื่องใหม่ (เช่น เครื่องอาจารย์)

**คู่มือสำหรับการ Demo ระบบบนเครื่องอื่น**

---

## 🎯 **ไฟล์ที่ใช้สำหรับ Demo**

### **✅ `live_demo_complete.ipynb`** ⭐ (แนะนำ!)

**Notebook ที่รวมทุกอย่างไว้แล้ว - ไม่ต้อง setup ล่วงหน้า!**

---

## 📦 **สิ่งที่ต้องเตรียมบนเครื่องใหม่**

### **1. Software ที่ต้องมี:**
- ✅ Python 3.8+ ติดตั้งแล้ว
- ✅ MySQL Server ทำงานอยู่
- ✅ Jupyter Notebook: `pip install jupyter mysql-connector-python`

### **2. Database ที่ต้องมี:**
- ✅ Database `portfolio_backtesting` พร้อมข้อมูล
- ✅ รันไฟล์ `database/complete_setup.sql` ใน MySQL Workbench ก่อน
- ✅ Import ข้อมูลจาก `data/etf_price_history.csv`

### **3. ไฟล์ที่ต้องคัดลอกไป:**
```
desktop-tutorial/
├── live_demo_complete.ipynb    ⭐ ไฟล์หลัก
├── database/
│   └── stored_procedures.sql    ⭐ จำเป็น (Notebook จะอ่านไฟล์นี้)
└── (ไฟล์อื่นๆ ตามต้องการ)
```

---

## 🚀 **วิธีใช้งานแบบละเอียด**

### **Step 1: คัดลอกโปรเจกต์ไปยังเครื่องใหม่**

**ทางเลือกที่ 1: ใช้ USB Drive**
1. คัดลอกทั้งโฟลเดอร์ `desktop-tutorial` ลง USB
2. เสียบ USB ที่เครื่องใหม่
3. คัดลอกโฟลเดอร์ไปยังเครื่องใหม่ (เช่น `Documents/`)

**ทางเลือกที่ 2: ใช้ Git Clone**
```bash
git clone https://github.com/krittanut789656/desktop-tutorial.git
cd desktop-tutorial
```

---

### **Step 2: เปิด Jupyter Notebook**

1. เปิด **Terminal** (Mac/Linux) หรือ **Command Prompt** (Windows)

2. ไปที่โฟลเดอร์โปรเจกต์:
   ```bash
   cd desktop-tutorial
   ```

3. เปิด Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

4. Browser จะเปิดขึ้นมาอัตโนมัติ

---

### **Step 3: เปิดไฟล์ `live_demo_complete.ipynb`**

คลิกที่ **`live_demo_complete.ipynb`** ใน Jupyter

---

### **Step 4: แก้ไข MySQL Password** ⚠️ **สำคัญ!**

1. เลื่อนลงไปหา **Cell 1** (Cell แรก)

2. หาบรรทัดนี้:
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'krittanut123456',  # ⬅️ แก้ไขตรงนี้!
       'database': 'portfolio_backtesting'
   }
   ```

3. แก้ไข **`'password'`** ให้ตรงกับ MySQL password ของเครื่องนั้น:
   ```python
   'password': 'mysql_password_of_this_machine',
   ```

4. บันทึกการแก้ไข: **File** → **Save** (หรือกด Ctrl+S)

---

### **Step 5: รัน Cell 1 (Setup + Install SQL Procedures)**

1. คลิกที่ **Cell 1** (Cell แรก)

2. กด **Shift+Enter** เพื่อรัน

3. **จะเกิดอะไรขึ้น:**
   - เชื่อมต่อ MySQL
   - อ่านไฟล์ `database/stored_procedures.sql`
   - ติดตั้ง 8 Stored Procedures อัตโนมัติ
   - ติดตั้ง 3 Views อัตโนมัติ
   - แสดงสถิติของ Database

4. **ผลลัพธ์ที่ควรเห็น:**
   ```
   ============================================================
   🚀 Portfolio Backtesting System - Complete Setup
   ============================================================

   🔌 กำลังเชื่อมต่อ MySQL...
   ✅ เชื่อมต่อ MySQL สำเร็จ!
   📊 Database: portfolio_backtesting

   📖 กำลังอ่านไฟล์: database/stored_procedures.sql
   ✅ อ่านไฟล์สำเร็จ

   ⚙️  กำลังติดตั้ง SQL Stored Procedures & Views...
   ------------------------------------------------------------
     ✅ สร้าง View: vw_weekly_returns
     ✅ สร้าง View: vw_etf_performance
     ✅ สร้าง View: vw_portfolio_summary
     ✅ สร้าง Procedure: sp_calculate_portfolio_return
     ✅ สร้าง Procedure: sp_calculate_sharpe_ratio
     ✅ สร้าง Procedure: sp_calculate_max_drawdown
     ✅ สร้าง Procedure: sp_calculate_volatility
     ✅ สร้าง Procedure: sp_get_etf_correlation
     ✅ สร้าง Procedure: sp_get_top_performers
     ✅ สร้าง Procedure: sp_compare_portfolios
     ✅ สร้าง Procedure: sp_get_portfolio_weights

   ============================================================
   📊 สรุปผลการติดตั้ง
   ============================================================
   ✅ สำเร็จ: 14 statements
   ❌ ล้มเหลว: 0 statements

   📋 Views ที่ติดตั้งแล้ว:
      ✓ vw_weekly_returns
      ✓ vw_etf_performance
      ✓ vw_portfolio_summary

   📋 Stored Procedures ที่ติดตั้งแล้ว:
      ✓ sp_calculate_portfolio_return
      ✓ sp_calculate_sharpe_ratio
      ✓ sp_calculate_max_drawdown
      ✓ sp_calculate_volatility
      ✓ sp_get_etf_correlation
      ✓ sp_get_top_performers
      ✓ sp_compare_portfolios
      ✓ sp_get_portfolio_weights

   ============================================================
   📈 Database Statistics
   ============================================================
      - ETFs: 50
      - Portfolios: 35
      - Price History Records: 208,700

   ============================================================
   ✅ Setup เสร็จสมบูรณ์!
   ============================================================

   🎉 พร้อมใช้งาน Live Demo!
   💡 กรุณารัน Cell ถัดไป (Main Loop) โดยกด Shift+Enter ครั้งเดียว
   ============================================================
   ```

5. **ถ้าเห็นข้อความนี้ = สำเร็จ! ✅**

---

### **Step 6: รัน Cell 2 (Live Demo Menu)** ⭐

1. คลิกที่ **Cell 2** (Cell ที่สอง)

2. กด **Shift+Enter** **ครั้งเดียว**

3. **จะเกิดอะไรขึ้น:**
   - แสดง Interactive Menu
   - รอรับ Input จากคุณ

4. **จะเห็น Menu:**
   ```
   ============================================================
   🎬 Live Demo Started!
   ============================================================
   💡 กรุณาเลือก Option 1-5 เพื่อ Demo Analytics Features
   💡 เลือก 0 เพื่อออกจากโปรแกรม

   ============================================================
   📈 Data Analytics Menu (SQL-based)
   ============================================================

   1. 🏆 Top Performers - Top 5 ETFs ที่ดีที่สุด
   2. ⚖️  Portfolio Comparison - เปรียบเทียบ Portfolios ทั้งหมด
   3. 🔗 ETF Correlation - วิเคราะห์ความสัมพันธ์ระหว่าง ETFs
   4. 📊 Sharpe Ratio Calculator - คำนวณ Sharpe Ratio
   5. 📈 Top 10 ETFs Performance - ดูผลตอบแทนจาก SQL View
   0. 🚪 Exit - ออกจากโปรแกรม

   ============================================================

   เลือก Option (0-5): _
   ```

---

### **Step 7: Demo Analytics Features** 🎬

**พิมพ์ตัวเลข 1-5 และกด Enter:**

#### **ตัวอย่าง: เลือก 1 → Top Performers**

```
เลือก Option (0-5): 1

🏆 Top 5 ETFs ที่มี Sharpe Ratio สูงสุด
========================================================================
📌 ใช้ SQL Stored Procedure: sp_get_top_performers
========================================================================

Rank   Ticker     ETF Name                       Return       Volatility   Sharpe
--------------------------------------------------------------------------------
#1     QQQ        Nasdaq 100 ETF                 18.50%       15.20%       1.2200
#2     VTI        Total Stock Market ETF         14.80%       14.50%       1.0200
#3     SPY        S&P 500 ETF                    14.20%       14.80%       0.9600
#4     IWM        Russell 2000 ETF               12.50%       18.50%       0.6750
#5     AGG        US Aggregate Bond ETF           3.20%        3.50%       0.9140

💡 Actionable Insights:
   - 🎯 QQQ มี Sharpe Ratio สูงสุด (1.2200)
   - 📊 ผลตอบแทนต่อปี: 18.50%
   - 💼 แนะนำสำหรับนักลงทุนที่ต้องการผลตอบแทนดีเมื่อปรับความเสี่ยง
   - ✅ Sharpe Ratio > 1.0 = ผลตอบแทนคุ้มค่ากับความเสี่ยง

⏎ กด Enter เพื่อกลับสู่ Menu...
```

กด **Enter** → กลับสู่ Menu

#### **เลือก Option อื่นต่อ:**

```
เลือก Option (0-5): 3

🔗 ETF Correlation Analysis
========================================================================
📌 ใช้ SQL Stored Procedure: sp_get_etf_correlation
========================================================================

ป้อน Ticker 1 (เช่น SPY): SPY
ป้อน Ticker 2 (เช่น QQQ): QQQ

📊 SPY vs QQQ
--------------------------------------------------------------------------------
Correlation: 0.8500

ความสัมพันธ์: แข็งแกร่งมาก (Highly Correlated)

💡 Actionable Insights:
   - ⚠️  ไม่แนะนำให้ถือทั้ง 2 ETFs ในพอร์ตเดียวกัน
   - เหตุผล: มีความเสี่ยงคล้ายกันมาก ไม่ได้ช่วย Diversify

⏎ กด Enter เพื่อกลับสู่ Menu...
```

#### **ทำต่อไปเรื่อยๆ...**

เลือก Option 1-5 ไปเรื่อยๆ จนกว่าจะต้องการออก

#### **เลือก 0 → Exit:**

```
เลือก Option (0-5): 0

========================================================================
🚪 ขอบคุณที่ใช้งาน Portfolio Backtesting System!
========================================================================

✅ สรุปการ Demo:
   - ใช้ SQL Stored Procedures ทั้งหมด (ตามโจทย์ข้อ 3)
   - มี Actionable Insights ในทุก Feature (ตามโจทย์ข้อ 5f)
   - ข้อมูลจริงจาก Yahoo Finance (ตามโจทย์ข้อ 4)

💼 ระบบหลักอยู่ที่: main.py (Integrated System)

👋 Goodbye!

✅ Database connection closed
```

---

## ✅ **สรุป Flow การ Demo**

```
1. เปิด Jupyter Notebook
   ↓
2. เปิดไฟล์ live_demo_complete.ipynb
   ↓
3. แก้ไข MySQL Password ใน Cell 1
   ↓
4. รัน Cell 1 (Setup) → Shift+Enter
   ↓
5. รัน Cell 2 (Demo) → Shift+Enter ครั้งเดียว
   ↓
6. เลือก 1-5 ไปเรื่อยๆ
   ↓
7. เลือก 0 เพื่อออก
```

---

## 🚨 **Troubleshooting**

### **❌ Error: Connection Error (2003)**
```
❌ Connection Error: 2003 (HY000): Can't connect to MySQL server
```

**วิธีแก้:**
1. ตรวจสอบว่า MySQL Server ทำงานอยู่
2. เปิด MySQL Server:
   - **Windows**: `net start MySQL80`
   - **Mac**: `brew services start mysql`

---

### **❌ Error: Access Denied (1045)**
```
❌ Connection Error: 1045 (28000): Access denied for user 'root'
```

**วิธีแก้:**
1. แก้ไข password ใน Cell 1 ให้ถูกต้อง
2. รัน Cell 1 ใหม่

---

### **❌ Error: Unknown Database**
```
❌ Connection Error: 1049 (42000): Unknown database 'portfolio_backtesting'
```

**วิธีแก้:**
1. เปิด MySQL Workbench
2. รันไฟล์ `database/complete_setup.sql` เพื่อสร้าง database
3. Import ข้อมูลจาก `data/etf_price_history.csv`
4. รัน Cell 1 ใหม่

---

### **❌ Error: File Not Found**
```
❌ ไม่พบไฟล์: database/stored_procedures.sql
```

**วิธีแก้:**
1. ตรวจสอบว่าโฟลเดอร์ `database/` มีอยู่
2. ตรวจสอบว่าไฟล์ `stored_procedures.sql` อยู่ในโฟลเดอร์ `database/`
3. ตรวจสอบว่า Jupyter Notebook รันอยู่ที่โฟลเดอร์ `desktop-tutorial`

---

## 💡 **Tips สำหรับการ Demo**

1. **เตรียม Database ล่วงหน้า** - รัน `complete_setup.sql` และ import ข้อมูลก่อน
2. **ทดสอบก่อน Demo จริง** - รันทดสอบบนเครื่องตัวเองก่อน
3. **แก้ไข Password ให้ถูกต้อง** - ต้องรู้ MySQL password ของเครื่องที่จะ Demo
4. **เตรียม USB Backup** - กันกรณี Internet/Git ไม่ได้

---

## 📊 **เปรียบเทียบ Notebooks**

| Feature | `live_demo_complete.ipynb` ⭐ | `live_demo_analytics.ipynb` |
|---------|------------------------------|----------------------------|
| **ติดตั้ง SQL Procedures** | ✅ อัตโนมัติใน Cell 1 | ❌ ต้องรัน setup_procedures.py ก่อน |
| **ใช้งานบนเครื่องใหม่** | ✅ ง่ายมาก (แค่แก้ password) | ⚠️  ต้อง setup ล่วงหน้า |
| **จำนวน Cells** | 2 Cells | 2 Cells |
| **Interactive Menu** | ✅ มี | ✅ มี |
| **เหมาะสำหรับ** | **Demo บนเครื่องอื่น** | Demo บนเครื่องที่ setup แล้ว |

**สรุป:** ใช้ **`live_demo_complete.ipynb`** สำหรับ Demo บนเครื่องใหม่! ⭐

---

## 📁 **Checklist สำหรับ Demo**

**ก่อน Demo:**
- [ ] คัดลอกโฟลเดอร์ `desktop-tutorial` ไปยังเครื่องใหม่
- [ ] รัน `database/complete_setup.sql` ใน MySQL Workbench
- [ ] Import ข้อมูลจาก `data/etf_price_history.csv`
- [ ] ติดตั้ง: `pip install jupyter mysql-connector-python`
- [ ] ทดสอบรัน Notebook ครั้งหนึ่ง

**ขณะ Demo:**
- [ ] เปิด Jupyter: `jupyter notebook`
- [ ] เปิดไฟล์: `live_demo_complete.ipynb`
- [ ] แก้ไข password ใน Cell 1
- [ ] รัน Cell 1 → Shift+Enter
- [ ] รัน Cell 2 → Shift+Enter
- [ ] Demo Option 1-5 ตามต้องการ

---

## 🎉 **พร้อม Demo!**

ตอนนี้คุณพร้อมที่จะ Demo ระบบบนเครื่องใหม่แล้ว!

**Good luck! 🚀**
