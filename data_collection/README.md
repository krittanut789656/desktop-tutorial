# ETF Data Collection Script

Python script สำหรับดึงข้อมูลราคาย้อนหลังของ ETF จาก Yahoo Finance และบันทึกลง MySQL database

## 🎯 Features

- ✅ ดึงข้อมูลราคารายวันของ ETF 47 ตัวจาก yfinance
- ✅ บันทึกข้อมูลลง MySQL database (ตาราง `daily_prices`)
- ✅ ตรวจสอบความสมบูรณ์ของข้อมูล (missing data, duplicates)
- ✅ สร้าง log file (`data_import.log`) พร้อม timestamp
- ✅ แสดง progress bar ขณะดึงข้อมูล
- ✅ มี function สำหรับ update ข้อมูลเพิ่มเติมในภายหลัง
- ✅ สร้าง summary report (`data_summary.txt`)
- ✅ จัดการ rate limiting เพื่อไม่ให้ถูก block จาก API
- ✅ รองรับ batch processing และ error handling

## 📋 ETF ที่รองรับ (47 ตัว)

### US Large Cap (5 ETFs)
- SPY, VOO, IVV, VTI, QQQ

### US Small/Mid Cap (5 ETFs)
- IWM, IJH, MDY, VB, VO

### International Developed (5 ETFs)
- EFA, VEA, IEFA, VGK, EWJ

### Emerging Markets (5 ETFs)
- EEM, VWO, IEMG, EWZ, FXI

### Bonds (6 ETFs)
- AGG, BND, LQD, TLT, IEF, SHY

### Commodities (5 ETFs)
- GLD, SLV, DBC, USO, PDBC

### Real Estate (3 ETFs)
- VNQ, IYR, XLRE

### Sectors (9 ETFs)
- XLF, XLE, XLK, XLV, XLY, XLP, XLU, XLI, XLB

## 🚀 การติดตั้ง

### ความต้องการของระบบ

- Python 3.8 หรือสูงกว่า
- MySQL 8.0+ (ติดตั้งและรัน database จาก Phase 1)
- pip (Python package manager)

### ขั้นตอนการติดตั้ง

#### 1. ติดตั้ง Dependencies

```bash
cd data_collection
pip install -r requirements.txt
```

#### 2. ตั้งค่า Database Connection

แก้ไขไฟล์ `config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',    # เปลี่ยนเป็น username ของคุณ
    'password': 'your_mysql_password', # เปลี่ยนเป็น password ของคุณ
    'database': 'etf_backtesting',
    'port': 3306
}
```

#### 3. สร้าง Database (ถ้ายังไม่ได้สร้าง)

```bash
cd ../database
mysql -u root -p < 01_create_database.sql
mysql -u root -p < 02_insert_sample_etfs.sql
```

## 📖 วิธีใช้งาน

### Mode 1: Full Data Collection (แนะนำสำหรับครั้งแรก)

ดึงข้อมูลย้อนหลังตั้งแต่ 2009-01-01 ถึงปัจจุบัน

```bash
python data_collection.py
# เลือก option 1: Full data collection
```

**คำเตือน**: การดึงข้อมูลครั้งแรกอาจใช้เวลา 15-30 นาที ขึ้นอยู่กับความเร็วอินเทอร์เน็ต

### Mode 2: Update Existing Data

อัพเดทข้อมูลล่าสุดเท่านั้น (เร็วกว่า)

```bash
python data_collection.py
# เลือก option 2: Update existing data
```

### Mode 3: Custom Ticker List

ดึงข้อมูลเฉพาะ ETF ที่ต้องการ

```bash
python data_collection.py
# เลือก option 3: Custom ticker list
# ใส่ tickers: SPY,QQQ,VOO
```

### การใช้งานแบบ Python Script

```python
from data_collection import ETFDataCollector

# สร้าง collector instance
collector = ETFDataCollector()

# ดึงข้อมูลทั้งหมด
collector.collect_all_data()

# สร้าง summary report
collector.generate_summary_report()

# หรืออัพเดทข้อมูลเฉพาะบาง ticker
collector.update_data(tickers=['SPY', 'QQQ', 'VOO'])
```

## 📁 โครงสร้างไฟล์

```
data_collection/
├── data_collection.py      # Main script
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # Documentation (ไฟล์นี้)
├── data_import.log        # Log file (สร้างอัตโนมัติ)
└── data_summary.txt       # Summary report (สร้างอัตโนมัติ)
```

## ⚙️ Configuration Options

แก้ไขไฟล์ `config.py` เพื่อปรับแต่งการทำงาน:

### Database Settings
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'etf_backtesting',
    'port': 3306
}
```

### Date Range
```python
DATA_START_DATE = '2009-01-01'  # วันที่เริ่มต้น
DATA_END_DATE = '2025-12-31'    # วันที่สิ้นสุด
```

### Rate Limiting
```python
DELAY_BETWEEN_REQUESTS = 1.0    # หน่วงเวลาระหว่าง request (วินาที)
BATCH_SIZE = 5                  # จำนวน ticker ต่อ batch
BATCH_DELAY = 5.0               # หน่วงเวลาหลังแต่ละ batch (วินาที)
```

### Data Validation
```python
MIN_REQUIRED_DAYS = 100         # จำนวนวันขั้นต่ำที่ต้องการ
MAX_MISSING_PERCENTAGE = 20     # % ข้อมูลหายสูงสุดที่ยอมรับได้
```

## 📊 Output Files

### 1. data_import.log

Log file แสดงรายละเอียดการทำงานทั้งหมด:

```
2024-01-15 10:30:45 - INFO - ETF Data Collection Started
2024-01-15 10:30:46 - INFO - Successfully connected to database: etf_backtesting
2024-01-15 10:30:47 - INFO - Fetching data for SPY...
2024-01-15 10:30:52 - INFO - Successfully fetched 3847 records for SPY
2024-01-15 10:30:53 - INFO - Inserted 3847 records, skipped 0 duplicates for SPY
...
```

### 2. data_summary.txt

Summary report แสดงสถิติโดยรวม:

```
================================================================================
ETF DATA COLLECTION SUMMARY REPORT
================================================================================
Generated: 2024-01-15 11:05:23

OVERALL STATISTICS
--------------------------------------------------------------------------------
Total ETFs Processed: 47
Successful: 45
Failed: 2
Success Rate: 95.74%
Total Records Inserted: 156,432
Duplicate Records Skipped: 0

DETAILED TICKER STATISTICS
--------------------------------------------------------------------------------
Ticker     Status       Records      Date Range                     Valid
--------------------------------------------------------------------------------
SPY        success      3847         2009-01-02 to 2024-01-12      Yes
VOO        success      3456         2010-09-09 to 2024-01-12      Yes
...
```

## 🔍 ตัวอย่างผลลัพธ์

### Console Output

```
================================================================================
ETF DATA COLLECTION SCRIPT
================================================================================

Options:
1. Full data collection (2009 - 2025)
2. Update existing data (fetch recent data only)
3. Custom ticker list
4. Exit

Enter your choice (1-4): 1

Starting full data collection...
2024-01-15 10:30:45 - INFO - Successfully connected to database: etf_backtesting
2024-01-15 10:30:46 - INFO - Starting data collection for 47 ETFs

Processing SPY: 100%|████████████████████████| 47/47 [15:23<00:00, 19.64s/ETF]

2024-01-15 10:46:09 - INFO - Data collection completed
2024-01-15 10:46:10 - INFO - Generating summary report...
2024-01-15 10:46:10 - INFO - Summary report saved to data_summary.txt

================================================================================
DATA COLLECTION COMPLETED
================================================================================
Log file: data_import.log
Summary report: data_summary.txt
================================================================================
```

### Database Records

ตรวจสอบข้อมูลในฐานข้อมูล:

```sql
-- ดูจำนวน records ทั้งหมด
SELECT COUNT(*) FROM daily_prices;
-- ผลลัพธ์: 156,432

-- ดูจำนวน records แต่ละ ETF
SELECT ticker, COUNT(*) as records, MIN(date) as first_date, MAX(date) as last_date
FROM daily_prices
GROUP BY ticker
ORDER BY ticker;
```

## 🛠️ Troubleshooting

### ปัญหา: ไม่สามารถเชื่อมต่อ Database

**แก้ไข**:
1. ตรวจสอบว่า MySQL service กำลังทำงาน
2. ตรวจสอบ username/password ใน `config.py`
3. ตรวจสอบว่าสร้าง database แล้ว: `mysql -u root -p -e "SHOW DATABASES;"`

### ปัญหา: Ticker not found in etfs table

**แก้ไข**:
1. รัน script insert ETF ข้อมูลก่อน: `mysql -u root -p < ../database/02_insert_sample_etfs.sql`
2. หรือเพิ่ม ticker ใหม่ด้วยตัวเอง:
```sql
INSERT INTO etfs (ticker, name, asset_class, expense_ratio, inception_date)
VALUES ('TICKER', 'ETF Name', 'Asset Class', 0.10, '2000-01-01');
```

### ปัญหา: Rate limiting / Too many requests

**แก้ไข**:
1. เพิ่มค่า `DELAY_BETWEEN_REQUESTS` ใน `config.py`
2. ลด `BATCH_SIZE` ลง
3. เพิ่ม `BATCH_DELAY`

### ปัญหา: No data available for ticker

**สาเหตุ**:
- ETF inception date หลัง start date ที่กำหนด
- Ticker delisted หรือไม่มีข้อมูลใน Yahoo Finance
- Ticker symbol ผิด

**แก้ไข**:
1. ตรวจสอบ ticker symbol ว่าถูกต้อง
2. ลองค้นหาใน Yahoo Finance: https://finance.yahoo.com/
3. ปรับ start date ให้ใหม่กว่า inception date

### ปัญหา: ImportError / ModuleNotFoundError

**แก้ไข**:
```bash
pip install -r requirements.txt --upgrade
```

## 📈 Performance Tips

### 1. เพิ่มความเร็วการดึงข้อมูล

```python
# ใน config.py
DELAY_BETWEEN_REQUESTS = 0.5  # ลดเวลาหน่วง (ระวังถูก rate limit)
```

### 2. ดึงเฉพาะข้อมูลที่ต้องการ

```python
# ใช้ custom ticker list แทนดึงทั้งหมด
collector.collect_all_data(tickers=['SPY', 'QQQ', 'VOO'])
```

### 3. Update แทน Full Collection

```python
# ใช้ update mode สำหรับดึงข้อมูลล่าสุดเท่านั้น
collector.update_data()
```

## 🔒 Security Best Practices

1. **ไม่ควร hardcode password**: ใช้ environment variables แทน

```python
import os
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'etf_backtesting'),
}
```

2. **สร้าง MySQL user แยก**: อย่าใช้ root

```sql
CREATE USER 'etf_collector'@'localhost' IDENTIFIED BY 'secure_password';
GRANT INSERT, SELECT ON etf_backtesting.daily_prices TO 'etf_collector'@'localhost';
GRANT SELECT ON etf_backtesting.etfs TO 'etf_collector'@'localhost';
FLUSH PRIVILEGES;
```

3. **Backup ก่อนรันครั้งแรก**

```bash
mysqldump -u root -p etf_backtesting > backup_before_import.sql
```

## 📅 Scheduled Updates (Cron Job)

ตั้งค่า auto-update ข้อมูลทุกวัน:

### Linux/Mac
```bash
# เปิด crontab
crontab -e

# เพิ่มบรรทัดนี้ (รันทุกวันเวลา 18:00)
0 18 * * * cd /path/to/data_collection && /usr/bin/python3 data_collection.py << EOF
2
EOF
```

### Windows Task Scheduler
1. เปิด Task Scheduler
2. Create Basic Task
3. Schedule: Daily at 6:00 PM
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `data_collection.py`
7. Start in: `C:\path\to\data_collection`

## 🧪 Testing

ทดสอบ script ด้วย ticker น้อยๆ ก่อน:

```bash
python data_collection.py
# เลือก option 3
# ใส่: SPY,VOO
```

## 📚 Additional Resources

- yfinance Documentation: https://github.com/ranaroussi/yfinance
- MySQL Python Connector: https://dev.mysql.com/doc/connector-python/en/
- pandas Documentation: https://pandas.pydata.org/docs/

## 🤝 Support

หากพบปัญหาหรือมีคำถาม:
1. ตรวจสอบ `data_import.log` file
2. อ่าน Troubleshooting section
3. ตรวจสอบว่ารัน database scripts ครบแล้ว

## 📝 Change Log

### Version 1.0.0 (2024-01-15)
- Initial release
- รองรับ 47 ETFs
- Full data collection และ update mode
- Data validation และ quality checks
- Comprehensive logging และ reporting

---

**License**: MIT
**Version**: 1.0.0
**Last Updated**: 2024-01-15
