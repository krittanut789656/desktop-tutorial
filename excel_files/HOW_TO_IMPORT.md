# Import ข้อมูลเข้า MySQL - คู่มือง่ายๆ

## ✅ ไฟล์ Excel ที่มี (ทั้งหมด 6 ไฟล์):

```
excel_files/
├── 1_etf_master.xlsx            (50 rows)
├── 2_benchmark_portfolios.xlsx  (35 rows)
├── 3_benchmark_holdings.xlsx    (114 rows)
├── 4_price_history_part01.xlsx  (70,000 rows)
├── 4_price_history_part02.xlsx  (70,000 rows)
└── 4_price_history_part03.xlsx  (68,700 rows)
```

**✨ ไฟล์ทั้งหมดมี IDs แล้ว - Import ด้วย MySQL Workbench ได้เลย!**

---

## 📋 วิธี Import ด้วย MySQL Workbench (แนะนำ!)

### ขั้นตอนที่ 1: เปิด MySQL Workbench

1. เปิด MySQL Workbench
2. เชื่อมต่อกับ **localhost** (MyLocalDB)
3. เลือก database `portfolio_backtesting`

---

### ขั้นตอนที่ 2: Import ตาราง etf_master

1. ใน **Schemas tab** → ขยาย `portfolio_backtesting` → ขยาย `Tables`
2. **คลิกขวา** ที่ตาราง `etf_master`
3. เลือก **Table Data Import Wizard**
4. กด **Browse** → เลือกไฟล์ `1_etf_master.xlsx`
5. กด **Next**
6. เลือก **Use existing table: `etf_master`**
7. กด **Next** → ตรวจสอบ column mapping ว่าตรงกันหมด
8. กด **Next** → **Finish**
9. รอ 2-3 วินาที → เสร็จ! ✅

**ตรวจสอบ:**
```sql
SELECT COUNT(*) FROM etf_master;  -- ต้องได้ 50
```

---

### ขั้นตอนที่ 3: Import ตาราง benchmark_portfolios

1. **คลิกขวา** ที่ตาราง `benchmark_portfolios`
2. เลือก **Table Data Import Wizard**
3. เลือกไฟล์ `2_benchmark_portfolios.xlsx`
4. กด **Next** → เลือก **Use existing table**
5. กด **Next** → **Finish**

**ตรวจสอบ:**
```sql
SELECT COUNT(*) FROM benchmark_portfolios;  -- ต้องได้ 35
```

---

### ขั้นตอนที่ 4: Import ตาราง benchmark_holdings

1. **คลิกขวา** ที่ตาราง `benchmark_holdings`
2. เลือก **Table Data Import Wizard**
3. เลือกไฟล์ `3_benchmark_holdings.xlsx`
4. กด **Next** → เลือก **Use existing table**
5. กด **Next** → **Finish**

**ตรวจสอบ:**
```sql
SELECT COUNT(*) FROM benchmark_holdings;  -- ต้องได้ 114-116
```

---

### ขั้นตอนที่ 5: Import ตาราง price_history (3 ไฟล์)

**ไฟล์ที่ 1:**
1. **คลิกขวา** ที่ตาราง `price_history`
2. เลือก **Table Data Import Wizard**
3. เลือกไฟล์ `4_price_history_part01.xlsx`
4. กด **Next** → เลือก **Use existing table**
5. กด **Next** → **Finish**
6. **รอ 1-2 นาที** (ไฟล์ใหญ่)

**ไฟล์ที่ 2:**
1. ทำซ้ำกับ `4_price_history_part02.xlsx`

**ไฟล์ที่ 3:**
1. ทำซ้ำกับ `4_price_history_part03.xlsx`

**ตรวจสอบ:**
```sql
SELECT COUNT(*) FROM price_history;  -- ต้องได้ 208,700
```

---

## ✅ ตรวจสอบทั้งหมด

รัน SQL นี้เพื่อตรวจสอบว่า import ครบแล้ว:

```sql
USE portfolio_backtesting;

SELECT 'etf_master' AS table_name, COUNT(*) AS row_count FROM etf_master
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

## 💡 Tips:

1. **Import ตามลำดับ** (1 → 2 → 3 → 4) เพราะมี Foreign Keys
2. **ถ้า error "duplicate entry"**: ลบข้อมูลเก่าก่อน
   ```sql
   DELETE FROM price_history;
   DELETE FROM benchmark_holdings;
   DELETE FROM benchmark_portfolios;
   DELETE FROM etf_master;
   ```
3. **ใช้เวลา**: ไฟล์ price_history ใหญ่ รวมใช้เวลา 3-5 นาที

---

## 🎉 เสร็จแล้ว!

หลัง import ครบ พร้อมใช้งาน:
- เปิด `main.ipynb` ใน Jupyter Notebook
- หรือรัน `python main.py` สำหรับ backtesting

---

## ⚠️ หมายเหตุสำคัญ:

**ทำไมไฟล์มี etf_id และ benchmark_id?**
- เพื่อให้ import ได้โดยตรงผ่าน MySQL Workbench
- IDs เรียงตาม alphabetically (AGG=1, BND=2, ...)
- **ต้อง import ตามลำดับ** เพื่อให้ Auto Increment IDs ตรงกัน!

**ถ้า import ไม่ตามลำดับ:**
- IDs จะไม่ตรงกับที่ระบุในไฟล์
- Foreign Keys ใน benchmark_holdings และ price_history จะ error
