# SQL Data Files - Real Yahoo Finance Data

## Available SQL Files

### 1. ✅ `etf_master_data.sql` - READY TO USE

**Contains:** 50 real ETFs from Yahoo Finance with metadata

**Load immediately:**
```bash
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
```

**What you get:**
- 25 Equity ETFs (SPY, QQQ, VOO, VTI, sector funds, ARK Innovation funds, etc.)
- 15 Bond ETFs (AGG, TLT, corporate bonds, municipal bonds, international bonds)
- 5 Commodity ETFs (GLD, SLV, USO, agriculture, commodities index)
- 5 Mixed/Balanced ETFs (allocation funds)

---

### 2. 📥 `price_data_YYYYMMDD_HHMMSS.sql` - GENERATE WITH SCRIPT

**Contains:** Real weekly price data from Yahoo Finance (10 years, ~26,000 records)

**How to generate:**

#### Step 1: Install Requirements
```bash
pip install yfinance pandas numpy
```

#### Step 2: Run Generator Script
```bash
cd etf_backtester
python generate_price_data_sql.py
```

When prompted, type `yes` to continue.

#### Step 3: Wait for Download
- Takes 2-5 minutes depending on internet speed
- Downloads 10 years of weekly data for all 50 ETFs
- Creates ~10-15 MB SQL file

#### Step 4: Load into Database
```bash
# First, load ETF_Master (if not already loaded)
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql

# Then load Price_Data
mysql -u root -p etf_backtester_db < sql/price_data_20250119_143022.sql
```

**What you get:**
- Real OHLC prices (Open, High, Low, Close, Adjusted Close)
- Real trading volumes
- Weekly data frequency (~520 weeks over 10 years)
- ~26,000+ price records (50 ETFs × ~520 weeks)

---

## Why Generate SQL Files?

### Benefits:

1. **Faster Setup**
   - Download once, load many times
   - No waiting for Yahoo Finance API
   - Instant database population

2. **Team Collaboration**
   - Everyone uses identical data
   - Consistent backtest results across team
   - No version mismatches

3. **Offline Work**
   - Work without internet after initial download
   - No dependency on Yahoo Finance availability
   - Portable dataset

4. **Backup & Archive**
   - Preserve historical data snapshots
   - Document exact data used for analysis
   - Reproducible research

5. **Database Restore**
   - Quick disaster recovery
   - Reset to known good state
   - Test with production data

---

## Quick Start Options

### Option A: Use Python Auto-Initialization (Easiest)

```bash
# Just run the main program - it does everything!
python main.py
```

**What happens:**
- Auto-detects no database exists
- Creates database schema
- Downloads 50 ETFs from Yahoo Finance
- Downloads 10 years of price data
- Ready to use immediately!

**When to use:** Demo, first-time setup, you have internet

---

### Option B: Use SQL Files (Faster Subsequent Setups)

```bash
# 1. Create database schema
mysql -u root -p < sql/database.sql

# 2. Load ETF Master data
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql

# 3. Generate Price Data SQL (first time only)
python generate_price_data_sql.py

# 4. Load Price Data
mysql -u root -p etf_backtester_db < sql/price_data_20250119_143022.sql

# 5. Run Python
python main.py  # Starts instantly, data already loaded!
```

**When to use:** Team sharing, offline work, faster reset

---

### Option C: Hybrid Approach (Best for Teams)

**Team Lead (once):**
```bash
# Download fresh data
python main.py  # Auto-downloads from Yahoo Finance

# Export to SQL
python generate_price_data_sql.py

# Share SQL file with team
# Upload to Google Drive, Git LFS, or shared folder
```

**Team Members:**
```bash
# Get SQL files from team lead
# Load into database
mysql -u root -p < sql/database.sql
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/price_data_20250119_143022.sql

# Run Python - instant start!
python main.py
```

**Benefits:**
- ✅ Team lead downloads once
- ✅ Team members skip download time
- ✅ Everyone has identical data
- ✅ Consistent results across team

---

## File Sizes & Load Times

| File | Size | Records | Load Time |
|------|------|---------|-----------|
| `database.sql` | ~5 KB | Schema only | <1 sec |
| `etf_master_data.sql` | ~5 KB | 50 ETFs | <1 sec |
| `price_data_*.sql` | 10-15 MB | ~26,000 prices | 30-60 sec |

**Total time to load all SQL files:** ~1 minute

**Compared to Python download:** 2-5 minutes

**Savings:** 1-4 minutes per setup!

---

## Data Verification After Loading

```sql
-- Check ETF count
SELECT COUNT(*) FROM ETF_Master;
-- Expected: 50

-- Check ETF breakdown by asset type
SELECT Asset_Type, COUNT(*) as Count
FROM ETF_Master
GROUP BY Asset_Type;
-- Expected: Bond(15), Commodity(5), Equity(25), Mixed(5)

-- Check price data count
SELECT COUNT(*) FROM Price_Data;
-- Expected: 26,000+ (varies by current date)

-- Check date range
SELECT
    MIN(Price_Date) as Earliest,
    MAX(Price_Date) as Latest,
    COUNT(DISTINCT Price_Date) as Unique_Dates
FROM Price_Data;
-- Expected: ~10 years, ~520 unique weeks

-- Check data completeness
SELECT
    em.Ticker_Symbol,
    COUNT(pd.Price_ID) as Price_Records
FROM ETF_Master em
LEFT JOIN Price_Data pd ON em.ETF_ID = pd.ETF_ID
GROUP BY em.Ticker_Symbol
ORDER BY Price_Records;
-- Expected: Each ETF should have ~520 records
```

---

## Regenerating Price Data

Price data becomes stale over time. To get latest market data:

```bash
# Re-generate SQL file with fresh Yahoo Finance data
python generate_price_data_sql.py

# This creates a new file with current timestamp:
# sql/price_data_20250119_153045.sql (example)

# Load the new file
mysql -u root -p etf_backtester_db < sql/price_data_20250119_153045.sql
```

**Recommendation:** Regenerate monthly for up-to-date analysis

---

## Troubleshooting

### Problem: "Table 'Price_Data' doesn't exist"

**Solution:**
```bash
# Load database schema first
mysql -u root -p < sql/database.sql

# Then load price data
mysql -u root -p etf_backtester_db < sql/price_data_*.sql
```

---

### Problem: "Foreign key constraint fails"

**Solution:**
```bash
# Load ETF_Master BEFORE Price_Data
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/price_data_*.sql
```

Price_Data references ETF_Master via foreign key, so ETF_Master must exist first.

---

### Problem: "Duplicate entry" error

**Solution:**
```sql
-- Clear existing data first
DELETE FROM Price_Data;

-- Then load SQL file
SOURCE sql/price_data_20250119_143022.sql;
```

Or use the commented DELETE statement included in the SQL file.

---

### Problem: generate_price_data_sql.py fails to run

**Check requirements:**
```bash
# Verify Python packages installed
pip list | grep -E "(yfinance|pandas|numpy)"

# If missing, install:
pip install yfinance pandas numpy
```

**Check internet connection:**
```bash
# Test Yahoo Finance access
python -c "import yfinance as yf; print(yf.Ticker('SPY').history(period='1wk'))"
```

---

## Important Notes

### Data Authenticity

✅ **All data is REAL from Yahoo Finance**
- Not synthetic
- Not randomly generated
- Actual historical market prices
- Suitable for academic analysis

### Data Characteristics

- **Frequency:** Weekly (Monday close or first trading day)
- **History:** 10 years from generation date
- **Fields:** Open, High, Low, Close, Adjusted Close, Volume
- **Quality:** As provided by Yahoo Finance API
- **Gaps:** Market holidays/closures result in missing weeks (expected)

### Data Update Strategy

| Scenario | Recommendation |
|----------|---------------|
| Course project demo | Download once, keep throughout semester |
| Monthly analysis | Regenerate monthly |
| Daily trading | Use Python auto-download instead |
| Team collaboration | Share one SQL snapshot, all use same data |

---

## Summary

**For quick setup:**
```bash
python main.py  # Auto-downloads everything
```

**For team sharing:**
```bash
# Lead: Generate SQL once
python generate_price_data_sql.py

# Team: Load SQL files
mysql -u root -p etf_backtester_db < sql/price_data_*.sql
```

**For offline work:**
```bash
# Download once with internet
python generate_price_data_sql.py

# Use forever offline
mysql -u root -p etf_backtester_db < sql/price_data_*.sql
```

---

**All SQL files contain 100% REAL data from Yahoo Finance!** 📊✅
