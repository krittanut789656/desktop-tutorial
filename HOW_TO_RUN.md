# 🚀 วิธีรันระบบ Portfolio Backtesting System

**คู่มือฉบับสมบูรณ์สำหรับการใช้งาน**

---

## 📋 สารบัญ

1. [เตรียมความพร้อม](#1-เตรียมความพร้อม)
2. [ติดตั้ง SQL Stored Procedures](#2-ติดตั้ง-sql-stored-procedures)
3. [วิธีใช้ Jupyter Notebook](#3-วิธีใช้-jupyter-notebook)
4. [วิธีรัน main.py](#4-วิธีรัน-mainpy)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. เตรียมความพร้อม

### ✅ สิ่งที่ต้องมี:

1. **Python 3.8+** ติดตั้งแล้ว
2. **MySQL Server** ทำงานอยู่
3. **Python Libraries**:
   ```bash
   pip install mysql-connector-python pandas jupyter
   ```

### ✅ ตรวจสอบว่า MySQL ทำงานหรือไม่:

**Windows:**
```bash
# ตรวจสอบ
net start | findstr MySQL

# เปิด MySQL (ถ้าปิดอยู่)
net start MySQL80
```

**Mac:**
```bash
# ตรวจสอบ
brew services list | grep mysql

# เปิด MySQL (ถ้าปิดอยู่)
brew services start mysql
```

**Linux:**
```bash
# ตรวจสอบ
sudo service mysql status

# เปิด MySQL (ถ้าปิดอยู่)
sudo service mysql start
```

---

## 2. ติดตั้ง SQL Stored Procedures

### **วิธีที่ 1: ใช้ Python Script** (แนะนำ ⭐)

เปิด Terminal/Command Prompt และรัน:

```bash
cd desktop-tutorial
python3 setup_procedures.py
```

**ผลลัพธ์ที่คาดหวัง:**

```
============================================================
🚀 ติดตั้ง SQL Stored Procedures & Views
============================================================

🔌 กำลังเชื่อมต่อ MySQL...
✅ เชื่อมต่อสำเร็จ!

📖 กำลังอ่านไฟล์: database/stored_procedures.sql
⚙️  กำลังประมวลผล SQL statements...

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
📊 สรุปผลการติดตั้ง SQL Stored Procedures & Views
============================================================
✅ สำเร็จ: 14 statements
❌ ล้มเหลว: 0 statements

📋 Views ที่สร้างแล้ว:
  ✓ vw_weekly_returns
  ✓ vw_etf_performance
  ✓ vw_portfolio_summary

📋 Stored Procedures ที่สร้างแล้ว:
  ✓ sp_calculate_portfolio_return
  ✓ sp_calculate_sharpe_ratio
  ✓ sp_calculate_max_drawdown
  ✓ sp_calculate_volatility
  ✓ sp_get_etf_correlation
  ✓ sp_get_top_performers
  ✓ sp_compare_portfolios
  ✓ sp_get_portfolio_weights

✅ ติดตั้งเสร็จสมบูรณ์!

🎉 พร้อมใช้งาน! ตอนนี้สามารถรัน python main.py ได้แล้ว
```

---

### **วิธีที่ 2: ใช้ MySQL Workbench**

หากวิธีที่ 1 ไม่ได้ผล:

1. เปิด **MySQL Workbench**
2. Connect to `portfolio_backtesting` database
3. เปิดไฟล์: `File` → `Open SQL Script` → เลือก `database/stored_procedures.sql`
4. กด **Execute** (⚡ icon หรือ Ctrl+Shift+Enter)
5. รอ 3-5 วินาที จนเห็น "8 procedures created successfully"

---

## 3. วิธีใช้ Jupyter Notebook

### **Step 1: ติดตั้ง Jupyter** (ถ้ายังไม่มี)

```bash
pip install jupyter
```

### **Step 2: เปิด Jupyter Notebook**

เปิด Terminal/Command Prompt:

```bash
cd desktop-tutorial
jupyter notebook
```

**จะเกิดอะไรขึ้น:**
1. Browser จะเปิดขึ้นมาอัตโนมัติ (http://localhost:8888)
2. จะเห็นหน้า Jupyter ที่แสดงไฟล์ในโฟลเดอร์ `desktop-tutorial`

---

### **Step 3: เลือก Notebook ที่ต้องการ**

คุณจะเห็น 2 Notebooks:

#### **A. `live_demo_analytics.ipynb`** ⭐ (แนะนำสำหรับ Live Demo)

**เหมาะสำหรับ:**
- Live Demo ต่อหน้าอาจารย์
- การนำเสนอแบบ Interactive
- ตรงตามโจทย์ที่อาจารย์ต้องการ

**วิธีใช้:**

1. **คลิกเปิด** `live_demo_analytics.ipynb`

2. **รัน Cell แรก (Setup)**:
   - คลิกที่ Cell แรก
   - กด **Shift+Enter**
   - จะเชื่อมต่อ Database และแสดง Statistics

3. **รัน Cell ที่สอง (Main Loop)** ⭐:
   - คลิกที่ Cell ที่สอง
   - กด **Shift+Enter** **ครั้งเดียว**
   - จะแสดง Menu:

   ```
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

4. **เลือก Option**:
   - พิมพ์ตัวเลข 1-5 เพื่อ Demo Analytics Features
   - ระบบจะวนลูปไปเรื่อยๆ
   - พิมพ์ 0 เพื่อออก

5. **ตัวอย่างการ Demo:**

   ```
   เลือก Option (0-5): 1

   🏆 Top 5 ETFs ที่มี Sharpe Ratio สูงสุด
   ========================================================================

   Rank   Ticker     ETF Name                       Return       Volatility   Sharpe
   --------------------------------------------------------------------------------
   #1     QQQ        Nasdaq 100 ETF                  18.50%       15.20%       1.2200
   #2     VTI        Total Stock Market ETF          14.80%       14.50%       1.0200
   ...

   💡 Actionable Insights:
      - 🎯 QQQ มี Sharpe Ratio สูงสุด (1.2200)
      - 📊 ผลตอบแทนต่อปี: 18.50%
      - 💼 แนะนำสำหรับนักลงทุนที่ต้องการผลตอบแทนดีเมื่อปรับความเสี่ยง

   ⏎ กด Enter เพื่อกลับสู่ Menu...
   ```

   กด Enter → กลับสู่ Menu → เลือก Option อื่นต่อได้เรื่อยๆ

---

#### **B. `demo_analytics.ipynb`** (Demo แบบรันทีละ Cell)

**เหมาะสำหรับ:**
- Presentation แบบเตรียมไว้ล่วงหน้า
- อธิบายทีละขั้นตอน

**วิธีใช้:**

1. **คลิกเปิด** `demo_analytics.ipynb`

2. **รัน Cell ทีละ Cell**:
   - กด **Shift+Enter** เพื่อรัน Cell ปัจจุบันและไปต่อ Cell ถัดไป
   - หรือกด **Cell** → **Run All** เพื่อรันทั้งหมดพร้อมกัน

3. **ดูผลลัพธ์**:
   - แต่ละ Cell จะแสดง Analytics Features ต่างๆ
   - มี DataFrame สวยงาม
   - มี Markdown อธิบายละเอียด

---

### **📌 Keyboard Shortcuts สำหรับ Jupyter Notebook:**

| Shortcut | คำอธิบาย |
|----------|---------|
| **Shift+Enter** | รัน Cell ปัจจุบันและไปต่อ Cell ถัดไป |
| **Ctrl+Enter** | รัน Cell ปัจจุบันโดยไม่ย้าย |
| **Alt+Enter** | รัน Cell ปัจจุบันและสร้าง Cell ใหม่ด้านล่าง |
| **A** (Command Mode) | เพิ่ม Cell ด้านบน |
| **B** (Command Mode) | เพิ่ม Cell ด้านล่าง |
| **DD** (Command Mode) | ลบ Cell |
| **Esc** | เข้า Command Mode |
| **Enter** | เข้า Edit Mode |

---

### **Step 4: หยุด Jupyter Notebook**

เมื่อใช้งานเสร็จแล้ว:

1. ปิด Browser tabs
2. กลับไปที่ Terminal
3. กด **Ctrl+C** สองครั้ง
4. พิมพ์ `y` และกด Enter เพื่อ Shutdown

---

## 4. วิธีรัน main.py

### **ระบบหลักแบบ Integrated System** (ตามโจทย์อาจารย์)

เปิด Terminal/Command Prompt:

```bash
cd desktop-tutorial
python3 main.py
```

**จะแสดง Menu:**

```
============================================================
   📊 Portfolio Backtesting System - DADS 4002
============================================================

🎯 เมนูหลัก:

1. 📊 จัดการข้อมูล ETF (CRUD)
2. 📂 จัดการ Benchmark Portfolios (CRUD)
3. 📈 Data Analytics (SQL-based)
4. ⚙️  System Utilities
5. ℹ️  About System
0. 🚪 ออกจากระบบ

============================================================
เลือกเมนู (0-5): _
```

**Features ทั้งหมด:**
- ✅ ETF CRUD Operations
- ✅ Portfolio CRUD Operations
- ✅ Analytics (5 Features ด้วย SQL Stored Procedures)
- ✅ System Utilities (Logs, Backup, Statistics)
- ✅ Text File Operations

---

## 5. Troubleshooting

### ❌ **ปัญหา: MySQL Connection Error (2003)**

**Error:**
```
❌ MySQL Error: 2003 (HY000): Can't connect to MySQL server on 'localhost:3306' (111)
```

**วิธีแก้:**

1. **ตรวจสอบว่า MySQL Server ทำงานหรือไม่:**
   ```bash
   # Windows
   net start MySQL80

   # Mac
   brew services start mysql

   # Linux
   sudo service mysql start
   ```

2. **ตรวจสอบ Port:**
   - MySQL ควรทำงานที่ Port 3306
   - เปิด MySQL Workbench → Server → Server Status → ดู Port

3. **ตรวจสอบ Password:**
   - เปิดไฟล์ `main.py` หรือ `setup_procedures.py`
   - แก้ไข `MYSQL_CONFIG`:
     ```python
     MYSQL_CONFIG = {
         'host': 'localhost',
         'user': 'root',
         'password': 'YOUR_PASSWORD_HERE',  # แก้ไขตรงนี้
         'database': 'portfolio_backtesting'
     }
     ```

---

### ❌ **ปัญหา: ModuleNotFoundError: No module named 'mysql.connector'**

**Error:**
```
ModuleNotFoundError: No module named 'mysql.connector'
```

**วิธีแก้:**
```bash
pip install mysql-connector-python
```

---

### ❌ **ปัญหา: Jupyter Notebook ไม่เปิด**

**Error:**
```
jupyter: command not found
```

**วิธีแก้:**
```bash
pip install jupyter
```

หรือ
```bash
python3 -m pip install jupyter
```

---

### ❌ **ปัญหา: Stored Procedure not found**

**Error:**
```
PROCEDURE portfolio_backtesting.sp_get_top_performers does not exist
```

**วิธีแก้:**

รัน `setup_procedures.py` อีกครั้ง:
```bash
python3 setup_procedures.py
```

หรือรันใน MySQL Workbench:
- เปิดไฟล์ `database/stored_procedures.sql`
- Execute

---

### ❌ **ปัญหา: Database 'portfolio_backtesting' ไม่มี**

**Error:**
```
Unknown database 'portfolio_backtesting'
```

**วิธีแก้:**

1. เปิด MySQL Workbench
2. รันไฟล์ `database/complete_setup.sql` เพื่อสร้าง Database
3. Import ข้อมูลจาก `data/etf_price_history.csv`

---

### ❌ **ปัญหา: Jupyter Kernel ค้าง**

**Symptom:**
- Cell รันไม่เสร็จ
- แสดง `[*]` อยู่เรื่อยๆ

**วิธีแก้:**

1. กด **Kernel** → **Interrupt**
2. ถ้ายังไม่หาย: **Kernel** → **Restart**
3. รัน Cell ใหม่

---

## 📊 สรุปการใช้งาน

### **สำหรับ Live Demo ต่อหน้าอาจารย์:** ⭐

```bash
# 1. ติดตั้ง SQL Procedures (ครั้งเดียว)
python3 setup_procedures.py

# 2. เปิด Jupyter Notebook
jupyter notebook

# 3. เปิด live_demo_analytics.ipynb

# 4. รัน Cell 1 (Setup) → Shift+Enter

# 5. รัน Cell 2 (Main Loop) → Shift+Enter ครั้งเดียว

# 6. เลือก Option 1-5 ไปเรื่อยๆ จนกว่าจะ Exit (0)
```

---

### **สำหรับส่งงาน/ใช้งานจริง:**

```bash
# 1. ติดตั้ง SQL Procedures (ครั้งเดียว)
python3 setup_procedures.py

# 2. รันระบบหลัก
python3 main.py

# 3. ใช้งานตาม Menu
```

---

## 🎯 ไฟล์ทั้งหมดและการใช้งาน

| ไฟล์ | ประเภท | ใช้งานอย่างไร |
|------|--------|--------------|
| **main.py** | Python Script | `python3 main.py` - ระบบหลัก (Integrated System) |
| **live_demo_analytics.ipynb** | Jupyter Notebook | `jupyter notebook` → เลือกไฟล์นี้ → Live Demo |
| **demo_analytics.ipynb** | Jupyter Notebook | `jupyter notebook` → เลือกไฟล์นี้ → Demo แบบรันทีละ Cell |
| **setup_procedures.py** | Python Script | `python3 setup_procedures.py` - ติดตั้ง SQL Procedures (ครั้งเดียว) |
| **database/stored_procedures.sql** | SQL Script | รันใน MySQL Workbench (ทางเลือก) |
| **database/complete_setup.sql** | SQL Script | รันใน MySQL Workbench เพื่อสร้าง Database |

---

## 💡 Tips

1. **ติดตั้ง SQL Procedures ครั้งเดียวพอ** - หลังจากนั้นใช้งาน Notebook หรือ main.py ได้เลย

2. **Jupyter Notebook vs main.py:**
   - **Jupyter** = Demo/Presentation
   - **main.py** = ระบบหลักตามโจทย์อาจารย์

3. **Live Demo ต่อหน้าอาจารย์:**
   - ใช้ `live_demo_analytics.ipynb`
   - รัน Cell เดียว แล้ววนลูปได้เรื่อยๆ
   - ตรงตามโจทย์ที่อาจารย์ต้องการ

4. **ตรวจสอบ MySQL ก่อนใช้งานทุกครั้ง:**
   ```bash
   # Windows
   net start | findstr MySQL

   # Mac/Linux
   ps aux | grep mysql
   ```

---

## 📞 ติดปัญหา?

อ่านเพิ่มเติมได้ที่:
- **SYSTEM_READY_GUIDE.md** - คู่มือการใช้งานระบบแบบสมบูรณ์
- **README.md** - ข้อมูลโปรเจกต์

---

**Good luck! 🚀**

**อัปเดตล่าสุด:** 2025-11-19
**Branch:** `claude/create-project-checklist-01P2ygCJJ7yisYcFBPZZEWtN`
