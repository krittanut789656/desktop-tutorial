# ข้อมูล Database - ETF Backtester

## ชื่อ Database
```
etf_backtester_db
```

**ใช้ชื่อนี้ในทุกไฟล์และทุกที่!** ✅

---

## การยืนยันชื่อ Database ในแต่ละไฟล์

### 1. Schema Files
```sql
-- database/schema/01_create_schema.sql
DROP DATABASE IF EXISTS etf_backtester_db;
CREATE DATABASE etf_backtester_db;
USE etf_backtester_db;
```

### 2. Data Files
```sql
-- database/data/02_load_etf_master.sql
USE etf_backtester_db;
```

### 3. Complete Setup File (แนะนำ)
```sql
-- database/setup_complete.sql
DROP DATABASE IF EXISTS etf_backtester_db;
CREATE DATABASE etf_backtester_db;
USE etf_backtester_db;
```

### 4. Diagnostic Files
```sql
-- database/diagnose.sql
USE etf_backtester_db;

-- database/verify.sql
USE etf_backtester_db;
```

---

## โครงสร้าง Database

### Database: `etf_backtester_db`

#### Tables (3 ตาราง):
1. **`ETF_Master`** - ข้อมูล ETF ทั้ง 50 ตัว
2. **`Price_Data`** - ข้อมูลราคาย้อนหลัง (รายสัปดาห์)
3. **`Strategy_Log`** - บันทึกการทำ backtest

#### Views (2 views):
1. **`vw_latest_prices`** - ราคาล่าสุดของแต่ละ ETF
2. **`vw_portfolio_summary`** - สรุปผลการทำ portfolio

#### Triggers (1 trigger):
1. **`validate_price_data`** - ตรวจสอบความถูกต้องของข้อมูลราคา

---

## วิธีเชื่อมต่อ Database

### 1. MySQL Command Line
```bash
mysql -u root -p etf_backtester_db
```

### 2. Python (using mysql-connector-python)
```python
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='etf_backtester_db'  # ← ชื่อ database
)
```

### 3. Python (using pymysql)
```python
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='etf_backtester_db'  # ← ชื่อ database
)
```

### 4. MySQL Workbench
1. เปิด MySQL Workbench
2. เชื่อมต่อกับ server
3. เลือก schema: **`etf_backtester_db`**

---

## การตรวจสอบว่า Database ถูกสร้างแล้ว

```sql
-- ตรวจสอบว่ามี database หรือไม่
SHOW DATABASES LIKE 'etf_backtester_db';

-- ใช้ database
USE etf_backtester_db;

-- ดูตารางทั้งหมด
SHOW TABLES;

-- ผลลัพธ์ที่คาดหวัง:
-- ETF_Master
-- Price_Data
-- Strategy_Log
-- vw_latest_prices
-- vw_portfolio_summary
```

---

## Configuration สำหรับ Connection

### ไฟล์ config.ini
```ini
[database]
host = localhost
port = 3306
user = root
password = your_password_here
database = etf_backtester_db    # ← ชื่อ database
```

### Environment Variables
```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=etf_backtester_db    # ← ชื่อ database
```

---

## สรุป

| รายการ | ค่า |
|--------|-----|
| **Database Name** | `etf_backtester_db` |
| **Character Set** | `utf8mb4` |
| **Collation** | `utf8mb4_unicode_ci` |
| **Engine** | `InnoDB` |
| **Tables** | 3 (ETF_Master, Price_Data, Strategy_Log) |
| **Views** | 2 (vw_latest_prices, vw_portfolio_summary) |
| **Triggers** | 1 (validate_price_data) |
| **ETF Records** | 50 |

---

## คำสั่งที่ใช้บ่อย

```sql
-- เลือกใช้ database
USE etf_backtester_db;

-- นับจำนวน ETF
SELECT COUNT(*) FROM etf_backtester_db.ETF_Master;

-- ดู ETF แยกตามประเภท
SELECT Asset_Type, COUNT(*)
FROM etf_backtester_db.ETF_Master
GROUP BY Asset_Type;

-- ดูข้อมูล ETF ทั้งหมด
SELECT * FROM etf_backtester_db.ETF_Master;
```

---

## หมายเหตุสำคัญ

⚠️ **ชื่อ Database ที่ใช้คือ `etf_backtester_db` เท่านั้น**

- ไม่ใช่ `etf_backtest`
- ไม่ใช่ `etf_backtester`
- ไม่ใช่ `etf_db`
- ต้องเป็น **`etf_backtester_db`** เท่านั้น!

---

## ไฟล์ที่เกี่ยวข้อง

ทุกไฟล์ด้านล่างใช้ชื่อ database เดียวกัน: **`etf_backtester_db`**

```
database/
├── setup_complete.sql           ← ใช้ etf_backtester_db ✅
├── schema/
│   └── 01_create_schema.sql     ← ใช้ etf_backtester_db ✅
├── data/
│   └── 02_load_etf_master.sql   ← ใช้ etf_backtester_db ✅
├── diagnose.sql                 ← ใช้ etf_backtester_db ✅
├── verify.sql                   ← ใช้ etf_backtester_db ✅
└── example_connection.py        ← ใช้ etf_backtester_db ✅
```

**ทุกไฟล์พร้อมใช้งานแล้ว ไม่ต้องแก้ไขอะไร!** ✅
