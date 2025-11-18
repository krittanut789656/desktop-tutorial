# 📥 Database Import Guide

คำแนะนำทีละขั้นตอนสำหรับการ Import ข้อมูลเข้า MySQL

---

## ✅ สิ่งที่ต้องเตรียม

- ✅ MySQL Server installed และ running
- ✅ MySQL username: `root`
- ✅ MySQL password: `krittanut123456`
- ✅ Python 3.7+ installed
- ✅ ไฟล์ข้อมูลทั้งหมด (อยู่ใน repository แล้ว)

---

## 🚀 Method 1: ใช้ Python Script (แนะนำ - ง่ายที่สุด)

### Step 1: เปิด Terminal/Command Prompt

```bash
cd /path/to/desktop-tutorial
```

### Step 2: Install Dependencies

```bash
pip install mysql-connector-python pandas
```

### Step 3: Run Import Script

```bash
cd scripts
python import_to_mysql.py
```

### ✅ ผลลัพธ์ที่ควรเห็น:

```
╔════════════════════════════════════════════════════════════╗
║    Portfolio Backtesting System - Data Import            ║
╚════════════════════════════════════════════════════════════╝

Connecting to MySQL...
✅ Database schema created

============================================================
Importing ETF Master Data
============================================================
✅ SPY: SPDR S&P 500 ETF Trust
✅ VOO: Vanguard S&P 500 ETF
...
✅ Imported 50 ETFs

============================================================
Importing Price History Data
============================================================
File size: 23.00 MB
Processing chunk 1... ✅ 10000 rows
Processing chunk 2... ✅ 10000 rows
...
✅ Total imported: 208,700 price records

============================================================
Importing Benchmark Portfolios
============================================================
✅ Traditional 60/40
✅ Aggressive 80/20
...
✅ Imported 35 benchmark portfolios

============================================================
Importing Benchmark Holdings
============================================================
✅ Imported 117 holdings

============================================================
VERIFICATION SUMMARY
============================================================
etf_master                            50 rows
price_history                    208,700 rows
benchmark_portfolios                  35 rows
benchmark_holdings                   117 rows
============================================================

✅ Import completed successfully!
```

---

## 🗄️ Method 2: ใช้ MySQL Workbench (Alternative)

### Step 1: เปิด MySQL Workbench

### Step 2: Connect to MySQL Server
- Host: `127.0.0.1`
- Port: `3306`
- Username: `root`
- Password: `krittanut123456`

### Step 3: Run SQL Script
1. File → Open SQL Script
2. เลือก `database/complete_setup.sql`
3. Click ⚡ Execute

### Step 4: Import Data Using Python
หลังจาก run SQL script แล้ว ยังต้องใช้ Python script import ข้อมูล:

```bash
cd scripts
python import_to_mysql.py
```

---

## 🗄️ Method 3: ใช้ MySQL Command Line

### Step 1: เปิด MySQL Command Line

**Windows:**
```bash
mysql -u root -p
# Enter password: krittanut123456
```

**macOS/Linux:**
```bash
mysql -u root -pkrittanut123456
```

### Step 2: Run SQL Script

```sql
SOURCE /path/to/desktop-tutorial/database/complete_setup.sql;
```

### Step 3: Verify Tables Created

```sql
USE portfolio_backtesting;
SHOW TABLES;
```

ควรเห็น 9 tables:
- backtest_results
- backtest_scenarios
- benchmark_holdings
- benchmark_portfolios
- etf_master
- portfolio_snapshots
- price_history
- scenario_holdings
- transaction_log

### Step 4: Import Data Using Python Script

```bash
# Exit MySQL
exit;

# Run Python import script
cd scripts
python import_to_mysql.py
```

---

## ✅ Verification - ตรวจสอบว่า Import สำเร็จ

### ใช้ MySQL Command Line:

```sql
USE portfolio_backtesting;

-- Check number of rows in each table
SELECT 'etf_master' AS table_name, COUNT(*) AS rows FROM etf_master
UNION ALL
SELECT 'price_history', COUNT(*) FROM price_history
UNION ALL
SELECT 'benchmark_portfolios', COUNT(*) FROM benchmark_portfolios
UNION ALL
SELECT 'benchmark_holdings', COUNT(*) FROM benchmark_holdings;
```

### ✅ ผลลัพธ์ที่ถูกต้อง:

| table_name | rows |
|-----------|------|
| etf_master | 50 |
| price_history | 208,700 |
| benchmark_portfolios | 35 |
| benchmark_holdings | 117 |

### Sample Queries:

```sql
-- View ETFs
SELECT ticker_symbol, etf_name, asset_class
FROM etf_master
LIMIT 10;

-- View Benchmark Portfolios
SELECT benchmark_name, risk_level, target_return
FROM benchmark_portfolios
LIMIT 10;

-- Price data date range
SELECT
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    COUNT(DISTINCT etf_id) AS num_etfs,
    COUNT(*) AS total_rows
FROM price_history;
```

---

## ❗ Troubleshooting

### Error: "Can't connect to MySQL server"

**Solution:**
1. ตรวจสอบว่า MySQL Server running อยู่
2. ตรวจสอบ username/password ถูกต้อง
3. ตรวจสอบ port 3306 ไม่ถูก block

**Windows:**
```bash
# Check MySQL service
services.msc
# หา "MySQL" และตรวจสอบว่า running
```

**macOS:**
```bash
mysql.server status
# ถ้า stopped: mysql.server start
```

**Linux:**
```bash
sudo service mysql status
# ถ้า inactive: sudo service mysql start
```

### Error: "Access denied for user 'root'"

**Solution:**
1. ตรวจสอบ password ถูกต้อง
2. อัพเดท password ใน `scripts/import_to_mysql.py`:

```python
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE'  # <-- เปลี่ยนที่นี่
}
```

### Error: "No module named 'mysql.connector'"

**Solution:**
```bash
pip install mysql-connector-python
```

### Error: "No module named 'pandas'"

**Solution:**
```bash
pip install pandas
```

---

## 📊 Next Steps

หลังจาก import สำเร็จแล้ว:

1. ✅ Database พร้อมใช้งาน (9 tables)
2. ✅ ข้อมูล 50 ETFs พร้อม
3. ✅ ข้อมูลราคา 208,700 rows พร้อม
4. ✅ Benchmark portfolios 35 ตัวพร้อม

**ขั้นตอนถัดไป:**
- สร้าง Python modules (main.py, analytics.py)
- Implement SQL queries (11 insights)
- Build CRUD operations
- Create ER Diagram

---

## 💡 Tips

- ✅ Import ครั้งแรกอาจใช้เวลา 2-3 นาที (price_history มี 208,700 rows)
- ✅ ถ้าต้องการ import ใหม่ ให้ run SQL script `complete_setup.sql` ก่อน (จะ DROP และสร้าง database ใหม่)
- ✅ สำรอง data ก่อน DROP database:
  ```bash
  mysqldump -u root -p portfolio_backtesting > backup.sql
  ```

---

## ✉️ Need Help?

ถ้ามีปัญหา:
1. ตรวจสอบ error message ที่แสดง
2. ดู Troubleshooting section ด้านบน
3. ตรวจสอบ MySQL logs

**Happy Importing! 🚀**
