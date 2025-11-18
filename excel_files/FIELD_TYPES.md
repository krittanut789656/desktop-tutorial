# MySQL Field Types สำหรับ Import Excel

## 📋 ตารางที่ 1: etf_master (ไฟล์ 1_etf_master.xlsx)

| Column Name | Field Type | ตัวอย่างข้อมูล |
|-------------|-----------|----------------|
| ticker_symbol | VARCHAR(10) | SPY |
| etf_name | VARCHAR(255) | SPDR S&P 500 ETF Trust |
| asset_class | VARCHAR(50) | Equity |
| region | VARCHAR(50) | US |
| sector | VARCHAR(100) | Broad Market |
| expense_ratio | DECIMAL(5,4) | 0.0945 |
| inception_date | DATE | 1993-01-22 |

---

## 📋 ตารางที่ 2: benchmark_portfolios (ไฟล์ 2_benchmark_portfolios.xlsx)

| Column Name | Field Type | ตัวอย่างข้อมูล |
|-------------|-----------|----------------|
| benchmark_name | VARCHAR(100) | Traditional 60/40 |
| description | TEXT | 60% Stocks 40% Bonds |
| risk_level | VARCHAR(20) | Moderate |
| target_return | DECIMAL(5,2) | 8.0 |
| asset_allocation | TEXT | 60% SPY / 40% AGG |

**หมายเหตุ:** risk_level ต้องเป็น: Conservative, Moderate, หรือ Aggressive เท่านั้น

---

## 📋 ตารางที่ 3: benchmark_holdings (ไฟล์ 3_benchmark_holdings.xlsx)

| Column Name | Field Type | ตัวอย่างข้อมูล |
|-------------|-----------|----------------|
| benchmark_name | VARCHAR(100) | Traditional 60/40 |
| ticker_symbol | VARCHAR(10) | SPY |
| target_weight | DECIMAL(5,4) | 0.6000 |

**⚠️ สำคัญ:** ไฟล์นี้ import ไม่ได้โดยตรง! ต้องแปลง benchmark_name และ ticker_symbol เป็น ID ก่อน

---

## 📋 ตารางที่ 4: price_history (ไฟล์ 4_price_history_part*.xlsx)

| Column Name | Field Type | ตัวอย่างข้อมูล |
|-------------|-----------|----------------|
| ticker_symbol | VARCHAR(10) | SPY |
| date | DATE | 2020-01-02 |
| open | DECIMAL(12,4) | 324.8700 |
| high | DECIMAL(12,4) | 325.2500 |
| low | DECIMAL(12,4) | 323.3400 |
| close | DECIMAL(12,4) | 324.8700 |
| adj_close | DECIMAL(12,4) | 324.8700 |
| volume | BIGINT | 32856000 |

**⚠️ สำคัญ:** ไฟล์นี้มี ticker_symbol แต่ database ต้องการ etf_id!

---

## 🚨 ปัญหาที่พบ:

### ปัญหา 1: benchmark_holdings ใช้ชื่อแทน ID
**Excel มี:**
- benchmark_name (text)
- ticker_symbol (text)

**Database ต้องการ:**
- benchmark_id (INT)
- etf_id (INT)

### ปัญหา 2: price_history ใช้ ticker แทน ID
**Excel มี:**
- ticker_symbol (text)

**Database ต้องการ:**
- etf_id (INT)

---

## ✅ วิธีแก้ (ง่ายที่สุด):

ผมจะสร้าง **Excel files แบบพร้อม import** ที่มี ID แทน ให้รอครู่...

หรือถ้าอยากลองเอง:

### สำหรับ benchmark_holdings:
1. Import etf_master ก่อน
2. Import benchmark_portfolios ก่อน
3. ใน Excel ใช้ VLOOKUP เพื่อแปลงชื่อเป็น ID
4. หรือใช้ Python script

### สำหรับ price_history:
1. Import etf_master ก่อน
2. ใน Excel ใช้ VLOOKUP เพื่อแปลงชื่อเป็น ID
3. หรือใช้ Python script

---

## 💡 คำแนะนำ:

**ง่ายที่สุดคือใช้ Python script** ที่ผมจะสร้างให้:
- อ่าน Excel
- แปลง names → IDs อัตโนมัติ
- Import เข้า MySQL

**ให้ผมสร้างให้ไหมครับ?**
