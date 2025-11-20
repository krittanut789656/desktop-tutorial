# SQL Data Files - Real Yahoo Finance Data

## What You Have Now ✅

### 1. `etf_master_data.sql` - READY TO USE
**Load immediately into MySQL:**
```bash
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
```
Contains 50 real ETFs (SPY, QQQ, VTI, VOO, bonds, commodities, etc.)

### 2. `Price_Data_SAMPLE.sql` - STRUCTURE EXAMPLE
Shows the correct format with 40 sample records (4 ETFs × 10 weeks)
- Demonstrates SQL INSERT statement format
- Shows real price data structure
- Use for testing or understanding format

## How to Get FULL Price_Data.sql 📥

### Yahoo Finance requires authentication - cannot download directly via simple scripts.

### ✅ METHOD 1: Generate Using Python (Recommended)

**This is the EASIEST and MOST RELIABLE method:**

```bash
# Step 1: Install requirements (one time)
cd etf_backtester
pip install -r requirements.txt

# Step 2: Run main program (downloads from Yahoo Finance)
python main.py
# Automatically downloads 26,000+ real price records
# Takes 2-5 minutes on first run

# Step 3: Export to SQL file
python export_to_sql.py
# Choose option 1 (Price_Data only) or option 3 (Complete dataset)

# Done! You now have:
# sql/price_data_YYYYMMDD_HHMMSS.sql (10-15 MB, ~26,000 records)
```

**Load it:**
```bash
mysql -u root -p etf_backtester_db < sql/price_data_20250119_143022.sql
```

---

### ✅ METHOD 2: Team Collaboration

**Team Lead (one person does this):**
```bash
# Download data once
python main.py

# Export to SQL
python export_to_sql.py  # Choose option 3

# Share the SQL file with team
# (Upload to Google Drive, shared folder, etc.)
```

**Team Members:**
```bash
# Get SQL file from team lead
# Load into your database
mysql -u root -p etf_backtester_db < sql/price_data_YYYYMMDD_HHMMSS.sql

# Everyone now has identical Yahoo Finance data!
```

---

## Why Can't We Provide Price_Data.sql Directly?

1. **Dynamic Data**: Market data changes daily/weekly
2. **File Size**: ~10-15 MB (too large for git by default)
3. **Yahoo Finance Auth**: Requires proper authentication (handled by yfinance library)
4. **Team Consistency**: Better for each team to download once and share

---

## What You'll Get

When you generate `Price_Data.sql` using Method 1:

- **Records:** ~26,000 (50 ETFs × ~520 weeks)
- **Period:** 10 years of weekly data
- **Fields:** Open, High, Low, Close, Adjusted Close, Volume
- **Source:** 100% REAL from Yahoo Finance
- **Size:** 10-15 MB
- **Format:** SQL INSERT statements (1000 rows per batch)

**ETFs included:**
- **25 Equity:** SPY, QQQ, IWM, VTI, VOO, DIA, IVV, VEA, VWO, EFA, VUG, VTV, XLF, XLE, XLK, XLV, XLI, XLY, XLP, XLU, ARKK, ARKW, ARKG, ARKF, SOXX
- **15 Bond:** AGG, BND, TLT, IEF, SHY, LQD, HYG, MUB, TIP, VCIT, VCSH, BNDX, EMB, JNK, GOVT
- **5 Commodity:** GLD, SLV, USO, DBA, DBC
- **5 Mixed:** AOR, AOM, AOK, GAL, INKM

---

## Quick Start Options

### Option A: Let Python Handle Everything (Easiest)
```bash
python main.py
# Auto-downloads and loads everything
# No SQL files needed!
```

### Option B: Generate SQL Files for Team Sharing
```bash
# 1. Download data
python main.py

# 2. Export to SQL
python export_to_sql.py

# 3. Share with team
# Everyone loads the same SQL file
```

### Option C: Just Testing/Learning
```bash
# Load sample data
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/Price_Data_SAMPLE.sql

# Try the system with 40 sample records
python main.py
```

---

## Verification After Loading

```sql
-- Check record count
SELECT COUNT(*) FROM Price_Data;
-- Sample: 40 | Full: ~26,000

-- Check date range
SELECT
    MIN(Price_Date) as Earliest,
    MAX(Price_Date) as Latest,
    COUNT(DISTINCT ETF_ID) as ETFs
FROM Price_Data;
-- Full dataset: ~10 years, 50 ETFs

-- View recent data
SELECT pd.*, em.Ticker_Symbol, em.ETF_Name
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
ORDER BY pd.Price_Date DESC
LIMIT 10;
```

---

## Files in this Directory

| File | Status | Purpose |
|------|--------|---------|
| `database.sql` | ✅ Ready | Database schema (tables, constraints) |
| `etf_master_data.sql` | ✅ Ready | 50 real ETFs (load immediately) |
| `Price_Data_SAMPLE.sql` | ✅ Ready | Sample data showing format (40 records) |
| `price_data_*.sql` | 📥 Generate | Full dataset (~26,000 records) - use Method 1 or 2 above |
| `HOW_TO_GET_PRICE_DATA.md` | 📖 Guide | Detailed instructions |
| `README_SQL_DATA.md` | 📖 Guide | Comprehensive SQL data guide |
| `README.md` | 📖 This file | Quick reference |

---

## Summary

**You have:**
- ✅ `etf_master_data.sql` (50 ETFs - ready to load)
- ✅ `Price_Data_SAMPLE.sql` (40 records - for testing)
- ✅ Complete guides and documentation

**To get full Price_Data.sql:**
```bash
python main.py              # Downloads from Yahoo Finance
python export_to_sql.py     # Exports to SQL file
```

**Or:** Get SQL file from team member who already ran the steps above.

---

**All data is 100% REAL from Yahoo Finance API!** 📊

See `HOW_TO_GET_PRICE_DATA.md` for detailed instructions and troubleshooting.
