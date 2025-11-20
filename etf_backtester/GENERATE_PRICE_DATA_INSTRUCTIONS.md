# How to Generate Full Price_Data.sql File

## Quick Instructions

Run these commands to get your complete Price_Data.sql file with ~26,000 real Yahoo Finance records:

```bash
# Step 1: Install requirements (one time only)
pip install yfinance pandas

# Step 2: Run the generator
cd etf_backtester
python generate_full_price_data.py

# Wait 3-5 minutes for download
# Output: sql/Price_Data.sql (~10-15 MB)
```

That's it! You'll have the complete SQL file ready to import.

---

## Detailed Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **Internet connection** (to download from Yahoo Finance)
3. **pip** package manager

### Step-by-Step Process

#### 1. Install Required Packages

Open terminal/command prompt and run:

```bash
pip install yfinance pandas
```

Or if you prefer using pip3:

```bash
pip3 install yfinance pandas
```

**What this installs:**
- `yfinance`: Yahoo Finance API library (handles authentication automatically)
- `pandas`: Data manipulation library

#### 2. Navigate to Project Directory

```bash
cd etf_backtester
```

Or full path:

```bash
cd /path/to/your/etf_backtester
```

#### 3. Run the Generator Script

```bash
python generate_full_price_data.py
```

Or:

```bash
python3 generate_full_price_data.py
```

**What happens:**
- Downloads 10 years of weekly data for all 50 ETFs
- Shows progress for each ETF (1/50, 2/50, etc.)
- Writes data to `sql/Price_Data.sql` file
- Takes 3-5 minutes depending on internet speed

**Expected output:**

```
================================================================================
GENERATING COMPLETE Price_Data.sql - REAL YAHOO FINANCE DATA
================================================================================

This will download 10 years of weekly data for 50 real ETFs
Estimated time: 3-5 minutes
Output file: sql/Price_Data.sql (10-15 MB, ~26,000 records)

Download period: 2015-11-20 to 2025-11-20
Downloading data for 50 ETFs...
================================================================================

[1/50] SPY    ... ✓ 521 weeks
[2/50] QQQ    ... ✓ 521 weeks
[3/50] IWM    ... ✓ 521 weeks
...
[50/50] INKM   ... ✓ 521 weeks

================================================================================
✓ Downloaded 26,050 total price records
================================================================================

Writing SQL file: sql/Price_Data.sql
Please wait...

  Progress: 5,000/26,050 (19.2%)
  Progress: 10,000/26,050 (38.4%)
  Progress: 15,000/26,050 (57.6%)
  Progress: 20,000/26,050 (76.8%)
  Progress: 25,000/26,050 (96.0%)
  Progress: 26,050/26,050 (100.0%)

================================================================================
SUCCESS!
================================================================================

✓ Created: sql/Price_Data.sql
✓ File size: 12.45 MB
✓ Total records: 26,050
✓ Date range: 2015-11-20 to 2025-11-20
✓ ETFs: 50 real securities

To load into MySQL:
  1. Load ETF_Master first: mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
  2. Load Price_Data: mysql -u root -p etf_backtester_db < sql/Price_Data.sql

================================================================================
```

#### 4. Load into MySQL

```bash
# Step 1: Load ETF Master data (if not already loaded)
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql

# Step 2: Load Price Data
mysql -u root -p etf_backtester_db < sql/Price_Data.sql
```

Enter your MySQL password when prompted.

---

## What You Get

**File created:** `sql/Price_Data.sql`

**Contents:**
- ~26,000 price records (exact number depends on current date)
- 50 real ETFs (all tradeable securities)
- 10 years of historical data
- Weekly OHLC prices:
  - Open Price
  - High Price
  - Low Price
  - Close Price
  - Adjusted Close Price
  - Volume

**Data source:** Yahoo Finance API (100% real market data)

**File structure:**
```sql
-- Batch INSERT statements (1000 rows per batch)
INSERT INTO Price_Data
(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)
VALUES
  (1, '2015-11-23', 205.56, 207.58, 203.51, 206.87, 206.87, 35670100),
  (1, '2015-11-30', 206.52, 209.50, 203.58, 208.82, 208.82, 38952300),
  ...
```

---

## Verification After Loading

Run these queries in MySQL to verify the data:

```sql
-- Total records
SELECT COUNT(*) FROM Price_Data;
-- Expected: ~26,000

-- Date range and coverage
SELECT
    MIN(Price_Date) as Earliest,
    MAX(Price_Date) as Latest,
    COUNT(DISTINCT ETF_ID) as ETFs
FROM Price_Data;
-- Expected: ~10 years, 50 ETFs

-- Sample data
SELECT pd.*, em.Ticker_Symbol
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE em.Ticker_Symbol = 'SPY'
ORDER BY pd.Price_Date DESC
LIMIT 10;
-- Should show recent SPY prices
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'yfinance'"

**Solution:**
```bash
pip install yfinance pandas
```

Make sure you're using the same Python version that you run the script with.

---

### Error: "Connection error" or "403 Forbidden"

**Cause:** Yahoo Finance temporary block or internet connection issue

**Solutions:**
1. Wait a few minutes and try again
2. Check your internet connection
3. Try from a different network
4. The yfinance library handles most authentication - make sure it's up to date:
   ```bash
   pip install --upgrade yfinance
   ```

---

### Script runs but no data downloaded

**Check:**
1. Internet connection is working
2. You're running from the `etf_backtester` directory
3. The `sql/` directory exists (script creates it automatically)

---

### Download is very slow

**Normal behavior:** Downloading 10 years of data for 50 ETFs takes 3-5 minutes.

**If it's taking longer:**
- Check internet speed
- Yahoo Finance servers might be slow (try during off-peak hours)
- Some ETFs might have connection timeouts (script will show warnings and continue)

---

## Alternative: Use Main Program

If you have trouble with the standalone generator, you can use the main program:

```bash
# Step 1: Run main program (auto-downloads data)
python main.py
# Let it complete auto-initialization

# Step 2: Export to SQL
python export_to_sql.py
# Choose option 1 (Price_Data only) or 3 (Complete dataset)
```

This requires MySQL to be installed and configured.

---

## For Team Collaboration

**Team Lead (one person):**
1. Run `python generate_full_price_data.py`
2. Share the `sql/Price_Data.sql` file with team (Google Drive, Dropbox, etc.)

**Team Members:**
1. Get the SQL file from team lead
2. Load it: `mysql -u root -p etf_backtester_db < sql/Price_Data.sql`
3. Everyone now has identical Yahoo Finance data!

**Benefits:**
- ✅ Consistent dataset across team
- ✅ Faster setup (no re-downloading)
- ✅ Reproducible results
- ✅ Works offline after initial download

---

## Summary

**To get your full Price_Data.sql:**

```bash
# Install (one time)
pip install yfinance pandas

# Generate (3-5 minutes)
python generate_full_price_data.py

# Load into MySQL
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/Price_Data.sql
```

**Result:** Complete database with 50 real ETFs and 10 years of real Yahoo Finance market data!

---

**All data is 100% REAL from Yahoo Finance!** 📊
