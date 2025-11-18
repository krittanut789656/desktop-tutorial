# Portfolio Backtesting System - MySQL to Excel Exporter

เครื่องมือสำหรับ export ข้อมูลจาก MySQL Database (Portfolio Backtesting System) ออกมาเป็นไฟล์ Excel

## 📦 ไฟล์ในโปรเจกต์

- **mysql_to_excel.py** - โปรแกรม Python สำหรับ export ข้อมูล
- **database_setup.sql** - SQL Script สำหรับสร้าง database และ tables
- **requirements.txt** - Dependencies ที่ต้องติดตั้ง
- **.env.example** - ตัวอย่างไฟล์ configuration
- **USAGE_TH.md** - คู่มือการใช้งานภาษาไทยแบบละเอียด

## 🚀 Quick Start

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. สร้าง Database (ถ้ายังไม่ได้สร้าง)

```bash
mysql -u root -p < database_setup.sql
```

### 3. ตั้งค่า Database Connection

```bash
cp .env.example .env
# แก้ไขไฟล์ .env ด้วยข้อมูลของคุณ
```

### 4. รันโปรแกรม

```bash
python mysql_to_excel.py
```

## 📊 ผลลัพธ์

โปรแกรมจะสร้างไฟล์ Excel ที่มี 10 sheets:
- etf_master
- price_history
- benchmark_portfolios
- benchmark_holdings
- backtest_scenarios
- scenario_holdings
- backtest_results
- portfolio_snapshots
- transaction_log
- _Summary (สรุปจำนวนข้อมูล)

## 📖 คู่มือการใช้งาน

ดูรายละเอียดเพิ่มเติมได้ที่ [USAGE_TH.md](USAGE_TH.md)

## 🛠️ Requirements

- Python 3.8+
- MySQL Server
- Libraries: mysql-connector-python, pandas, openpyxl

## 📝 License

MIT License
