# คู่มือการใช้ Jupyter Notebook กับ ETF Portfolio Backtester

## 📋 Overview

โปรเจกต์นี้ออกแบบมาให้รันผ่าน Command Line (`python main.py`) แต่คุณสามารถใช้ Jupyter Notebook ได้ โดยมีวิธีการดังนี้

---

## 📁 ขั้นตอนที่ 1: ดาวน์โหลดไฟล์มาไว้บนเครื่อง

### วิธีที่ 1: ดาวน์โหลดจาก Git Repository

```bash
# Clone repository
git clone <your-repository-url>
cd desktop-tutorial/etf_backtester
```

### วิธีที่ 2: คัดลอกไฟล์ทั้งโฟลเดอร์

คัดลอกโฟลเดอร์ `etf_backtester` ทั้งหมดมาไว้บนเครื่อง เช่น:
```
C:\Users\YourName\Documents\etf_backtester\
```

หรือ (Mac/Linux):
```
/Users/YourName/Documents/etf_backtester/
```

---

## 📂 โครงสร้างไฟล์ที่ต้องมี

ตรวจสอบว่ามีไฟล์ครบตามนี้:

```
etf_backtester/
├── main.py                         # Main program
├── requirements.txt                # Dependencies
├── modules/
│   ├── __init__.py                 # ทำให้เป็น Python package
│   ├── db_connector.py             # Database connection
│   ├── data_loader.py              # Yahoo Finance loader
│   ├── backtest_engine.py          # Backtesting logic
│   ├── analytics.py                # SQL analytics
│   ├── crud_operations.py          # CRUD operations
│   └── text_logger.py              # Text file logging
├── sql/
│   ├── database.sql                # Database schema
│   ├── etf_master_data.sql         # 50 ETFs
│   └── price_data_*.sql            # Price data (ถ้ามี)
├── logs/                           # จะถูกสร้างอัตโนมัติ
└── data/                           # จะถูกสร้างอัตโนมัติ
```

---

## 🔧 ขั้นตอนที่ 2: Install Dependencies

เปิด Terminal หรือ Anaconda Prompt แล้วรัน:

```bash
# ไปที่โฟลเดอร์โปรเจกต์
cd C:\Users\YourName\Documents\etf_backtester

# Install packages
pip install -r requirements.txt

# Install Jupyter Notebook (ถ้ายังไม่มี)
pip install jupyter notebook
```

**หรือถ้าใช้ Anaconda:**
```bash
conda install mysql-connector-python pandas numpy yfinance openpyxl
conda install jupyter notebook
```

---

## 📊 ขั้นตอนที่ 3: ตั้งค่า MySQL Database

ก่อนใช้ Jupyter Notebook ต้องมี MySQL Database พร้อมข้อมูลก่อน:

```bash
# สร้าง database และโหลดข้อมูล
mysql -u root -p < sql/database.sql
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/price_data_20251120_072559.sql
```

---

## 📓 ขั้นตอนที่ 4: สร้าง Jupyter Notebook

### 4.1 เปิด Jupyter Notebook

```bash
cd C:\Users\YourName\Documents\etf_backtester
jupyter notebook
```

Browser จะเปิดขึ้นมาอัตโนมัติ

---

### 4.2 สร้าง Notebook ใหม่

1. คลิก **New** → **Python 3**
2. ตั้งชื่อ Notebook เป็น `ETF_Backtester_Demo.ipynb`
3. บันทึกไว้ในโฟลเดอร์ `etf_backtester/`

---

## 💻 วิธีการใช้งานใน Jupyter Notebook

### ตัวอย่างที่ 1: Import Modules และเชื่อมต่อ Database

```python
# Cell 1: Import libraries และ modules
import sys
import os
from datetime import datetime, timedelta

# เพิ่ม path ของโปรเจกต์เข้าไปใน sys.path
# ถ้า Notebook อยู่ในโฟลเดอร์ etf_backtester/ แล้ว ไม่ต้องเพิ่ม
# sys.path.append('/path/to/etf_backtester')

# Import modules จากโปรเจกต์
from modules.db_connector import DatabaseConnector
from modules.data_loader import DataLoader
from modules.backtest_engine import BacktestEngine
from modules.analytics import Analytics
from modules.crud_operations import CRUDOperations
from modules.text_logger import TextLogger

print("✓ All modules imported successfully!")
```

---

```python
# Cell 2: เชื่อมต่อ Database
db = DatabaseConnector()

# ทดสอบการเชื่อมต่อ
if db.test_connection():
    print("✓ Database connected successfully!")

    # ดูจำนวนข้อมูล
    etf_count = db.get_table_count('ETF_Master')
    price_count = db.get_table_count('Price_Data')

    print(f"✓ ETF_Master: {etf_count} ETFs")
    print(f"✓ Price_Data: {price_count:,} records")
else:
    print("✗ Cannot connect to database")
```

---

### ตัวอย่างที่ 2: ดูข้อมูล ETF ทั้งหมด

```python
# Cell 3: แสดง ETF ทั้งหมด
import pandas as pd

query = """
SELECT
    ETF_ID,
    Ticker_Symbol,
    ETF_Name,
    Asset_Type,
    Expense_Ratio
FROM ETF_Master
ORDER BY Asset_Type, Ticker_Symbol
"""

results = db.execute_query_dict(query)
df_etfs = pd.DataFrame(results)

print(f"Total ETFs: {len(df_etfs)}\n")
print(df_etfs.head(10))

# แสดงจำนวนตาม Asset Type
print("\nETF Count by Asset Type:")
print(df_etfs.groupby('Asset_Type').size())
```

---

### ตัวอย่างที่ 3: ดูราคาล่าสุดของ SPY

```python
# Cell 4: ดูราคา SPY ล่าสุด 10 สัปดาห์
query = """
SELECT
    pd.Price_Date,
    pd.Open_Price,
    pd.High_Price,
    pd.Low_Price,
    pd.Close_Price,
    pd.Volume,
    em.Ticker_Symbol
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE em.Ticker_Symbol = 'SPY'
ORDER BY pd.Price_Date DESC
LIMIT 10
"""

results = db.execute_query_dict(query)
df_spy = pd.DataFrame(results)

print("SPY - Latest 10 Weeks:")
print(df_spy)

# Plot ราคา
import matplotlib.pyplot as plt

df_spy_sorted = df_spy.sort_values('Price_Date')
plt.figure(figsize=(12, 6))
plt.plot(df_spy_sorted['Price_Date'], df_spy_sorted['Close_Price'], marker='o')
plt.title('SPY - Close Price (Last 10 Weeks)')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

---

### ตัวอย่างที่ 4: รัน Backtest

```python
# Cell 5: รัน Standard Backtest
backtest = BacktestEngine(db)

# กำหนดพารามิเตอร์
selection_date = datetime.now()
lookback_days = 90
top_n = 5
holding_days = 30

print(f"Running backtest...")
print(f"Selection Date: {selection_date.date()}")
print(f"Lookback Period: {lookback_days} days")
print(f"Top N ETFs: {top_n}")
print(f"Holding Period: {holding_days} days")
print("=" * 60)

# รัน backtest
results = backtest.run_backtest(
    selection_date=selection_date,
    lookback_days=lookback_days,
    top_n=top_n,
    holding_days=holding_days
)

# แสดงผลลัพธ์
if results:
    print("\n✓ Backtest completed!")
    print(f"Backtest Run ID: {results['backtest_run_id']}")
    print(f"\nTop {top_n} ETFs Selected:")

    df_results = pd.DataFrame(results['portfolio'])
    print(df_results[['rank', 'ticker', 'etf_name', 'asset_type', 'momentum_score', 'holding_return']])

    print(f"\nPortfolio Return: {results['portfolio_return']:.2f}%")
else:
    print("✗ Backtest failed")
```

---

### ตัวอย่างที่ 5: Generate Analytics

```python
# Cell 6: Volatility Analysis
analytics = Analytics(db)

print("Insight #1: Volatility Analysis by Asset Type")
print("=" * 60)

volatility_df = analytics.get_volatility_analysis()

if not volatility_df.empty:
    print(volatility_df)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(volatility_df['Asset_Type'], volatility_df['Annualized_Volatility'])
    plt.title('Annualized Volatility by Asset Type')
    plt.xlabel('Asset Type')
    plt.ylabel('Volatility')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
else:
    print("No data available")
```

---

```python
# Cell 7: Lookback Period Comparison
print("Insight #2: Lookback Period Optimization")
print("=" * 60)

lookback_df = analytics.get_lookback_comparison()

if not lookback_df.empty:
    print(lookback_df)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(lookback_df['Lookback_Days'], lookback_df['CAGR'], marker='o', linewidth=2)
    plt.title('CAGR by Lookback Period')
    plt.xlabel('Lookback Period (Days)')
    plt.ylabel('CAGR (%)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
else:
    print("No backtest data available. Run some backtests first!")
```

---

### ตัวอย่างที่ 6: CRUD Operations

```python
# Cell 8: View Latest Backtest Results (READ)
crud = CRUDOperations(db)

print("Latest Backtest Results:")
print("=" * 60)

results = crud.read_latest_backtest()

if results:
    df = pd.DataFrame(results)
    print(df[['rank', 'ticker', 'momentum_score', 'holding_return']])
else:
    print("No backtest results found")
```

---

```python
# Cell 9: View All ETF Information (READ)
print("All ETFs Information:")
print("=" * 60)

etf_info = crud.read_etf_info()

if etf_info:
    df = pd.DataFrame(etf_info)
    print(f"Total: {len(df)} ETFs\n")
    print(df.groupby('Asset_Type').size())
else:
    print("No ETF data found")
```

---

### ตัวอย่างที่ 7: Export to Excel

```python
# Cell 10: Export to Excel
from export_to_excel import ExcelExporter

exporter = ExcelExporter(db)

print("Exporting data to Excel...")

# Export ETF_Master
etf_file = exporter.export_etf_master()
print(f"✓ ETF_Master exported to: {etf_file}")

# Export Price_Data (first 5000 rows for demo)
price_file = exporter.export_price_data(limit=5000)
print(f"✓ Price_Data exported to: {price_file}")

print("\n✓ Excel export completed!")
```

---

### ตัวอย่างที่ 8: Advanced Analysis with Pandas

```python
# Cell 11: Calculate Returns for All ETFs
query = """
SELECT
    em.Ticker_Symbol,
    em.Asset_Type,
    pd.Price_Date,
    pd.Close_Price
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE pd.Price_Date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
ORDER BY em.Ticker_Symbol, pd.Price_Date
"""

results = db.execute_query_dict(query)
df = pd.DataFrame(results)

# Pivot table
pivot = df.pivot_table(
    index='Price_Date',
    columns='Ticker_Symbol',
    values='Close_Price'
)

# Calculate returns
returns = pivot.pct_change()

# Calculate cumulative returns
cumulative_returns = (1 + returns).cumprod()

# Plot top 5 ETFs
top_5 = ['SPY', 'QQQ', 'AGG', 'GLD', 'TLT']
plt.figure(figsize=(14, 7))

for ticker in top_5:
    if ticker in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[ticker], label=ticker, linewidth=2)

plt.title('Cumulative Returns - Last 1 Year')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Summary statistics
print("\nSummary Statistics (Annualized):")
annual_returns = returns[top_5].mean() * 52
annual_vol = returns[top_5].std() * (52 ** 0.5)

summary = pd.DataFrame({
    'Annual Return': annual_returns,
    'Annual Volatility': annual_vol,
    'Sharpe Ratio': annual_returns / annual_vol
})

print(summary)
```

---

### ตัวอย่างที่ 9: Close Database Connection

```python
# Cell สุดท้าย: ปิด Connection
db.close_pool()
print("✓ Database connection closed")
```

---

## 🎯 Complete Example Notebook

นี่คือตัวอย่าง Notebook แบบสมบูรณ์:

```python
# =============================================================================
# ETF Portfolio Backtester - Jupyter Notebook Demo
# =============================================================================

# ============= CELL 1: Setup =============
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Import project modules
from modules.db_connector import DatabaseConnector
from modules.backtest_engine import BacktestEngine
from modules.analytics import Analytics
from modules.crud_operations import CRUDOperations

print("✓ Modules imported")

# ============= CELL 2: Connect Database =============
db = DatabaseConnector()

if db.test_connection():
    print("✓ Connected to MySQL")
    print(f"  ETF_Master: {db.get_table_count('ETF_Master')} rows")
    print(f"  Price_Data: {db.get_table_count('Price_Data'):,} rows")
else:
    print("✗ Connection failed")

# ============= CELL 3: View ETFs =============
query = "SELECT * FROM ETF_Master ORDER BY Asset_Type, Ticker_Symbol"
df_etfs = pd.DataFrame(db.execute_query_dict(query))
print(f"Total ETFs: {len(df_etfs)}")
print(df_etfs.groupby('Asset_Type').size())

# ============= CELL 4: Run Backtest =============
backtest = BacktestEngine(db)
results = backtest.run_backtest(
    selection_date=datetime.now(),
    lookback_days=90,
    top_n=5,
    holding_days=30
)

if results:
    print(f"✓ Backtest Run ID: {results['backtest_run_id']}")
    df_portfolio = pd.DataFrame(results['portfolio'])
    print(df_portfolio[['ticker', 'momentum_score', 'holding_return']])
    print(f"\nPortfolio Return: {results['portfolio_return']:.2f}%")

# ============= CELL 5: Analytics =============
analytics = Analytics(db)

# Volatility
vol_df = analytics.get_volatility_analysis()
print("\nVolatility by Asset Type:")
print(vol_df)

# Lookback Comparison
lookback_df = analytics.get_lookback_comparison()
print("\nLookback Period Comparison:")
print(lookback_df)

# ============= CELL 6: Visualization =============
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Volatility chart
ax1.bar(vol_df['Asset_Type'], vol_df['Annualized_Volatility'])
ax1.set_title('Volatility by Asset Type')
ax1.set_ylabel('Annualized Volatility')
ax1.grid(axis='y', alpha=0.3)

# Lookback chart
if not lookback_df.empty:
    ax2.plot(lookback_df['Lookback_Days'], lookback_df['CAGR'], marker='o')
    ax2.set_title('CAGR by Lookback Period')
    ax2.set_xlabel('Lookback Days')
    ax2.set_ylabel('CAGR (%)')
    ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============= CELL 7: Close =============
db.close_pool()
print("✓ Database closed")
```

---

## ⚠️ หมายเหตุสำคัญ

### 1. Path ของโปรเจกต์

**ถ้า Notebook อยู่ในโฟลเดอร์ `etf_backtester/`** → ไม่ต้องเพิ่ม path

**ถ้า Notebook อยู่ที่อื่น** → ต้องเพิ่ม:
```python
import sys
sys.path.append('C:/Users/YourName/Documents/etf_backtester')
```

หรือ (Mac/Linux):
```python
import sys
sys.path.append('/Users/YourName/Documents/etf_backtester')
```

---

### 2. MySQL Configuration

ตรวจสอบ config ใน `modules/db_connector.py`:
```python
'host': 'localhost',
'port': 3306,
'database': 'etf_backtester_db',
'user': 'root',
'password': 'password'  # แก้เป็นรหัสผ่านของคุณ
```

---

### 3. Working Directory

ตรวจสอบว่าอยู่ที่ไหน:
```python
import os
print("Current directory:", os.getcwd())
```

ถ้าไม่ใช่โฟลเดอร์โปรเจกต์ ให้เปลี่ยน:
```python
os.chdir('C:/Users/YourName/Documents/etf_backtester')
```

---

## 🎓 สำหรับการ Demo กับอาจารย์

### ข้อดีของการใช้ Jupyter Notebook:

✅ **แสดงผลลัพธ์ได้สวยงาม** - มี tables, charts
✅ **รันทีละส่วนได้** - แสดงให้อาจารย์เห็นทีละขั้นตอน
✅ **Visualization** - Plot graphs ได้สะดวก
✅ **Interactive** - แก้ไขและรันใหม่ได้ทันที

### ข้อเสียของการใช้ Jupyter Notebook:

❌ **ไม่ใช่ CLI ตามโจทย์** - โจทย์ระบุ "Python CLI"
❌ **ต้องรัน cell ตามลำดับ** - ไม่ใช่ menu-driven

---

## 💡 คำแนะนำ

### สำหรับการ Demo:

**แนะนำให้ใช้ `python main.py` เป็นหลัก** เพราะ:
1. ตรงตามโจทย์ที่ระบุ "Python CLI"
2. มี Menu-driven interface ที่เป็นระเบียบ
3. ทำงานครบทุกฟีเจอร์

**ใช้ Jupyter Notebook เป็น Bonus** สำหรับ:
1. แสดง Advanced Analysis พิเศษ
2. Visualization ข้อมูล
3. ตอบคำถามอาจารย์แบบ Interactive

---

## 📚 สรุป

### การใช้ Jupyter Notebook กับโปรเจกต์นี้:

1. ✅ **ดาวน์โหลดไฟล์ทั้งหมด** มาไว้บนเครื่อง
2. ✅ **Install dependencies** (`pip install -r requirements.txt`)
3. ✅ **Setup MySQL Database** และโหลดข้อมูล
4. ✅ **เปิด Jupyter Notebook** ในโฟลเดอร์โปรเจกต์
5. ✅ **Import modules** จาก `modules/`
6. ✅ **รัน code ทีละ cell** ตามตัวอย่างข้างบน

**ใช้ได้ทั้งสองวิธี:**
- **Command Line (`python main.py`)** → เหมาะสำหรับ Demo หลัก
- **Jupyter Notebook** → เหมาะสำหรับ Analysis เพิ่มเติม

---

**มีคำถามเพิ่มเติมถามได้เลยครับ!** 📊✨
