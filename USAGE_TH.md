# คู่มือการใช้งาน MySQL to Excel Exporter

โปรแกรมนี้จะช่วยคุณดึงข้อมูลจาก MySQL Database (Portfolio Backtesting System) ทั้งหมด 9 ตาราง และ export เป็นไฟล์ Excel พร้อม sheet แยกสำหรับแต่ละตาราง

## 📋 ตารางที่จะถูก Export

1. **etf_master** - ข้อมูล ETF หลัก
2. **price_history** - ประวัติราคา
3. **benchmark_portfolios** - พอร์ตมาตรฐาน
4. **benchmark_holdings** - การถือครอง benchmark
5. **backtest_scenarios** - สถานการณ์ทดสอบ
6. **scenario_holdings** - การถือครองในแต่ละสถานการณ์
7. **backtest_results** - ผลการทดสอบ
8. **portfolio_snapshots** - ภาพรวมพอร์ต
9. **transaction_log** - บันทึกธุรกรรม
10. **_Summary** - สรุปจำนวนข้อมูลในแต่ละตาราง (สร้างอัตโนมัติ)

## 🚀 วิธีการติดตั้งและใช้งาน

### ขั้นตอนที่ 1: ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### ขั้นตอนที่ 2: ตั้งค่า Database Configuration

คุณมี 2 วิธีในการตั้งค่า:

#### วิธีที่ 1: ใช้ไฟล์ .env (แนะนำ)

1. Copy ไฟล์ตัวอย่าง:
```bash
cp .env.example .env
```

2. แก้ไขไฟล์ `.env` ด้วยข้อมูลของคุณ:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=portfolio_backtesting
```

#### วิธีที่ 2: แก้ไขค่าใน Script โดยตรง

แก้ไขค่าในไฟล์ `mysql_to_excel.py` บรรทัด 142-147:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'portfolio_backtesting'
}
```

### ขั้นตอนที่ 3: รันโปรแกรม

```bash
python mysql_to_excel.py
```

หรือ

```bash
python3 mysql_to_excel.py
```

## 📊 ผลลัพธ์

โปรแกรมจะสร้างไฟล์ Excel ชื่อ:
```
portfolio_backtesting_export_YYYYMMDD_HHMMSS.xlsx
```

ตัวอย่าง: `portfolio_backtesting_export_20241118_143025.xlsx`

### ตัวอย่าง Output จากโปรแกรม:

```
============================================================
  MySQL to Excel Exporter
  Portfolio Backtesting System
============================================================

🔧 Configuration:
   Host: localhost
   Database: portfolio_backtesting
   User: root

✓ Connected to MySQL database: portfolio_backtesting

📊 Starting export to: portfolio_backtesting_export_20241118_143025.xlsx
============================================================

📋 Exporting etf_master...
  ✓ etf_master: 15 rows

📋 Exporting price_history...
  ✓ price_history: 5420 rows

📋 Exporting benchmark_portfolios...
  ✓ benchmark_portfolios: 3 rows

📋 Exporting benchmark_holdings...
  ✓ benchmark_holdings: 12 rows

📋 Exporting backtest_scenarios...
  ✓ backtest_scenarios: 5 rows

📋 Exporting scenario_holdings...
  ✓ scenario_holdings: 20 rows

📋 Exporting backtest_results...
  ✓ backtest_results: 5 rows

📋 Exporting portfolio_snapshots...
  ✓ portfolio_snapshots: 250 rows

📋 Exporting transaction_log...
  ✓ transaction_log: 180 rows

📋 Creating summary sheet...

============================================================
✓ Export completed successfully!
📁 File saved: /path/to/portfolio_backtesting_export_20241118_143025.xlsx
📊 Total tables exported: 9

✓ MySQL connection closed

✅ Success! Your data has been exported to Excel.
```

## ⚙️ การกำหนดชื่อไฟล์ Output (Optional)

ถ้าต้องการกำหนดชื่อไฟล์เอง สามารถเพิ่มในไฟล์ `.env`:
```
OUTPUT_FILE=my_portfolio_data.xlsx
```

หรือใช้ environment variable:
```bash
OUTPUT_FILE=my_data.xlsx python mysql_to_excel.py
```

## 🔧 คุณสมบัติพิเศษ

- ✅ Auto-adjust column width ในไฟล์ Excel
- ✅ สร้าง Summary sheet แสดงจำนวน rows ของแต่ละตาราง
- ✅ แสดง progress ขณะ export
- ✅ Error handling ที่ดี
- ✅ สามารถ export ตารางว่างได้

## 🐛 แก้ปัญหา

### ปัญหา: Connection Error
```
✗ Error connecting to MySQL: Access denied for user
```
**แก้ไข**: ตรวจสอบ username และ password ในไฟล์ `.env`

### ปัญหา: Database not found
```
✗ Error connecting to MySQL: Unknown database 'portfolio_backtesting'
```
**แก้ไข**: ตรวจสอบว่าได้สร้าง database แล้วโดยการรัน SQL script ก่อน

### ปัญหา: Module not found
```
ModuleNotFoundError: No module named 'mysql'
```
**แก้ไข**: รัน `pip install -r requirements.txt`

## 📝 หมายเหตุ

- ตรวจสอบให้แน่ใจว่า MySQL Server กำลังทำงานอยู่
- ต้องมีสิทธิ์ในการ read ข้อมูลจาก database
- Python version ที่แนะนำ: 3.8 หรือสูงกว่า

## 📞 ติดต่อ / รายงานปัญหา

หากพบปัญหาหรือต้องการความช่วยเหลือ กรุณาแจ้งได้เลยครับ
