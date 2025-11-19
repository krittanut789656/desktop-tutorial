# 🔧 คู่มือติดตั้ง SQL Stored Procedures แบบละเอียด

**setup_procedures.py - Step by Step Guide**

---

## 📋 สารบัญ

1. [เตรียมความพร้อม](#1-เตรียมความพร้อม)
2. [ตรวจสอบ MySQL Server](#2-ตรวจสอบ-mysql-server)
3. [แก้ไข Password (ถ้าจำเป็น)](#3-แก้ไข-password-ถ้าจำเป็น)
4. [รัน setup_procedures.py](#4-รัน-setupprocedurespy)
5. [ตรวจสอบผลลัพธ์](#5-ตรวจสอบผลลัพธ์)
6. [วิธีแก้ปัญหา (Troubleshooting)](#6-วิธีแก้ปัญหา-troubleshooting)
7. [ทางเลือก: รันใน MySQL Workbench](#7-ทางเลือก-รันใน-mysql-workbench)

---

## 1. เตรียมความพร้อม

### ✅ สิ่งที่ต้องมี:

1. **Python 3.8+** ติดตั้งแล้ว
   ```bash
   python3 --version
   # ควรแสดง: Python 3.8.x หรือสูงกว่า
   ```

2. **MySQL Server** ติดตั้งและทำงานอยู่
   - MySQL 5.7+ หรือ MySQL 8.0+

3. **Database `portfolio_backtesting`** สร้างแล้ว
   - ถ้ายังไม่มี ให้รัน `database/complete_setup.sql` ก่อน

4. **Python Library: mysql-connector-python**
   ```bash
   pip install mysql-connector-python
   ```

---

## 2. ตรวจสอบ MySQL Server

### **Windows:**

**วิธีที่ 1: ใช้ Command Prompt (CMD)**

1. เปิด **Command Prompt** (กด Win+R → พิมพ์ `cmd` → Enter)

2. ตรวจสอบว่า MySQL ทำงานหรือไม่:
   ```cmd
   net start | findstr MySQL
   ```

   **ผลลัพธ์ที่ดี:**
   ```
   MySQL80
   ```

3. **ถ้า MySQL ไม่ทำงาน** (ไม่มีผลลัพธ์):
   ```cmd
   net start MySQL80
   ```

   หรือ
   ```cmd
   net start MySQL
   ```

**วิธีที่ 2: ใช้ Services**

1. กด **Win+R** → พิมพ์ `services.msc` → Enter
2. หา **MySQL80** หรือ **MySQL**
3. ตรวจสอบ **Status**:
   - ถ้าเป็น **"Running"** = ✅ พร้อมใช้งาน
   - ถ้าเป็น **"Stopped"** = คลิกขวา → **Start**

---

### **Mac:**

**วิธีที่ 1: ใช้ Terminal**

1. เปิด **Terminal** (Cmd+Space → พิมพ์ `Terminal`)

2. ตรวจสอบว่า MySQL ทำงานหรือไม่:
   ```bash
   brew services list | grep mysql
   ```

   **ผลลัพธ์ที่ดี:**
   ```
   mysql    started
   ```

3. **ถ้า MySQL ไม่ทำงาน**:
   ```bash
   brew services start mysql
   ```

**วิธีที่ 2: ใช้ System Preferences**

1. เปิด **System Preferences**
2. คลิก **MySQL**
3. คลิก **Start MySQL Server**

---

### **Linux (Ubuntu/Debian):**

1. เปิด **Terminal**

2. ตรวจสอบ status:
   ```bash
   sudo service mysql status
   ```

   **ผลลัพธ์ที่ดี:**
   ```
   ● mysql.service - MySQL Community Server
      Loaded: loaded
      Active: active (running)
   ```

3. **ถ้า MySQL ไม่ทำงาน**:
   ```bash
   sudo service mysql start
   ```

---

## 3. แก้ไข Password (ถ้าจำเป็น)

### **ตรวจสอบ MySQL Password ของคุณ**

1. เปิดไฟล์ **`setup_procedures.py`** ด้วย Text Editor (VS Code, Notepad++, etc.)

2. หาบรรทัดนี้ (บรรทัดที่ 10-15):
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'krittanut123456',  # ⬅️ ตรงนี้!
       'database': 'portfolio_backtesting'
   }
   ```

3. **แก้ไข `password`** ให้ตรงกับ MySQL password ของคุณ:
   ```python
   'password': 'YOUR_ACTUAL_PASSWORD',  # เช่น 'mypassword123'
   ```

4. **บันทึกไฟล์** (Ctrl+S หรือ Cmd+S)

---

### **ไม่รู้ Password?**

**วิธีหา/รีเซ็ต MySQL Password:**

1. เปิด **MySQL Workbench**
2. ถ้า Connect ได้โดยไม่ต้องใส่ password → Password คือ **`""`** (เว้นว่าง)
3. ถ้า Connect ได้ด้วย password ที่จำได้ → ใช้ password นั้น
4. ถ้าลืม password → ต้องรีเซ็ต MySQL root password (ดูวิธีใน Google: "reset mysql root password")

---

## 4. รัน setup_procedures.py

### **ขั้นตอนการรัน:**

**Step 1: เปิด Terminal/Command Prompt**

- **Windows**: Win+R → `cmd` → Enter
- **Mac**: Cmd+Space → `Terminal` → Enter
- **Linux**: Ctrl+Alt+T

**Step 2: ไปที่โฟลเดอร์ `desktop-tutorial`**

```bash
cd desktop-tutorial
```

หรือถ้าอยู่ที่อื่น:
```bash
cd /path/to/your/desktop-tutorial
```

**ตัวอย่าง:**
```bash
# Windows
cd C:\Users\YourName\Documents\desktop-tutorial

# Mac/Linux
cd ~/Documents/desktop-tutorial
```

**Step 3: ตรวจสอบว่าไฟล์มีอยู่**

```bash
ls setup_procedures.py
```
หรือ (Windows):
```cmd
dir setup_procedures.py
```

ควรเห็น:
```
setup_procedures.py
```

**Step 4: รัน script**

```bash
python3 setup_procedures.py
```

หรือ (Windows บางเครื่อง):
```cmd
python setup_procedures.py
```

---

## 5. ตรวจสอบผลลัพธ์

### **✅ กรณีสำเร็จ:**

คุณจะเห็นข้อความแบบนี้:

```
============================================================
🚀 ติดตั้ง SQL Stored Procedures & Views
============================================================

🔌 กำลังเชื่อมต่อ MySQL...
✅ เชื่อมต่อ MySQL สำเร็จ!

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

**ถ้าเห็นข้อความนี้ = สำเร็จ! 🎉**

ตอนนี้สามารถรัน:
- `python3 main.py`
- `python3 live_demo.py`
- หรือเปิด Jupyter Notebook: `live_demo_analytics.ipynb`

---

## 6. วิธีแก้ปัญหา (Troubleshooting)

### **❌ Error 1: Connection Error (2003)**

```
❌ MySQL Error: 2003 (HY000): Can't connect to MySQL server on 'localhost:3306' (111)
```

**สาเหตุ:** MySQL Server ไม่ทำงาน

**วิธีแก้:**

1. **เปิด MySQL Server:**
   ```bash
   # Windows
   net start MySQL80

   # Mac
   brew services start mysql

   # Linux
   sudo service mysql start
   ```

2. **ตรวจสอบอีกครั้ง:**
   ```bash
   python3 setup_procedures.py
   ```

---

### **❌ Error 2: Access Denied (1045)**

```
❌ MySQL Error: 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
```

**สาเหตุ:** Password ไม่ถูกต้อง

**วิธีแก้:**

1. **เปิดไฟล์ `setup_procedures.py`**

2. **แก้ไข password:**
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': 'YOUR_CORRECT_PASSWORD',  # ⬅️ แก้ตรงนี้
       'database': 'portfolio_backtesting'
   }
   ```

3. **บันทึกและรันใหม่:**
   ```bash
   python3 setup_procedures.py
   ```

---

### **❌ Error 3: Unknown Database**

```
❌ MySQL Error: 1049 (42000): Unknown database 'portfolio_backtesting'
```

**สาเหตุ:** ยังไม่ได้สร้าง database `portfolio_backtesting`

**วิธีแก้:**

**Option 1: ใช้ MySQL Workbench**

1. เปิด **MySQL Workbench**
2. Connect to MySQL Server
3. ไปที่ **File** → **Open SQL Script**
4. เลือกไฟล์ **`database/complete_setup.sql`**
5. กด **Execute** (⚡ icon)
6. รอจนเสร็จ
7. รัน `setup_procedures.py` อีกครั้ง

**Option 2: ใช้ Command Line**

```bash
mysql -u root -p < database/complete_setup.sql
```

---

### **❌ Error 4: File Not Found**

```
❌ ไม่พบไฟล์: database/stored_procedures.sql
```

**สาเหตุ:** รัน script ไม่ใช่ที่โฟลเดอร์ `desktop-tutorial`

**วิธีแก้:**

1. **ตรวจสอบว่าอยู่ที่โฟลเดอร์ถูกต้อง:**
   ```bash
   pwd  # Mac/Linux
   cd   # Windows
   ```

2. **ควรเห็น path ที่ลงท้ายด้วย `desktop-tutorial`**

3. **ถ้าไม่ใช่ ให้ cd ไปที่ถูกต้อง:**
   ```bash
   cd /path/to/desktop-tutorial
   ```

4. **รันใหม่:**
   ```bash
   python3 setup_procedures.py
   ```

---

### **❌ Error 5: ModuleNotFoundError**

```
ModuleNotFoundError: No module named 'mysql.connector'
```

**สาเหตุ:** ยังไม่ได้ติดตั้ง `mysql-connector-python`

**วิธีแก้:**

```bash
pip install mysql-connector-python
```

หรือ:
```bash
pip3 install mysql-connector-python
```

หรือ (ถ้ายังไม่ได้):
```bash
python3 -m pip install mysql-connector-python
```

---

### **❌ Error 6: Permission Denied**

```
PermissionError: [Errno 13] Permission denied: 'database/stored_procedures.sql'
```

**วิธีแก้:**

**Windows:**
```cmd
# รันเป็น Administrator
# คลิกขวาที่ Command Prompt → Run as administrator
```

**Mac/Linux:**
```bash
sudo python3 setup_procedures.py
```

---

## 7. ทางเลือก: รันใน MySQL Workbench

หากไม่สามารถรัน `setup_procedures.py` ได้ สามารถติดตั้ง Stored Procedures ใน MySQL Workbench แทนได้:

### **ขั้นตอน:**

**Step 1: เปิด MySQL Workbench**

**Step 2: Connect to MySQL Server**
- เลือก Connection ของคุณ (เช่น `localhost`)
- ใส่ Password
- คลิก **OK**

**Step 3: เลือก Database**
- คลิกที่ **Schemas** ทางซ้าย
- คลิกขวาที่ **`portfolio_backtesting`**
- เลือก **Set as Default Schema**

**Step 4: เปิดไฟล์ SQL**
- ไปที่ **File** → **Open SQL Script**
- เลือกไฟล์: **`database/stored_procedures.sql`**
- คลิก **Open**

**Step 5: Execute Script**
- กดปุ่ม **⚡ Execute** (หรือกด **Ctrl+Shift+Enter**)
- รอ 3-5 วินาที

**Step 6: ตรวจสอบผลลัพธ์**

ด้านล่างจะแสดง:
```
14 queries executed, 14 success, 0 errors
```

**Step 7: ตรวจสอบ Stored Procedures**
- ขยาย **`portfolio_backtesting`** ใน Schemas
- ขยาย **Stored Procedures**
- ควรเห็น 8 procedures:
  - `sp_calculate_portfolio_return`
  - `sp_calculate_sharpe_ratio`
  - `sp_calculate_max_drawdown`
  - `sp_calculate_volatility`
  - `sp_get_etf_correlation`
  - `sp_get_top_performers`
  - `sp_compare_portfolios`
  - `sp_get_portfolio_weights`

**Step 8: ตรวจสอบ Views**
- ขยาย **Views**
- ควรเห็น 3 views:
  - `vw_weekly_returns`
  - `vw_etf_performance`
  - `vw_portfolio_summary`

**ถ้าเห็นครบ = สำเร็จ! ✅**

---

## 📊 สรุปขั้นตอนแบบสั้น

```bash
# 1. ตรวจสอบ MySQL ทำงานหรือไม่
# Windows: net start | findstr MySQL
# Mac: brew services list | grep mysql

# 2. เปิด MySQL (ถ้าปิดอยู่)
# Windows: net start MySQL80
# Mac: brew services start mysql

# 3. แก้ไข password ใน setup_procedures.py (ถ้าจำเป็น)

# 4. ไปที่โฟลเดอร์โปรเจกต์
cd desktop-tutorial

# 5. รัน setup script
python3 setup_procedures.py

# 6. ตรวจสอบผลลัพธ์
# ควรเห็น "✅ ติดตั้งเสร็จสมบูรณ์!"
```

---

## ✅ Checklist

หลังจากรัน `setup_procedures.py` สำเร็จแล้ว ควรได้:

- [ ] ✅ เห็นข้อความ "✅ ติดตั้งเสร็จสมบูรณ์!"
- [ ] ✅ มี 3 Views: `vw_weekly_returns`, `vw_etf_performance`, `vw_portfolio_summary`
- [ ] ✅ มี 8 Stored Procedures: `sp_get_top_performers`, `sp_compare_portfolios`, etc.
- [ ] ✅ ไม่มี Error แสดง
- [ ] ✅ สามารถรัน `python3 main.py` หรือ `live_demo.py` ได้

---

## 🎯 ขั้นตอนถัดไป

หลังจาก setup เสร็จแล้ว:

### **1. ทดสอบระบบหลัก:**
```bash
python3 main.py
```

### **2. ทดสอบ Live Demo:**
```bash
python3 live_demo.py
```

### **3. ทดสอบ Jupyter Notebook:**
```bash
jupyter notebook
# จากนั้นเปิด live_demo_analytics.ipynb
```

---

## 💡 Tips

1. **รัน setup_procedures.py ครั้งเดียวพอ** - หลังจากนั้นสามารถใช้งาน main.py หรือ live_demo.py ได้เลย

2. **ถ้าแก้ไข stored_procedures.sql** - ต้องรัน setup_procedures.py อีกครั้งเพื่ออัปเดต

3. **เช็ค MySQL ก่อนใช้งานทุกครั้ง** - ต้องให้ MySQL Server ทำงานอยู่เสมอ

4. **Password อย่าลืม!** - เก็บ MySQL password ไว้ในที่ปลอดภัย

---

## 📞 ยังติดปัญหา?

ถ้ายังแก้ไม่ได้ ลองวิธีนี้:

1. **ดู Error Message ให้ดี** - มักจะบอกว่าปัญหาคืออะไร
2. **Google Error Message** - มักจะมีคนเจอและแก้ไปแล้ว
3. **ใช้ MySQL Workbench แทน** - วิธีที่ 7 ด้านบน (ทางเลือกที่ง่ายกว่า)
4. **ตรวจสอบ MySQL Version** - ควรเป็น 5.7+ หรือ 8.0+

---

**Good luck! 🚀**

**อัปเดตล่าสุด:** 2025-11-19
