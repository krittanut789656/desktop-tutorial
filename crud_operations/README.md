# CRUD Operations Module

Python module สำหรับจัดการ CRUD operations ของระบบ ETF Portfolio Backtesting

## 🎯 Overview

Module นี้ให้บริการ CRUD (Create, Read, Update, Delete) operations ที่ครบถ้วนสำหรับ:

1. **Portfolio Management** - สร้าง แก้ไข อ่าน และลบ portfolio พร้อม asset allocation
2. **ETF Management** - จัดการข้อมูล ETF และราคาย้อนหลัง
3. **Backtest Management** - จัดการประวัติและผลลัพธ์การ backtest

##  Features

✅ **Comprehensive Error Handling** - จัดการ errors ทุกประเภทอย่างละเอียด
✅ **Input Validation** - ตรวจสอบความถูกต้องของ weights, dates, ticker symbols
✅ **Logging** - บันทึก log ทุก operation ลง `crud_operations.log`
✅ **Type Hints** - ใช้ type hints สำหรับ parameters และ return values
✅ **Docstrings** - เอกสารครบถ้วนทุก function
✅ **Transaction Management** - ใช้ context manager สำหรับ database connections
✅ **MySQL Support** - ออกแบบสำหรับ MySQL โดยเฉพาะ

## 📋 Requirements

- Python 3.8+
- MySQL 8.0+
- MySQL database จาก Phase 1 (ต้องรัน database scripts แล้ว)

## 🚀 Installation

### 1. Install Dependencies

```bash
cd crud_operations
pip install -r requirements.txt
```

### 2. Configure Database Connection

แก้ไขไฟล์ `crud_operations.py` บรรทัดที่ 23-29:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # เปลี่ยนเป็น MySQL username ของคุณ
    'password': 'your_password',  # เปลี่ยนเป็น MySQL password ของคุณ
    'database': 'etf_backtesting',
    'port': 3306
}
```

**หมายเหตุ**: สำหรับความปลอดภัย ควรใช้ environment variables แทน hardcode password

### 3. Verify Database Setup

ตรวจสอบว่า database พร้อมใช้งาน:

```bash
mysql -u root -p -e "USE etf_backtesting; SHOW TABLES;"
```

ควรเห็น tables ทั้งหมด 8 ตาราง

## 📖 Usage

### Import Module

```python
from crud_operations import (
    # Portfolio functions
    create_portfolio,
    read_portfolio,
    update_portfolio_weights,
    delete_portfolio,

    # ETF functions
    add_etf,
    get_etf_info,
    update_etf_prices,
    delete_etf,

    # Backtest functions
    list_backtests,
    delete_backtest,

    # Utility
    get_database_stats
)
```

### Portfolio Management

#### สร้าง Portfolio ใหม่

```python
result = create_portfolio(
    name="Balanced Portfolio",
    description="60% stocks, 40% bonds",
    etf_list=["SPY", "AGG"],
    weights=[60.0, 40.0],
    user_id=1
)

if result['success']:
    portfolio_id = result['portfolio_id']
    print(f"Created portfolio ID: {portfolio_id}")
else:
    print(f"Error: {result['message']}")
```

#### อ่านข้อมูล Portfolio

```python
# อ่าน portfolio เดียว
result = read_portfolio(portfolio_id=1)

# อ่าน portfolios ทั้งหมด
result = read_portfolio()

if result['success']:
    for portfolio in result['data']:
        print(f"Portfolio: {portfolio['name']}")
        print(f"Holdings: {portfolio['num_holdings']}")
        for allocation in portfolio['allocations']:
            print(f"  {allocation['ticker']}: {allocation['weight']}%")
```

#### แก้ไขน้ำหนัก Portfolio

```python
result = update_portfolio_weights(
    portfolio_id=1,
    etf_list=["SPY", "AGG", "GLD"],
    weights=[50.0, 30.0, 20.0]
)

if result['success']:
    print("Portfolio updated successfully")
```

#### ลบ Portfolio

```python
# จะถามยืนยันก่อนลบ
result = delete_portfolio(portfolio_id=1, confirm=True)

# ลบทันทีไม่ต้องถาม
result = delete_portfolio(portfolio_id=1, confirm=False)
```

### ETF Management

#### เพิ่ม ETF ใหม่

```python
result = add_etf(
    ticker="VTI",
    name="Vanguard Total Stock Market ETF",
    asset_class="US Total Market Equity",
    expense_ratio=0.03,
    inception_date="2001-05-24",
    description="Covers the entire US stock market"
)
```

#### ดูข้อมูล ETF

```python
# ดู ETF เดียว
result = get_etf_info(ticker="SPY")

# ดู ETFs ทั้งหมด
result = get_etf_info()

if result['success']:
    for etf in result['data']:
        print(f"{etf['ticker']}: {etf['name']}")
        print(f"  Price records: {etf['price_count']}")
        print(f"  Date range: {etf['first_price_date']} to {etf['last_price_date']}")
```

#### อัพเดทราคา ETF

```python
# อัพเดทตั้งแต่วันที่ระบุ
result = update_etf_prices(ticker="SPY", start_date="2024-01-01")

# อัพเดทจากวันล่าสุดใน database (auto-detect)
result = update_etf_prices(ticker="SPY")

if result['success']:
    print(f"Added {result['records_added']} new price records")
```

#### ลบ ETF

```python
# จะถามยืนยันก่อนลบ
result = delete_etf(ticker="TEST", confirm=True)

# หมายเหตุ: จะลบไม่ได้ถ้า ETF ถูกใช้ใน portfolio อยู่
```

### Backtest Management

#### แสดงรายการ Backtests

```python
# แสดงทั้งหมด
result = list_backtests()

# แสดงเฉพาะ portfolio หนึ่ง
result = list_backtests(portfolio_id=1)

if result['success']:
    for bt in result['data']:
        print(f"Backtest {bt['backtest_id']}")
        print(f"  Portfolio: {bt['portfolio_name']}")
        print(f"  Strategy: {bt['strategy_type']}")
        print(f"  Results: {bt['result_count']} records")
```

#### ลบ Backtest

```python
result = delete_backtest(backtest_id=1)

if result['success']:
    print(result['message'])
```

### Utility Functions

#### ดู Database Statistics

```python
result = get_database_stats()

if result['success']:
    for table, count in result['data'].items():
        print(f"{table}: {count} records")
```

## 🧪 Testing

รัน test script เพื่อทดสอบ functions ทั้งหมด:

```bash
python test_crud.py
```

Test script จะทดสอบ:
- ✅ Portfolio CRUD operations
- ✅ ETF CRUD operations
- ✅ Backtest operations
- ✅ Input validation
- ✅ Error handling
- ✅ Database statistics

**หมายเหตุ**: Operations ที่เป็น destructive (delete) จะถูก comment ไว้โดย default

## 📊 Return Values

ทุก function จะ return dictionary ที่มีโครงสร้างดังนี้:

### Success Response

```python
{
    'success': True,
    'data': [...],  # หรือ 'portfolio_id', 'records_added' ขึ้นกับ function
    'message': 'Operation completed successfully'
}
```

### Error Response

```python
{
    'success': False,
    'data': [],  # หรือ None
    'message': 'Error description here'
}
```

## ⚠️ Input Validation

Module มี validation ที่เข้มงวดสำหรับ:

### Portfolio Weights
- ✅ ต้องรวมเป็น 100% (tolerance ±0.01%)
- ✅ ทุกค่าต้อง ≥ 0
- ✅ จำนวน weights ต้องเท่ากับจำนวน ETFs
- ❌ ไม่อนุญาตให้ ticker ซ้ำกัน

### Ticker Symbols
- ✅ ความยาว 1-10 ตัวอักษร
- ✅ ตัวพิมพ์ใหญ่เท่านั้น (จะแปลงอัตโนมัติ)
- ✅ ตัวอักษรและตัวเลขเท่านั้น

### Dates
- ✅ รูปแบบ: YYYY-MM-DD
- ✅ ต้องเป็นวันที่ที่ถูกต้อง

### Expense Ratios
- ✅ ต้องอยู่ระหว่าง 0-100%

## 📝 Logging

ทุก operation จะถูก log ลงไฟล์ `crud_operations.log`:

```
2024-01-15 10:30:45 - INFO - create_portfolio - Creating portfolio: My Portfolio
2024-01-15 10:30:46 - INFO - create_portfolio - Portfolio created successfully with ID: 1
2024-01-15 10:31:20 - ERROR - delete_etf - ETF SPY is used in 5 portfolio(s)
```

Log format:
```
timestamp - level - function_name - message
```

## 🔒 Security Best Practices

### 1. ใช้ Environment Variables

แทนที่จะ hardcode password:

```python
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'etf_backtesting'),
}
```

### 2. สร้าง MySQL User แยก

```sql
CREATE USER 'etf_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON etf_backtesting.* TO 'etf_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Backup ก่อนใช้งาน

```bash
mysqldump -u root -p etf_backtesting > backup_$(date +%Y%m%d).sql
```

## 🔧 Advanced Usage

### Custom Transaction Handling

```python
from crud_operations import DatabaseConnection

with DatabaseConnection() as (cursor, conn):
    # ทำ operations หลายอย่างใน transaction เดียว
    cursor.execute("INSERT INTO portfolios (...) VALUES (...)")
    cursor.execute("INSERT INTO portfolio_allocations (...) VALUES (...)")
    conn.commit()
```

### Batch Operations

```python
# สร้าง portfolios หลายอันพร้อมกัน
portfolios = [
    ("Portfolio 1", "Description 1", ["SPY"], [100.0]),
    ("Portfolio 2", "Description 2", ["SPY", "AGG"], [60.0, 40.0]),
    ("Portfolio 3", "Description 3", ["SPY", "AGG", "GLD"], [50.0, 30.0, 20.0])
]

for name, desc, etfs, weights in portfolios:
    result = create_portfolio(name, desc, etfs, weights)
    if result['success']:
        print(f"Created: {name} (ID: {result['portfolio_id']})")
    else:
        print(f"Failed: {name} - {result['message']}")
```

## 🐛 Troubleshooting

### Error: "Can't connect to MySQL server"

**สาเหตุ**: MySQL service ไม่ทำงาน หรือ config ผิด

**แก้ไข**:
```bash
# ตรวจสอบ MySQL service
sudo systemctl status mysql

# เริ่ม MySQL
sudo systemctl start mysql

# ทดสอบ connection
mysql -u root -p -e "SELECT VERSION();"
```

### Error: "Portfolio weights must sum to 100%"

**สาเหตุ**: น้ำหนักรวมไม่ได้ 100

**แก้ไข**:
```python
# ผิด
weights = [60.0, 40.1]  # รวม 100.1

# ถูก
weights = [60.0, 40.0]  # รวม 100.0
```

### Error: "ETF not found in database"

**สาเหตุ**: ยังไม่มี ETF ในฐานข้อมูล

**แก้ไข**:
```bash
# รัน script insert ETFs
mysql -u root -p < ../database/02_insert_sample_etfs.sql

# หรือเพิ่มด้วย add_etf()
```

### Error: "Cannot delete ETF. It is used in portfolios"

**สาเหตุ**: ETF ถูกใช้อยู่ใน portfolio

**แก้ไข**:
1. ลบหรือแก้ไข portfolios ที่ใช้ ETF นั้นก่อน
2. หรือ update portfolio weights ให้ไม่มี ETF นั้น

## 📚 API Reference

### Portfolio Functions

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `create_portfolio()` | name, description, etf_list, weights, user_id | Dict with portfolio_id | สร้าง portfolio ใหม่ |
| `read_portfolio()` | portfolio_id (optional) | Dict with data list | อ่านข้อมูล portfolio |
| `update_portfolio_weights()` | portfolio_id, etf_list, weights | Dict with success status | แก้ไขน้ำหนัก |
| `delete_portfolio()` | portfolio_id, confirm | Dict with success status | ลบ portfolio |

### ETF Functions

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `add_etf()` | ticker, name, asset_class, expense_ratio, inception_date, description | Dict with success status | เพิ่ม ETF |
| `get_etf_info()` | ticker (optional) | Dict with data list | อ่านข้อมูล ETF |
| `update_etf_prices()` | ticker, start_date, end_date | Dict with records_added | อัพเดทราคา |
| `delete_etf()` | ticker, confirm | Dict with success status | ลบ ETF |

### Backtest Functions

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `list_backtests()` | portfolio_id (optional) | Dict with data list | แสดงรายการ backtests |
| `delete_backtest()` | backtest_id | Dict with success status | ลบ backtest |

### Utility Functions

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `get_database_stats()` | None | Dict with stats | ดูสถิติ database |

## 📄 Files

```
crud_operations/
├── crud_operations.py      # Main CRUD module (1300+ lines)
├── test_crud.py            # Test script
├── requirements.txt        # Python dependencies
├── README.md              # Documentation (this file)
├── .gitignore             # Git ignore rules
└── crud_operations.log    # Log file (created automatically)
```

## 🔄 Version History

### Version 1.0.0 (2024-01-15)
- Initial release
- Portfolio CRUD operations
- ETF CRUD operations
- Backtest management
- Comprehensive validation and error handling
- MySQL support

## 📞 Support

ติดปัญหาหรือมีคำถาม:
1. ตรวจสอบ `crud_operations.log`
2. อ่าน Troubleshooting section
3. รัน `test_crud.py` เพื่อทดสอบระบบ

## 📖 Related Documentation

- [Database Schema](../database/ER_Diagram.md)
- [Data Collection](../data_collection/README.md)
- MySQL Documentation: https://dev.mysql.com/doc/

---

**License**: MIT
**Version**: 1.0.0
**Last Updated**: 2024-01-15
