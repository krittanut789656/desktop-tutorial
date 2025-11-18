# 📥 Import Price History - คู่มือใช้งาน

มี 3 วิธี เลือกได้ตามความสะดวก:

---

## 🚀 วิธีที่ 1: LOAD DATA INFILE (เร็วที่สุด!)

### ขั้นตอน:

#### 1. เปิดไฟล์ `IMPORT_PRICE_HISTORY.sql`

#### 2. แก้ path ให้ตรงกับเครื่องคุณ

หาบรรทัดนี้:
```sql
LOAD DATA LOCAL INFILE 'C:/Users/YourName/desktop-tutorial/data/etf_price_history.csv'
```

แก้เป็น path จริงของคุณ:

**Windows:**
```sql
LOAD DATA LOCAL INFILE 'C:/Users/Krittanut/desktop-tutorial/data/etf_price_history.csv'
```

**Mac/Linux:**
```sql
LOAD DATA LOCAL INFILE '/Users/Krittanut/desktop-tutorial/data/etf_price_history.csv'
```

⚠️ **สำคัญ:** ใช้ forward slash `/` แม้ใน Windows!

#### 3. Enable local_infile

ใน MySQL Workbench รัน:

```sql
SET GLOBAL local_infile = 1;
```

จากนั้นปิด connection แล้วเชื่อมต่อใหม่

หรือเพิ่ม parameter ใน connection:
```
--local-infile=1
```

#### 4. Copy-Paste ทั้งไฟล์แล้ว Execute

รอ **10-20 วินาที** (เร็วมาก!)

#### 5. เช็คผลลัพธ์

```sql
SELECT COUNT(*) FROM price_history;  -- ควรได้ 208,700
```

---

## 🐍 วิธีที่ 2: Python Script (ง่ายที่สุด!)

```bash
cd desktop-tutorial
python import_price_history.py
```

ใช้เวลา 1-2 นาที

---

## 📊 วิธีที่ 3: MySQL Workbench Import Wizard

ตาม `EASIEST_IMPORT_GUIDE.md` ขั้นตอนที่ 6:

1. แปลง Excel → CSV (3 ไฟล์)
2. คลิกขวา `price_history` → Table Data Import Wizard
3. Import ทีละไฟล์
4. ใช้เวลา 5-10 นาที

---

## ❌ แก้ปัญหา

### Error 3948: Loading local data is disabled

**สาเหตุ:** `local_infile` ถูก disable

**วิธีแก้:**

```sql
-- ตรวจสอบ
SHOW VARIABLES LIKE 'local_infile';

-- ถ้าได้ OFF ให้เปิด
SET GLOBAL local_infile = 1;

-- Reconnect MySQL Workbench
-- จากนั้นลองใหม่
```

### Error 1290: The MySQL server is running with --secure-file-priv

**สาเหตุ:** MySQL จำกัด path ที่อ่านไฟล์ได้

**วิธีแก้:**

```sql
-- เช็คว่า secure_file_priv คืออะไร
SHOW VARIABLES LIKE 'secure_file_priv';
```

ได้ path เช่น: `C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/`

**ทำอย่างใดอย่างหนึ่ง:**

1. **Copy ไฟล์ CSV ไปที่ secure_file_priv path** (แนะนำ)
   ```bash
   copy data\etf_price_history.csv "C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\"
   ```

   แล้วแก้ SQL:
   ```sql
   LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/etf_price_history.csv'
   ```
   (เอา `LOCAL` ออก)

2. **หรือใช้ Python script แทน** (ง่ายกว่า)
   ```bash
   python import_price_history.py
   ```

### Error: Can't find file

**วิธีแก้:**

1. เช็ค path ว่าถูกต้อง (ใช้ forward slash `/`)
2. เช็คว่าไฟล์มีจริง
3. ลองใช้ absolute path

---

## ✅ สรุป

**แนะนำ:**
1. ลอง LOAD DATA INFILE ก่อน (เร็วที่สุด)
2. ถ้าไม่ได้ ใช้ `python import_price_history.py` (ง่ายที่สุด)
3. ถ้ายังไม่ได้ ใช้ Import Wizard (ช้าที่สุดแต่แน่ใจว่าได้)

**เวลาที่ใช้:**
- LOAD DATA INFILE: 10-20 วินาที
- Python Script: 1-2 นาที
- Import Wizard: 5-10 นาที

---

## 📞 ต้องการความช่วยเหลือ?

บอกผม:
1. ใช้วิธีไหน?
2. Error message คืออะไร?
3. ผลจาก `SHOW VARIABLES LIKE 'local_infile'` คืออะไร?
