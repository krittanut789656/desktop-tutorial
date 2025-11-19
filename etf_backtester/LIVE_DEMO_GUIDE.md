# 🎯 LIVE DEMO GUIDE FOR PROFESSOR
## ETF Portfolio Backtester - One Run Complete Demo

---

## 🚀 How to Start Demo

Simply run **ONE** command:

```bash
cd etf_backtester
python main.py
```

That's it! Everything runs from this single program.

---

## 📋 Demo Flow (Recommended Order)

### **Step 1: Initialize System** ⚙️

```
Enter choice: 1.1
```
- Creates MySQL database
- Sets up 3 tables (ETF_Master, Price_Data, Strategy_Log)
- Creates Primary Keys and Foreign Keys
- Takes: ~5 seconds

**Result:** Database ready ✓

---

### **Step 2: Download Real Market Data** 📊

```
Enter choice: 1.2
Continue? yes
```
- Downloads 50 real ETFs from Yahoo Finance
- 10 years of weekly historical data
- ~26,000 price records
- Takes: 2-3 minutes (live download!)

**Result:** Real market data loaded ✓

---

### **Step 3: Check Data Status** 📈

```
Enter choice: 1.3
```
- Shows all 3 tables
- Row counts per table
- Verifies 30+ rows requirement

**Result:** Data verification ✓

---

### **Step 4: Run Backtest** 🔄

```
Enter choice: 2.1
Continue? yes
```
- Runs momentum strategy backtest
- Uses SQL to calculate momentum scores
- Selects top 5 ETFs
- Calculates returns
- Takes: ~10 seconds

**Result:** Backtest complete with CAGR ✓

---

### **Step 5: Generate Analytics** 📊

```
Enter choice: 3.1
Continue? yes
```
- **Insight #1:** Volatility by Asset Type (Complex SQL #1)
- **Insight #2:** Lookback Period Comparison (Complex SQL #2)
- **Insight #3:** Drawdown Analysis (Complex SQL #3)
- Takes: ~5 seconds

**Result:** All 3 SQL insights generated ✓

---

### **Step 6: CRUD Operations Demo** 🔧

#### READ Operation:
```
Enter choice: 4.1
(Press Enter for latest)
```
Shows backtest results from database

#### UPDATE Operation:
```
Enter choice: 4.4
ETF ID: 1
Date: 2024-01-01
New Price: 450.00
```
Updates price in database

#### DELETE Operation:
```
Enter choice: 4.5
Days: 365
Continue? yes
```
Deletes old logs from database

**Result:** CRUD operations demonstrated ✓

---

### **Step 7: Export to Excel** 📑

```
Enter choice: 6.3
```
- Exports ETF_Master table
- Exports Price_Data table (26,000+ rows)
- Creates multi-sheet Excel files
- Saves to `data/` folder
- Takes: ~30 seconds

**Result:** Excel files created ✓

---

### **Step 8: Exit Demo** 🏁

```
Enter choice: 0
```

**Demo Complete!** All requirements demonstrated ✓

---

## ✅ What Professor Can Show

### 1. **Database Requirements (DEMONSTRATED)**
- ✓ 3 Tables: ETF_Master, Price_Data, Strategy_Log
- ✓ Primary Keys (PK) on all tables
- ✓ Foreign Keys (FK) linking tables
- ✓ 30+ rows per table (26,000+ in Price_Data!)

### 2. **SQL-Focused Implementation (DEMONSTRATED)**
- ✓ Core backtest uses complex SQL queries
- ✓ Momentum calculation in SQL (not Python loops)
- ✓ 3 complex analytical SQL queries

### 3. **CRUD Operations (DEMONSTRATED)**
- ✓ CREATE: Loading data
- ✓ READ: View backtest results
- ✓ UPDATE: Modify price data
- ✓ DELETE: Remove old logs

### 4. **Python Interface (DEMONSTRATED)**
- ✓ Single CLI entry point (main.py)
- ✓ No need to open MySQL manually
- ✓ No need to edit files manually
- ✓ Everything via menu selections

### 5. **Text File Integration (DEMONSTRATED)**
- ✓ Logs backtest results to .txt files
- ✓ Available in menu 5.1, 5.2

### 6. **Real Data (DEMONSTRATED)**
- ✓ Downloads from Yahoo Finance
- ✓ 50 real, tradeable ETFs
- ✓ 10 years of historical data
- ✓ Weekly frequency

---

## 🎬 Quick Demo (5 Minutes)

For a fast demonstration, run these in order:

```
python main.py

1.1  → Initialize database (5 sec)
1.3  → Show database status (instant)
2.1  → Run backtest (10 sec) [Use pre-loaded data]
3.1  → Generate all insights (5 sec)
4.1  → Show results (instant)
6.1  → Export to Excel (5 sec)
0    → Exit
```

**Total Time:** ~5 minutes
**Shows:** All key features

---

## 🔥 Full Demo (10 Minutes)

For complete demonstration:

```
python main.py

1.1  → Initialize database
1.2  → Download data from Yahoo Finance (3 min)
1.3  → Verify data
2.1  → Run standard backtest
2.3  → Run comparative backtest (3M vs 6M)
3.1  → Generate all 3 insights
4.1  → READ: View results
4.4  → UPDATE: Modify a price
4.5  → DELETE: Remove old logs
6.3  → Export all tables to Excel
5.1  → View text logs
0    → Exit
```

**Total Time:** ~10 minutes
**Shows:** Every single feature

---

## 💡 Demo Tips

### Before Demo:
1. **Start MySQL server:**
   ```bash
   sudo service mysql start
   ```

2. **Test database connection:**
   ```bash
   mysql -u root -p
   # Enter password
   ```

3. **Have terminal ready:**
   - Font size 14+ for readability
   - Full screen mode

### During Demo:

**✓ DO:**
- Explain what each menu does
- Show the SQL queries running (visible in output)
- Point out the 3 complex SQL analytics
- Highlight real Yahoo Finance data
- Show Excel files after export

**✗ DON'T:**
- Don't exit the program between operations
- Don't switch to other applications
- Don't manually edit files or database
- Everything stays in `main.py`

### Key Talking Points:

1. **"Single Entry Point"** - One Python file controls everything
2. **"SQL-Focused"** - Core logic in SQL, not Python
3. **"Real Data"** - Yahoo Finance, not synthetic
4. **"Complete System"** - Database + Python + Analytics + Export

---

## 🐛 Troubleshooting During Demo

### If MySQL Not Connected:
```
# Before running main.py:
sudo service mysql start
```

### If Data Already Loaded:
- Just skip menu 1.2
- Go directly to menu 2.1 (backtest)

### If Want to Reset:
```
# In MySQL:
DROP DATABASE etf_backtester_db;

# Then start demo from 1.1 again
```

---

## 📊 Expected Output Examples

### After Backtest (Menu 2.1):
```
Total Rebalances: 12
Cumulative Return: 15.34%
CAGR: 14.82%
```

### After Analytics (Menu 3.1):
```
INSIGHT #1: Commodity has highest volatility (28.45%)
INSIGHT #2: 90-day lookback yielded highest CAGR (14.82%)
INSIGHT #3: Equity was held during max drawdown periods
```

### After Excel Export (Menu 6.3):
```
✓ Exported to: data/ETF_Master_20250119_120000.xlsx
✓ Exported to: data/Price_Data_20250119_120000.xlsx
```

---

## 🎓 For Questions

**Q: "Why weekly data instead of daily?"**
A: Reduces noise, better for momentum strategies, still captures trends

**Q: "Why Yahoo Finance?"**
A: Free, reliable, real market data, widely used in academia

**Q: "Can we modify the strategy?"**
A: Yes! Menu 2.2 allows custom parameters (lookback, rebalance frequency)

**Q: "What about the 3 complex SQL queries?"**
A:
- Query #1: Volatility calculation with STDDEV and window functions
- Query #2: CAGR comparison with grouped aggregations
- Query #3: Drawdown analysis with self-joins and CTEs

---

## ✅ Checklist for Professor

Before demo:
- [ ] MySQL running
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Terminal in full screen with large font
- [ ] Internet connection (for Yahoo Finance download)

During demo:
- [ ] Run `python main.py`
- [ ] Follow the demo flow above
- [ ] Stay in the program until done
- [ ] Exit with menu choice 0

After demo:
- [ ] Show generated Excel files in `data/` folder
- [ ] Show text logs in `logs/` folder
- [ ] Explain how everything was done from single program

---

**Remember:** The entire demo runs from ONE command: `python main.py`

**No switching programs. No manual database edits. No file editing. Just menu choices!** 🎯
