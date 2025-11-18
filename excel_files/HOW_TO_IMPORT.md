# Import ข้อมูลเข้า MySQL - คู่มือง่ายๆ

## ✅ ไฟล์ที่ต้อง Import (ทั้งหมด 6 ไฟล์):

```
excel_files/
├── 1_etf_master.xlsx                 (50 rows)
├── 2_benchmark_portfolios.xlsx       (35 rows)
├── 3_benchmark_holdings.xlsx         (116 rows)
├── 4_price_history_part01.xlsx       (100,000 rows)
├── 4_price_history_part02.xlsx       (100,000 rows)
└── 4_price_history_part03.xlsx       (8,700 rows)
```

---

## 📋 วิธีที่ 1: ใช้ MySQL Workbench (แนะนำ - ง่ายที่สุด)

### Step 1: Import etf_master

1. เปิด MySQL Workbench
2. เชื่อมต่อกับ localhost
3. เลือก database `portfolio_backtesting`
4. คลิกขวาที่ table `etf_master` → **Table Data Import Wizard**
5. เลือกไฟล์ `1_etf_master.xlsx`
6. กด **Next** → **Next** → **Finish**
7. รอจนเสร็จ (ไม่กี่วินาที)

### Step 2: Import benchmark_portfolios

1. คลิกขวาที่ table `benchmark_portfolios` → **Table Data Import Wizard**
2. เลือกไฟล์ `2_benchmark_portfolios.xlsx`
3. กด **Next** → **Next** → **Finish**

### Step 3: Import benchmark_holdings

1. คลิกขวาที่ table `benchmark_holdings` → **Table Data Import Wizard**
2. เลือกไฟล์ `3_benchmark_holdings.xlsx`
3. กด **Next** → **Next** → **Finish**

### Step 4: Import price_history (3 ไฟล์)

**ไฟล์ที่ 1:**
1. คลิกขวาที่ table `price_history` → **Table Data Import Wizard**
2. เลือกไฟล์ `4_price_history_part01.xlsx`
3. กด **Next** → **Next** → **Finish**
4. รอ 1-2 นาที

**ไฟล์ที่ 2:**
1. ทำซ้ำกับ `4_price_history_part02.xlsx`

**ไฟล์ที่ 3:**
1. ทำซ้ำกับ `4_price_history_part03.xlsx`

---

## 📋 วิธีที่ 2: ใช้ Command Line (สำหรับคนชอบ command)

```bash
# 1. แปลง Excel เป็น CSV ก่อน (ใช้ Excel: Save As → CSV)

# 2. Import ด้วย MySQL
mysql -u root -p portfolio_backtesting

# 3. รันคำสั่งนี้ทีละตาราง:
LOAD DATA LOCAL INFILE '/path/to/1_etf_master.csv'
INTO TABLE etf_master
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

---

## ✅ ตรวจสอบว่า Import สำเร็จ

รัน SQL ใน MySQL Workbench:

```sql
USE portfolio_backtesting;

SELECT COUNT(*) FROM etf_master;           -- ต้องได้ 50
SELECT COUNT(*) FROM benchmark_portfolios; -- ต้องได้ 35
SELECT COUNT(*) FROM benchmark_holdings;   -- ต้องได้ 116
SELECT COUNT(*) FROM price_history;        -- ต้องได้ 208,700
```

---

## 💡 Tips:

1. **Import ตามลำดับ**: เริ่มจาก etf_master → benchmarks → holdings → prices
2. **ถ้า error**: ลบข้อมูลเก่าก่อน: `DELETE FROM table_name;`
3. **ใช้เวลา**: ไฟล์ price_history ใหญ่ ใช้เวลา 2-3 นาทีต่อไฟล์

---

## 🎉 เสร็จแล้ว!

หลัง import ครบ พร้อมใช้งาน:
- เปิด `main.ipynb` ใน Jupyter
- หรือรัน `python main.py`

---

## ⚠️ หมายเหตุ:

**MySQL Workbench Import Wizard:**
- รองรับ CSV และ JSON ส่วนใหญ่
- ถ้า import Excel ไม่ได้ ให้ Save As → CSV ก่อน
- หรือใช้ online tool: https://www.convertcsv.com/xlsx-to-csv.htm
