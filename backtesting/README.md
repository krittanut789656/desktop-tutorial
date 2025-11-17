# Backtesting Engine

Python module สำหรับทดสอบกลยุทธ์การลงทุนย้อนหลัง (Backtesting) ของ ETF Portfolio

## 🎯 Overview

Backtesting Engine ให้บริการทดสอบ 3 กลยุทธ์การลงทุนหลักสำหรับ portfolio:

1. **Buy & Hold** - ซื้อและถือตามน้ำหนักที่กำหนดโดยไม่ปรับเปลี่ยน
2. **Periodic Rebalancing** - ปรับสมดุล portfolio กลับสู่น้ำหนักเป้าหมายตามระยะเวลาที่กำหนด
3. **Dollar Cost Averaging (DCA)** - ลงทุนเพิ่มเติมเป็นงวดๆ ตามจำนวนที่กำหนด

## ✨ Features

✅ **3 Strategies** - รองรับกลยุทธ์การลงทุนทั้ง 3 แบบ
✅ **SQL Optimized** - ใช้ SQL queries และ pandas สำหรับประสิทธิภาพสูง
✅ **Batch Processing** - INSERT ข้อมูลแบบ batch เพื่อความเร็ว
✅ **Progress Bar** - แสดง progress ขณะคำนวณ
✅ **Transaction Costs** - คำนวณค่าธรรมเนียมการซื้อขาย
✅ **Comprehensive Logging** - บันทึก log ทุกขั้นตอน
✅ **Summary Reports** - สร้าง report สรุปผลการทดสอบ
✅ **Results Backup** - สำรองผลลัพธ์เป็น text files
✅ **Error Handling** - จัดการกับกรณีข้อมูลไม่ครบ

## 📋 Requirements

- Python 3.8+
- MySQL 8.0+
- Database จาก Phase 1 (พร้อม price data จาก Phase 2)
- อย่างน้อย 1 portfolio (จาก Phase 3)

## 🚀 Installation

### 1. Install Dependencies

```bash
cd backtesting
pip install -r requirements.txt
```

### 2. Configure Database

แก้ไขใน `backtesting_engine.py` (บรรทัด 24-30):

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'etf_backtesting',
    'port': 3306
}
```

## 📖 Usage

### Basic Usage

```python
from backtesting_engine import run_backtest

# Run a backtest
backtest_id = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=100000.00,
    strategy_type='buy_hold',
    transaction_cost=0.001  # 0.1%
)

print(f"Backtest ID: {backtest_id}")
```

### Strategy 1: Buy & Hold

ซื้อและถือโดยไม่มีการ rebalance

```python
backtest_id = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=100000.00,
    strategy_type='buy_hold',
    transaction_cost=0.001
)
```

**ลักษณะการทำงาน**:
- ซื้อ ETFs ตามน้ำหนักที่กำหนดในวันแรก
- ไม่มีการปรับสมดุล portfolio
- คำนวณมูลค่า portfolio ทุกวันตามราคาตลาด
- เหมาะสำหรับผู้ลงทุนระยะยาว passive investor

### Strategy 2: Periodic Rebalancing

ปรับสมดุล portfolio กลับสู่น้ำหนักเป้าหมายตามความถี่

```python
backtest_id = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=100000.00,
    strategy_type='rebalancing',
    rebalance_frequency='quarterly',  # 'monthly', 'quarterly', 'semi_annually', 'annually'
    transaction_cost=0.001
)
```

**ความถี่ที่รองรับ**:
- `monthly` - รายเดือน
- `quarterly` - ทุก 3 เดือน
- `semi_annually` - ทุก 6 เดือน
- `annually` - ทุกปี

**ลักษณะการทำงาน**:
- ซื้อตามน้ำหนักเดิมในวันแรก
- Rebalance กลับสู่น้ำหนักเป้าหมายตามความถี่ที่กำหนด
- คำนวณค่าธรรมเนียมจากการ rebalance
- บันทึกประวัติการ rebalance ทุกครั้ง

### Strategy 3: Dollar Cost Averaging (DCA)

ลงทุนเพิ่มเป็นงวดๆ เป็นประจำ

```python
backtest_id = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=10000.00,
    strategy_type='dca',
    monthly_contribution=500.00,  # ลงทุนเพิ่ม $500 ทุกเดือน
    transaction_cost=0.001
)
```

**ลักษณะการทำงาน**:
- ลงทุนเงินต้นตามจำนวนที่กำหนดในวันแรก
- ลงทุนเพิ่มทุกต้นเดือนตามจำนวน monthly_contribution
- ซื้อตามน้ำหนักเป้าหมายในทุกครั้งที่ลงทุน
- เหมาะสำหรับผู้ที่มีรายได้ประจำและต้องการเฉลี่ยต้นทุน

### Running Examples

```bash
python example_backtest.py
```

จะแสดง menu ให้เลือกตัวอย่างที่ต้องการทดสอบ

## 📊 Output Files

### 1. Summary Report (backtest_summary_X.txt)

รายงานสรุปผลการทดสอบ:

```
================================================================================
BACKTEST SUMMARY REPORT
================================================================================

Backtest ID: 1
Generated: 2024-01-15 10:30:45

PORTFOLIO COMPOSITION
--------------------------------------------------------------------------------
Portfolio: Balanced 60/40

  SPY    -  60.0% - SPDR S&P 500 ETF Trust
  AGG    -  40.0% - iShares Core U.S. Aggregate Bond ETF

STRATEGY PARAMETERS
--------------------------------------------------------------------------------
Strategy: Buy and Hold
Initial Capital: $100,000.00
Transaction Cost: $100.00

BACKTEST PERIOD
--------------------------------------------------------------------------------
Start Date: 2015-01-02
End Date: 2023-12-29
Trading Days: 2267

PERFORMANCE RESULTS
--------------------------------------------------------------------------------
Final Portfolio Value: $182,543.21
Total Return: 82.54%
Annualized Return: 9.18%
Volatility (Annual): 12.34%
Sharpe Ratio: 0.74
Maximum Drawdown: -18.45%

================================================================================
END OF REPORT
================================================================================
```

### 2. Daily Results (backtest_results_X.txt)

ผลลัพธ์รายวัน:

```
================================================================================
BACKTEST RESULTS - Backtest ID: 1
================================================================================

Date         Portfolio Value    Daily Return   Cumulative Return
--------------------------------------------------------------------------------
2015-01-02     $100,000.00          0.0000%              0.00%
2015-01-05     $99,750.50          -0.2495%             -0.25%
2015-01-06     $100,123.45          0.3738%              0.12%
...
```

### 3. Log File (backtest.log)

บันทึกขั้นตอนการทำงานทั้งหมด:

```
2024-01-15 10:30:45 - INFO - run_backtest - STARTING BACKTEST
2024-01-15 10:30:45 - INFO - run_backtest - Portfolio ID: 1
2024-01-15 10:30:46 - INFO - strategy_buy_and_hold - Executing Buy and Hold strategy
2024-01-15 10:30:47 - INFO - get_price_data - Fetching price data for 2 ETFs
2024-01-15 10:35:12 - INFO - save_results_to_database - Inserted 2267 result records
2024-01-15 10:35:13 - INFO - run_backtest - BACKTEST COMPLETED SUCCESSFULLY
```

## 🎓 Strategy Comparison Example

```python
# เปรียบเทียบกลยุทธ์ต่างๆ บน portfolio เดียวกัน

# 1. Buy and Hold
bt1 = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=100000.00,
    strategy_type='buy_hold'
)

# 2. Quarterly Rebalancing
bt2 = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=100000.00,
    strategy_type='rebalancing',
    rebalance_frequency='quarterly'
)

# 3. DCA
bt3 = run_backtest(
    portfolio_id=1,
    start_date='2015-01-01',
    end_date='2023-12-31',
    initial_capital=10000.00,
    strategy_type='dca',
    monthly_contribution=500.00
)

# เปรียบเทียบผลลัพธ์
print("Backtest IDs:", bt1, bt2, bt3)
```

จากนั้นใช้ SQL query เปรียบเทียบ:

```sql
SELECT
    b.backtest_id,
    b.strategy_type,
    b.initial_capital,
    (SELECT portfolio_value FROM backtest_results
     WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1) AS final_value,
    (SELECT cumulative_return FROM backtest_results
     WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1) * 100 AS return_pct
FROM backtests b
WHERE b.backtest_id IN (1, 2, 3);
```

## 📈 Performance Metrics

Backtesting Engine คำนวณ metrics ต่อไปนี้:

### 1. Total Return
```
Total Return = (Final Value - Initial Capital) / Initial Capital
```

### 2. Annualized Return
```
Annualized Return = Total Return / (Trading Days / 252)
```

### 3. Volatility (Annual)
```
Volatility = Std Dev(Daily Returns) × √252
```

### 4. Sharpe Ratio
```
Sharpe Ratio = Annualized Return / Volatility
```

### 5. Maximum Drawdown
```
Drawdown = (Current Value - Running Maximum) / Running Maximum
Max Drawdown = Min(All Drawdowns)
```

## ⚙️ Configuration Options

### Transaction Cost

ค่าเริ่มต้น: 0.1% (0.001)

```python
transaction_cost=0.001  # 0.1% per transaction
transaction_cost=0.0005 # 0.05% for low-cost brokers
transaction_cost=0.0    # Zero cost (for comparison)
```

### Date Range

```python
start_date='2015-01-01'  # วันเริ่มต้น
end_date='2023-12-31'    # วันสิ้นสุด
```

**หมายเหตุ**:
- ระบบจะหา trading days อัตโนมัติจากข้อมูล price
- ถ้าวันที่ระบุไม่ใช่ trading day จะใช้วันถัดไป

## 🔧 Technical Details

### SQL Optimization

```python
# ดึงข้อมูลราคาด้วย WHERE clause filter
query = """
SELECT date, ticker, adjusted_close
FROM daily_prices
WHERE ticker IN (...)
  AND date >= %s
  AND date <= %s
ORDER BY date, ticker
"""
```

### Batch INSERT

```python
# Insert แบบ batch เพื่อความเร็ว
cursor.executemany(insert_query, batch_data)  # Insert หลายแถวพร้อมกัน
```

### Pandas Processing

```python
# ใช้ pandas pivot สำหรับคำนวณเร็ว
prices_pivot = price_data.pivot(index='date', columns='ticker', values='adjusted_close')

# คำนวณด้วย vectorized operations
portfolio_values = (shares * prices).sum(axis=1)
```

## 🐛 Error Handling

### กรณีข้อมูลไม่ครบ

```python
if price_data.empty:
    raise ValueError("No price data available for the specified date range")
```

**แก้ไข**:
1. ตรวจสอบว่ารัน data collection สำหรับ ETFs ทั้งหมดแล้ว
2. ตรวจสอบ date range ว่าอยู่ในช่วงที่มีข้อมูล

### กรณี Portfolio ไม่พบ

```python
if allocations.empty:
    raise ValueError(f"Portfolio {portfolio_id} not found or has no allocations")
```

**แก้ไข**:
- ตรวจสอบว่า portfolio_id ถูกต้อง
- ตรวจสอบว่ามี allocations ใน portfolio

## 📊 Database Schema

### backtests Table

```sql
CREATE TABLE backtests (
    backtest_id INT PRIMARY KEY,
    portfolio_id INT,
    start_date DATE,
    end_date DATE,
    initial_capital DECIMAL(15,2),
    strategy_type VARCHAR(50),
    rebalance_frequency VARCHAR(20),
    monthly_contribution DECIMAL(12,2),
    execution_date DATETIME,
    status VARCHAR(20)
);
```

### backtest_results Table

```sql
CREATE TABLE backtest_results (
    result_id BIGINT PRIMARY KEY,
    backtest_id INT,
    date DATE,
    portfolio_value DECIMAL(15,2),
    daily_return DECIMAL(10,6),
    cumulative_return DECIMAL(10,6),
    cash_balance DECIMAL(15,2),
    total_contributions DECIMAL(15,2)
);
```

### rebalance_history Table

```sql
CREATE TABLE rebalance_history (
    rebalance_id INT PRIMARY KEY,
    backtest_id INT,
    rebalance_date DATE,
    rebalance_details JSON,
    transaction_cost DECIMAL(12,2)
);
```

## 🚀 Performance Tips

### 1. ใช้ Date Range ที่เหมาะสม

```python
# ดี - ทดสอบ 5 ปี
start_date='2019-01-01'
end_date='2023-12-31'

# ระวัง - ทดสอบ 20 ปี อาจใช้เวลานาน
start_date='2003-01-01'
end_date='2023-12-31'
```

### 2. Batch Size Optimization

Code ใช้ batch insert โดยอัตโนมัติ - ไม่ต้องปรับแต่ง

### 3. Database Indexes

ตรวจสอบว่ามี indexes บน:
- `daily_prices.ticker`
- `daily_prices.date`
- `daily_prices (ticker, date)`

## 📁 Files

```
backtesting/
├── backtesting_engine.py   # Main engine (800+ lines)
├── example_backtest.py     # Usage examples
├── requirements.txt        # Dependencies
├── README.md              # Documentation (this file)
├── .gitignore             # Git ignore rules
├── backtest.log           # Log file (created automatically)
├── backtest_summary_*.txt # Summary reports (created per backtest)
└── backtest_results_*.txt # Daily results (created per backtest)
```

## 🔄 Workflow

```
1. Setup Database (Phase 1)
   ↓
2. Collect Price Data (Phase 2)
   ↓
3. Create Portfolio (Phase 3)
   ↓
4. Run Backtest (Phase 4) ← You are here
   ↓
5. Analyze Results
```

## 💡 Use Cases

### Use Case 1: เปรียบเทียบ Buy & Hold กับ Rebalancing

```python
# ทดสอบว่า rebalancing ช่วยเพิ่ม return หรือไม่
bt_hold = run_backtest(..., strategy_type='buy_hold')
bt_rebal = run_backtest(..., strategy_type='rebalancing', rebalance_frequency='quarterly')

# เปรียบเทียบใน database
```

### Use Case 2: หา Rebalance Frequency ที่เหมาะสม

```python
# ทดสอบความถี่ต่างๆ
frequencies = ['monthly', 'quarterly', 'semi_annually', 'annually']
results = {}

for freq in frequencies:
    bt_id = run_backtest(..., rebalance_frequency=freq)
    results[freq] = bt_id

# เปรียบเทียบผลลัพธ์
```

### Use Case 3: ทดสอบ DCA vs Lump Sum

```python
# DCA: ลงทุนค่อยเป็นค่อยไป
bt_dca = run_backtest(
    initial_capital=12000,
    monthly_contribution=1000,
    strategy_type='dca'
)

# Lump Sum: ลงทุนทีเดียว
bt_lump = run_backtest(
    initial_capital=24000,  # 12000 + (1000 × 12)
    strategy_type='buy_hold'
)
```

## 📝 Limitations

1. **ไม่รองรับ shorting** - ซื้อได้เท่านั้น
2. **ไม่รองรับ leverage** - ใช้เงินลงทุนตรงๆ
3. **ไม่รองรับ options/derivatives** - ETFs เท่านั้น
4. **Transaction cost แบบ flat rate** - ไม่ซับซ้อนตาม broker
5. **ไม่คำนวณ taxes** - ไม่รวมภาษี
6. **Rebalance แบบ calendar-based** - ไม่ใช่ threshold-based

## 🔒 Best Practices

1. **ทดสอบด้วย date range สั้นก่อน** เพื่อดูว่าทำงานถูกต้อง
2. **Backup database ก่อนรัน** backtest จำนวนมาก
3. **เช็ค log file** หากเกิด error
4. **เปรียบเทียบหลาย strategies** เพื่อหา optimal approach
5. **ใช้ transaction cost ที่สมจริง** ตาม broker ของคุณ

## 📞 Troubleshooting

### ปัญหา: "No price data available"

**แก้ไข**:
```bash
cd data_collection
python data_collection.py
# เลือก option 1 เพื่อดึงข้อมูล
```

### ปัญหา: Backtest ใช้เวลานาน

**แก้ไข**:
- ลด date range
- ตรวจสอบว่ามี database indexes
- ใช้ SSD แทน HDD

### ปัญหา: "Portfolio not found"

**แก้ไข**:
```python
from crud_operations import read_portfolio

# ดู portfolios ทั้งหมด
result = read_portfolio()
print(result['data'])
```

## 📚 References

- [Phase 1: Database Schema](../database/README.md)
- [Phase 2: Data Collection](../data_collection/README.md)
- [Phase 3: CRUD Operations](../crud_operations/README.md)

---

**License**: MIT
**Version**: 1.0.0
**Last Updated**: 2024-01-15
