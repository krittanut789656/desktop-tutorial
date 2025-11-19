# SQL Data Files Guide - Real Yahoo Finance Data

## Overview

This guide explains how to work with SQL data files containing **real market data from Yahoo Finance**. These files allow you to:

1. Load ETF data directly from SQL (no Python needed)
2. Backup your downloaded Yahoo Finance data
3. Share data with team members
4. Restore data quickly without re-downloading

---

## Available SQL Files

### 1. `sql/etf_master_data.sql` ✅ **READY TO USE**

**What it contains:**
- 50 real, tradeable ETFs across 4 asset types
- All ETF metadata (ticker, name, asset type, expense ratio)

**Asset breakdown:**
- Equity: 25 ETFs (SPY, QQQ, IWM, VOO, VTI, sector ETFs, ARK funds, etc.)
- Bond: 15 ETFs (AGG, BND, TLT, corporate bonds, muni bonds, etc.)
- Commodity: 5 ETFs (GLD, SLV, USO, DBA, DBC)
- Mixed: 5 ETFs (AOR, AOM, AOK, allocation funds)

**How to load:**
```bash
# From command line:
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql

# Or from MySQL prompt:
USE etf_backtester_db;
SOURCE sql/etf_master_data.sql;
```

**When to use:**
- When you want to load ETF definitions directly via SQL
- When setting up database manually instead of using auto-initialization
- When sharing ETF list with team members

---

### 2. `sql/price_data_*.sql` - **GENERATE WITH SCRIPT**

**What it contains:**
- Real weekly price data from Yahoo Finance
- 10 years of historical data
- 26,000+ records (50 ETFs × ~520 weeks)
- OHLC prices (Open, High, Low, Close, Adjusted Close, Volume)

**How to generate:**

**Option A: Using generator script (Direct from Yahoo Finance):**
```bash
# Install requirements (one time)
pip install yfinance pandas numpy

# Run generator script
cd etf_backtester
python generate_price_data_sql.py
# Type 'yes' when prompted
# Takes 2-5 minutes to download from Yahoo Finance
# Creates: sql/price_data_YYYYMMDD_HHMMSS.sql (~10-15 MB)
```

**Option B: Export from existing database:**
```bash
# First, run the system to download Yahoo Finance data:
python main.py
# Let it auto-download data (first time only)

# Then export to SQL:
python export_to_sql.py
# Choose option 1 or 3
```

**How to load:**
```bash
# Load ETF_Master first (if not already loaded)
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql

# Then load Price_Data
mysql -u root -p etf_backtester_db < sql/price_data_20250119_120000.sql
```

**File size:** ~10-15 MB for complete dataset (~26,000 records)

---

### 3. `sql/complete_data_*.sql` - **COMPLETE BACKUP**

**What it contains:**
- Everything: ETF_Master + Price_Data
- Full database content in one file
- Can restore entire database

**How to generate:**
```bash
python export_to_sql.py
# Choose option 3: Complete dataset
```

**How to load:**
```bash
# This will populate both ETF_Master and Price_Data tables
mysql -u root -p etf_backtester_db < sql/complete_data_20250119_120000.sql
```

---

## Usage Scenarios

### Scenario 1: Quick Setup with ETF_Master Only

**Use case:** You want to load ETF definitions via SQL, then download prices via Python

```bash
# 1. Create database schema
mysql -u root -p < etf_backtester/sql/database.sql

# 2. Load ETF Master data
mysql -u root -p etf_backtester_db < etf_backtester/sql/etf_master_data.sql

# 3. Run Python to download prices
cd etf_backtester
python main.py
# System will detect ETF_Master exists and only download price data
```

---

### Scenario 2: Complete Offline Setup (No Internet Required)

**Use case:** You want to work offline with pre-downloaded data

```bash
# First time (with internet):
# 1. Run system to download data
python main.py  # Auto-downloads from Yahoo Finance

# 2. Export to SQL for backup
python export_to_sql.py  # Choose option 3

# Later (offline, on another machine):
# 1. Create database schema
mysql -u root -p < sql/database.sql

# 2. Load complete data from SQL file
mysql -u root -p etf_backtester_db < sql/complete_data_20250119_120000.sql

# 3. Run Python (no download needed!)
python main.py  # Starts instantly, data already loaded
```

---

### Scenario 3: Team Data Sharing

**Use case:** Share exact same data with team members

**Team Lead:**
```bash
# 1. Download data once
python main.py

# 2. Export to SQL
python export_to_sql.py  # Option 3

# 3. Share the SQL file with team
# Upload to Google Drive / GitHub / shared folder
```

**Team Members:**
```bash
# 1. Get SQL file from team lead
# 2. Load into their database
mysql -u root -p etf_backtester_db < sql/complete_data_20250119_120000.sql

# 3. Everyone has identical data!
```

**Benefits:**
- ✅ Consistent data across team (same dates, same prices)
- ✅ No repeated Yahoo Finance downloads
- ✅ Faster setup for team members
- ✅ Works offline

---

## Export Tool Usage

### Running the Export Tool

```bash
cd etf_backtester
python export_to_sql.py
```

**Menu options:**
1. **Price_Data only** - Exports all ~26,000 price records
2. **Price_Data with limit** - Export recent N rows (e.g., 5000 rows)
3. **Complete dataset** - Exports ETF_Master + Price_Data

### Export Examples

**Example 1: Export all price data**
```bash
python export_to_sql.py
# Choose: 1
# Creates: sql/price_data_20250119_120000.sql (~10 MB)
```

**Example 2: Export recent data only**
```bash
python export_to_sql.py
# Choose: 2
# Enter: 5000
# Creates: sql/price_data_20250119_120000.sql (~500 KB)
```

**Example 3: Complete backup**
```bash
python export_to_sql.py
# Choose: 3
# Creates: sql/complete_data_20250119_120000.sql (~15 MB)
```

---

## Data Verification

After loading SQL files, verify the data:

```sql
-- Check ETF count
SELECT COUNT(*) as Total_ETFs FROM ETF_Master;
-- Expected: 50

-- Check ETF breakdown
SELECT Asset_Type, COUNT(*) as Count
FROM ETF_Master
GROUP BY Asset_Type
ORDER BY Asset_Type;
-- Expected: Equity(25), Bond(15), Commodity(5), Mixed(5)

-- Check price data
SELECT COUNT(*) as Total_Price_Records FROM Price_Data;
-- Expected: 26,000+ (depends on current date)

-- Check date range
SELECT
    MIN(Price_Date) as Earliest_Date,
    MAX(Price_Date) as Latest_Date,
    COUNT(DISTINCT Price_Date) as Unique_Dates,
    COUNT(DISTINCT ETF_ID) as Unique_ETFs
FROM Price_Data;
-- Expected: ~10 years of weekly data, ~520 weeks, 50 ETFs
```

---

## Important Notes

### Data Freshness

- **ETF_Master data**: Static (50 ETFs don't change frequently)
- **Price_Data**: Dynamic (market prices change daily)
- **Recommendation**: Re-download price data monthly for latest market data

### File Sizes

| File | Approximate Size | Records |
|------|-----------------|---------|
| `etf_master_data.sql` | ~5 KB | 50 ETFs |
| `price_data_*.sql` (all) | ~10 MB | 26,000+ prices |
| `price_data_*.sql` (5000 rows) | ~500 KB | 5,000 prices |
| `complete_data_*.sql` | ~15 MB | 50 + 26,000+ |

### Loading Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Load ETF_Master | <1 second | 50 rows only |
| Load Price_Data (all) | 30-60 seconds | 26,000+ rows |
| Load Complete Dataset | 1-2 minutes | Both tables |

**Tip:** Use `SET FOREIGN_KEY_CHECKS = 0;` for faster bulk loading (already included in export files)

---

## Workflow Recommendations

### For Development/Testing

```bash
# Use auto-initialization (easiest):
python main.py  # Auto-downloads everything

# Or use SQL files for faster setup:
mysql -u root -p < sql/database.sql
mysql -u root -p etf_backtester_db < sql/complete_data_YYYYMMDD.sql
```

### For Production/Demo

```bash
# Day before demo:
# 1. Download latest data
python main.py  # Downloads from Yahoo Finance

# 2. Backup to SQL
python export_to_sql.py  # Option 3

# Demo day:
# Just run Python - data already loaded!
python main.py  # Instant start
```

### For Team Collaboration

```bash
# Team Lead:
# 1. Download and export
python main.py
python export_to_sql.py

# 2. Share SQL file with team
git add sql/complete_data_YYYYMMDD.sql
git commit -m "Add Yahoo Finance data snapshot"
git push

# Team Members:
# 1. Pull latest
git pull

# 2. Load data
mysql -u root -p etf_backtester_db < sql/complete_data_YYYYMMDD.sql

# 3. Run system
python main.py  # Everyone has same data!
```

---

## Troubleshooting

### Error: "Table already exists"

**Solution:**
```sql
-- Clear existing data first:
DELETE FROM Strategy_Log;
DELETE FROM Price_Data;
DELETE FROM ETF_Master;

-- Then load SQL file
SOURCE sql/filename.sql;
```

### Error: "Foreign key constraint fails"

**Solution:**
The SQL files include `SET FOREIGN_KEY_CHECKS = 0;` at the beginning.
Make sure you run the entire file, not just parts of it.

### Export fails: "No data found"

**Solution:**
```bash
# You need to download data first:
python main.py
# Let auto-initialization complete

# Then export:
python export_to_sql.py
```

---

## Data Source Information

**Source:** Yahoo Finance API (via yfinance Python library)

**Data characteristics:**
- Frequency: Weekly (every Monday or first trading day of week)
- History: 10 years from current date
- Fields: Open, High, Low, Close, Adjusted Close, Volume
- Accuracy: Real market data, suitable for academic analysis

**ETF Selection:**
- All 50 ETFs are real, actively traded securities
- Selected for diversity across asset classes
- Include major market indices (SPY, QQQ, IWM)
- Include sector funds, bonds, commodities, and balanced funds

---

## Quick Reference

**Load ETF definitions only:**
```bash
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
```

**Load complete dataset:**
```bash
mysql -u root -p etf_backtester_db < sql/complete_data_*.sql
```

**Export current database to SQL:**
```bash
python export_to_sql.py
```

**Verify data after loading:**
```sql
SELECT COUNT(*) FROM ETF_Master;  -- Should be 50
SELECT COUNT(*) FROM Price_Data;  -- Should be 26,000+
```

---

**All data files contain REAL market data from Yahoo Finance!** 📊
