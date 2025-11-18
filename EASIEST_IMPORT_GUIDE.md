# 📋 วิธี Import ข้อมูล - ง่ายที่สุด (ไม่ต้องเขียนโค้ด!)

## ใช้ MySQL Workbench + Excel Files

---

## ขั้นตอนที่ 1: เปิด MySQL Workbench

1. เปิดโปรแกรม **MySQL Workbench**
2. Double-click ที่ **MyLocalDB** (127.0.0.1:3306)
3. ใส่ password: `krittanut123456`
4. กด **OK**

---

## ขั้นตอนที่ 2: เลือก Database

ด้านซ้ายมือ ใน **SCHEMAS** tab:

1. ขยาย (expand) `portfolio_backtesting`
2. ขยาย `Tables`
3. คุณจะเห็น 9 ตาราง

---

## ขั้นตอนที่ 3: Import ตารางที่ 1 - etf_master

### 3.1 เตรียมไฟล์

1. เปิดโฟลเดอร์ `desktop-tutorial/excel_files/`
2. เปิดไฟล์ `1_etf_master.xlsx` ด้วย Excel
3. **File → Save As → Save as type: CSV (Comma delimited)**
4. Save เป็น `1_etf_master.csv`

### 3.2 Import

กลับมาที่ MySQL Workbench:

1. **คลิกขวา** ที่ตาราง `etf_master`
2. เลือก **Table Data Import Wizard**
3. กด **Browse** → เลือกไฟล์ `1_etf_master.csv` ที่เพิ่ง save
4. กด **Next**
5. เลือก **Use existing table: `portfolio_backtesting`.`etf_master`**
6. กด **Next**
7. ตรวจสอบ column mapping (ควรจะ map อัตโนมัติ):
   ```
   etf_id          → etf_id
   ticker_symbol   → ticker_symbol
   etf_name        → etf_name
   asset_class     → asset_class
   region          → region
   sector          → sector
   expense_ratio   → expense_ratio
   inception_date  → inception_date
   ```
8. กด **Next**
9. กด **Next** อีกครั้ง
10. รอสักครู่ → เห็น **Import completed** ✅
11. กด **Finish**

### 3.3 ตรวจสอบ

รัน SQL นี้:
```sql
SELECT COUNT(*) FROM etf_master;
```

ผลลัพธ์ต้องได้: **50**

---

## ขั้นตอนที่ 4: Import ตารางที่ 2 - benchmark_portfolios

### 4.1 เตรียมไฟล์

1. เปิดไฟล์ `2_benchmark_portfolios.xlsx`
2. **File → Save As → CSV**
3. Save เป็น `2_benchmark_portfolios.csv`

### 4.2 Import

1. **คลิกขวา** ที่ตาราง `benchmark_portfolios`
2. **Table Data Import Wizard**
3. เลือกไฟล์ `2_benchmark_portfolios.csv`
4. **Next → Use existing table → Next**
5. ตรวจสอบ column mapping
6. **Next → Next → Finish**

### 4.3 ตรวจสอบ

```sql
SELECT COUNT(*) FROM benchmark_portfolios;
```

ผลลัพธ์ต้องได้: **35**

---

## ขั้นตอนที่ 5: Import ตารางที่ 3 - benchmark_holdings

### 5.1 เตรียมไฟล์

1. เปิดไฟล์ `3_benchmark_holdings.xlsx`
2. **File → Save As → CSV**
3. Save เป็น `3_benchmark_holdings.csv`

### 5.2 Import

1. **คลิกขวา** ที่ตาราง `benchmark_holdings`
2. **Table Data Import Wizard**
3. เลือกไฟล์ `3_benchmark_holdings.csv`
4. **Next → Use existing table → Next**
5. Column mapping:
   ```
   benchmark_id → benchmark_id
   etf_id       → etf_id
   target_weight → target_weight
   ```
6. **Next → Next → Finish**

### 5.3 ตรวจสอบ

```sql
SELECT COUNT(*) FROM benchmark_holdings;
```

ผลลัพธ์ต้องได้: **114-116**

---

## ขั้นตอนที่ 6: Import ตารางที่ 4 - price_history (3 ไฟล์)

### 6.1 เตรียมไฟล์ (ทำทีละไฟล์)

**ไฟล์ที่ 1:**
1. เปิด `4_price_history_part01.xlsx`
2. **File → Save As → CSV**
3. Save เป็น `4_price_history_part01.csv`

### 6.2 Import ไฟล์ที่ 1

1. **คลิกขวา** ที่ตาราง `price_history`
2. **Table Data Import Wizard**
3. เลือกไฟล์ `4_price_history_part01.csv`
4. **Next → Use existing table → Next**
5. Column mapping:
   ```
   etf_id       → etf_id
   price_date   → price_date
   open_price   → open_price
   high_price   → high_price
   low_price    → low_price
   close_price  → close_price
   volume       → volume
   ```
6. **Next → Next**
7. **รอ 1-2 นาที** (ไฟล์ใหญ่)
8. **Finish** เมื่อเสร็จ

### 6.3 Import ไฟล์ที่ 2

ทำซ้ำขั้นตอนเดิมกับ `4_price_history_part02.xlsx`:
1. Save as CSV
2. Table Data Import Wizard
3. Import เข้า `price_history` (ตารางเดิม)

### 6.4 Import ไฟล์ที่ 3

ทำซ้ำขั้นตอนเดิมกับ `4_price_history_part03.xlsx`:
1. Save as CSV
2. Table Data Import Wizard
3. Import เข้า `price_history` (ตารางเดิม)

### 6.5 ตรวจสอบ

```sql
SELECT COUNT(*) FROM price_history;
```

ผลลัพธ์ต้องได้: **208,700** (หรือใกล้เคียง)

---

## ขั้นตอนที่ 7: ตรวจสอบทั้งหมด

รัน SQL นี้:

```sql
SELECT 'etf_master' AS table_name, COUNT(*) AS rows FROM etf_master
UNION ALL
SELECT 'benchmark_portfolios', COUNT(*) FROM benchmark_portfolios
UNION ALL
SELECT 'benchmark_holdings', COUNT(*) FROM benchmark_holdings
UNION ALL
SELECT 'price_history', COUNT(*) FROM price_history;
```

**ผลลัพธ์ที่ถูกต้อง:**
```
etf_master           : 50
benchmark_portfolios : 35
benchmark_holdings   : 114-116
price_history        : 208,700
```

---

## 🎉 เสร็จแล้ว!

ถ้าเห็นตัวเลขตรงนี้ แสดงว่า **Import สำเร็จ** แล้ว!

---

## ❌ ถ้ามีปัญหา:

### ปัญหา 1: Import Wizard ไม่เห็น

**วิธีแก้:**
- ลง MySQL Workbench version ใหม่กว่า 8.0
- หรือใช้วิธีอื่น: copy ไฟล์ CSV ไปที่ `C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\` แล้วใช้ `LOAD DATA INFILE`

### ปัญหา 2: Error 1366 - Incorrect string value

**วิธีแก้:**
- เปิด Excel file
- Save As → CSV UTF-8 (แทน CSV ธรรมดา)

### ปัญหา 3: Error 1062 - Duplicate entry

**วิธีแก้:**
- มีข้อมูลอยู่แล้ว ให้ลบก่อน:
```sql
DELETE FROM price_history;
DELETE FROM benchmark_holdings;
DELETE FROM benchmark_portfolios;
DELETE FROM etf_master;
```

---

## 💡 เคล็ดลับ:

1. **Import ตามลำดับ** (1 → 2 → 3 → 4) เพราะมี Foreign Keys
2. **รอให้เสร็จ** price_history ใช้เวลานาน
3. **ตรวจสอบทีละตาราง** ด้วย `SELECT COUNT(*)`
4. **Save as CSV** ก่อน import ทุกครั้ง (Workbench รับ CSV ดีกว่า Excel)

---

## ⏱️ เวลาที่ใช้:

- ตาราง 1-3: อย่างละ 1-2 นาที
- ตาราง 4: 5-10 นาที (3 ไฟล์)
- **รวม: 15-20 นาที**

---

## 🆘 ถ้ายังไม่ได้:

บอกผมว่า:
1. ติดที่ขั้นตอนไหน?
2. Error message คืออะไร?
3. ผลลัพธ์จาก `SELECT COUNT(*)` ได้เท่าไหร่?

ผมจะช่วยแก้ให้ทันที!

---

## ❓ คำถามที่พบบ่อย (FAQ)

### Q1: Excel ไม่มี column `created_at` แต่ตาราง MySQL มี จะ import ได้ไหม?

**A: ได้!** ไม่มีปัญหา

ทุกตารางมี:
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**ความหมาย:**
- MySQL จะสร้าง `created_at` ให้อัตโนมัติ ตอน import
- คุณ **ไม่ต้อง** ใส่ column `created_at` ใน Excel
- Import ปกติได้เลย ไม่ error

**ตัวอย่าง:**

Excel มี:
```
etf_id, ticker_symbol, etf_name, ...
1, SPY, SPDR S&P 500, ...
```

MySQL จะได้:
```
etf_id, ticker_symbol, etf_name, ..., created_at
1, SPY, SPDR S&P 500, ..., 2024-11-18 10:30:00
```

MySQL สร้าง timestamp ให้เองตอน insert!

### Q2: ถ้า import ไฟล์เดิมซ้ำ จะเกิดอะไร?

**A: Error 1062 - Duplicate entry**

เพราะ `etf_id` เป็น PRIMARY KEY ห้ามซ้ำ

**วิธีแก้:**
```sql
DELETE FROM price_history;
DELETE FROM benchmark_holdings;
DELETE FROM benchmark_portfolios;
DELETE FROM etf_master;
```

จากนั้น import ใหม่

### Q3: ทำไม price_history ต้องแบ่ง 3 ไฟล์?

**A: Excel มีขอบเขต 1,048,576 rows**

ข้อมูล price_history มี 208,700 rows ดังนั้น:
- Part 1: 70,000 rows
- Part 2: 70,000 rows  
- Part 3: 68,700 rows

Import ทีละไฟล์เข้า table เดียวกัน

### Q4: Column mapping ไม่ตรง ทำยังไง?

**A: แก้ด้วยมือ**

ใน Table Data Import Wizard:
1. ที่หน้า **Configure Import Settings**
2. คลิกที่ dropdown ของแต่ละ column
3. เลือก column ที่ตรง

**ตัวอย่าง:**
```
Source Column    →  Destination Column
─────────────────────────────────────
etf_id           →  etf_id
ticker_symbol    →  ticker_symbol
etf_name         →  etf_name
(ignore)         →  created_at  ← ปล่อยว่างไว้
```

### Q5: เช็คว่า import สำเร็จยังไง?

**A: รัน SQL นี้:**
```sql
-- เช็คจำนวน
SELECT 
    'etf_master' AS table_name, 
    COUNT(*) AS rows 
FROM etf_master
UNION ALL
SELECT 'benchmark_portfolios', COUNT(*) FROM benchmark_portfolios
UNION ALL  
SELECT 'benchmark_holdings', COUNT(*) FROM benchmark_holdings
UNION ALL
SELECT 'price_history', COUNT(*) FROM price_history;

-- เช็คข้อมูล sample
SELECT * FROM etf_master LIMIT 5;
SELECT * FROM price_history LIMIT 5;
```

**ผลลัพธ์ที่ถูกต้อง:**
```
etf_master           : 50
benchmark_portfolios : 35
benchmark_holdings   : 114-116
price_history        : 208,700
```

---

## 📝 สรุปสั้นๆ

1. **Excel ไม่ต้องมี created_at** ✅
2. **Import ทีละตาราง** (1 → 2 → 3 → 4)
3. **Save as CSV ก่อน** import
4. **ตรวจสอบด้วย SELECT COUNT(*)**
5. **ใช้เวลา 15-20 นาที** รวมทั้งหมด

**ถ้ายังติดปัญหา บอกผมได้เลย!** 💪
