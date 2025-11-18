# 🎯 วิธี Import Price History - ง่ายที่สุด!

มี **3 วิธี** ให้เลือก เรียงจากง่ายที่สุดไปยากที่สุด

---

## ✅ วิธีที่ 1: Double-Click ไฟล์ (ง่ายที่สุด!) ⭐⭐⭐

### สำหรับ Windows:

1. **Double-click ไฟล์ `IMPORT_EASY.bat`**
2. รอ 1-2 นาที
3. เสร็จแล้ว!

### สำหรับ Mac/Linux:

1. **Double-click ไฟล์ `IMPORT_EASY.sh`**
2. รอ 1-2 นาที
3. เสร็จแล้ว!

### ถ้า Double-Click ไม่ได้:

**Windows:**
```cmd
IMPORT_EASY.bat
```

**Mac/Linux:**
```bash
bash IMPORT_EASY.sh
```

---

## ✅ วิธีที่ 2: รัน Python Script เอง ⭐⭐

### ขั้นตอน:

**1. เปิด Terminal/Command Prompt**
   - Windows: กด `Win + R` → พิมพ์ `cmd` → Enter
   - Mac: กด `Cmd + Space` → พิมพ์ `terminal` → Enter
   - Linux: กด `Ctrl + Alt + T`

**2. ไปที่ folder desktop-tutorial**
   ```bash
   cd C:\Users\YourName\desktop-tutorial     # Windows
   cd ~/desktop-tutorial                      # Mac/Linux
   ```

**3. รัน script**
   ```bash
   python import_price_history.py            # Windows
   python3 import_price_history.py           # Mac/Linux
   ```

**4. รอ 1-2 นาที**

---

## ✅ วิธีที่ 3: ใช้ MySQL Workbench (ถ้าวิธีอื่นไม่ได้) ⭐

### ขั้นตอน:

**1. เปิด MySQL Workbench**

**2. เชื่อมต่อกับ database `portfolio_backtesting`**

**3. Copy SQL command นี้ไปรัน:**

```sql
-- ตรวจสอบว่ามีข้อมูล ETF แล้ว
SELECT COUNT(*) FROM etf_master;  -- ต้องได้ 50

-- ถ้ายังไม่มี ให้รัน IMPORT_ALL_DATA.sql ก่อน!
```

**4. ใช้ Table Data Import Wizard:**
   - คลิกขวาที่ตาราง `price_history`
   - เลือก "Table Data Import Wizard"
   - เลือกไฟล์: `data/etf_price_history.csv`
   - Mapping columns:
     - `ticker` → ไม่ต้อง map (skip)
     - `date` → `price_date`
     - `open` → `open_price`
     - `high` → `high_price`
     - `low` → `low_price`
     - `close` → `close_price`
     - `adj_close` → ไม่ต้อง map (skip)
     - `volume` → `volume`
   - **⚠️ สำคัญ**: ต้องไป Edit ใน column `etf_id` ให้ map จาก ticker → etf_id ด้วย SQL:
     ```sql
     UPDATE price_history
     SET etf_id = (SELECT etf_id FROM etf_master WHERE ticker_symbol = '[ticker from CSV]')
     WHERE etf_id IS NULL;
     ```

**⚠️ วิธีนี้ยุ่งยากมาก ไม่แนะนำ!**

---

## ❌ Troubleshooting

### Error: "python is not recognized..."

**ปัญหา**: ไม่มี Python หรือไม่ได้ติดตั้งใน PATH

**วิธีแก้**:
1. ติดตั้ง Python จาก: https://www.python.org/downloads/
2. **สำคัญ**: เลือก "Add Python to PATH" ตอนติดตั้ง
3. Restart Terminal/Command Prompt
4. ลองรันใหม่

---

### Error: "No module named 'mysql'"

**ปัญหา**: ยังไม่ติดตั้ง library

**วิธีแก้**:
```bash
pip install mysql-connector-python pandas         # Windows
pip3 install mysql-connector-python pandas        # Mac/Linux
```

---

### Error: "Can't connect to MySQL server"

**ปัญหา**: MySQL ไม่ได้เปิดหรือ password ผิด

**วิธีแก้**:
1. ตรวจสอบ MySQL server ทำงานอยู่
2. เปิดไฟล์ `import_price_history.py`
3. แก้ password ให้ตรงกับเครื่องคุณ (บรรทัดที่ 25)
   ```python
   'password': 'your_password_here',
   ```

---

### Error: "No such file or directory: 'data/etf_price_history.csv'"

**ปัญหา**: ไม่ได้อยู่ใน folder ที่ถูกต้อง

**วิธีแก้**:
1. ตรวจสอบว่าคุณอยู่ใน folder `desktop-tutorial`
2. ตรวจสอบว่ามีไฟล์ `data/etf_price_history.csv`
3. ใช้ `IMPORT_EASY.bat` หรือ `IMPORT_EASY.sh` แทน (จะแก้ path ให้อัตโนมัติ)

---

### ยังไม่ได้อีก?

**ติดต่อผมพร้อมข้อมูลนี้:**
1. ระบบปฏิบัติการ (Windows/Mac/Linux)
2. Error message ทั้งหมด
3. ผลลัพธ์จาก command นี้:
   ```bash
   python --version                    # หรือ python3 --version
   pip list | grep mysql              # หรือ pip3 list | grep mysql
   ```

---

## 🎉 ตรวจสอบว่า Import สำเร็จ

รัน SQL นี้ใน MySQL Workbench:

```sql
SELECT COUNT(*) FROM price_history;
-- ต้องได้ 208,700 rows
```

```sql
SELECT
    e.ticker_symbol,
    ph.price_date,
    ph.close_price
FROM price_history ph
JOIN etf_master e ON ph.etf_id = e.etf_id
ORDER BY ph.price_date DESC
LIMIT 10;
-- ต้องเห็นข้อมูล 10 rows
```

---

## 💡 สรุป

**แนะนำวิธีที่ 1** - Double-click `IMPORT_EASY.bat` (Windows) หรือ `IMPORT_EASY.sh` (Mac/Linux)

ง่ายที่สุด ไม่ต้องพิมพ์ command ใดๆ แค่ double-click เดียว! 🚀
