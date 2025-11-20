# How to Get Price_Data.sql with Real Yahoo Finance Data

## The Challenge

Yahoo Finance requires authentication and proper headers to download data directly. The `yfinance` Python library handles this automatically, but requires specific dependencies.

## ✅ RECOMMENDED SOLUTION: Use Python Auto-Initialization

The **easiest and most reliable** way to get real Yahoo Finance data is to use the built-in Python auto-initialization:

### Step 1: Run the Main Program

```bash
cd etf_backtester
python main.py
```

**What happens:**
- System detects no database exists
- Automatically creates database schema
- **Downloads 50 ETFs from Yahoo Finance** (using yfinance with proper authentication)
- **Downloads 10 years of weekly price data** (~26,000 records)
- Takes 2-5 minutes
- All data is **REAL from Yahoo Finance**!

### Step 2: Export to SQL File

Once you have the data in your database, export it:

```bash
python export_to_sql.py
```

Choose **option 1** (Price_Data only) or **option 3** (Complete dataset)

**Result:** Creates `sql/price_data_YYYYMMDD_HHMMSS.sql` with all real Yahoo Finance data!

---

## Alternative Method: Manual Database Loading

If you don't want to run Python first, you'll need the data from someone who already has it:

### From Team Member:

1. **Team member** runs steps above and shares the `price_data_*.sql` file
2. **You** load it directly:

```bash
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/price_data_20250119_143022.sql
```

**Benefit:** Everyone on team uses identical Yahoo Finance dataset

---

## Why Can't We Download Directly?

Yahoo Finance implemented restrictions on direct CSV downloads:
- Requires cookies and authentication tokens
- Blocks simple HTTP requests (403 Forbidden)
- The `yfinance` Python library handles all of this automatically
- But yfinance has many dependencies that can be challenging to install

**Solution:** Use the Python program (main.py) which includes yfinance in requirements.txt and handles authentication properly.

---

## Step-by-Step Complete Guide

### For Individual Use:

```bash
# 1. Install requirements
cd etf_backtester
pip install -r requirements.txt

# 2. Run program (auto-downloads from Yahoo Finance)
python main.py
# Wait 2-5 minutes for download
# Data is now in your database!

# 3. Export to SQL file
python export_to_sql.py
# Choose option 3 for complete dataset

# 4. Now you have sql/price_data_*.sql file!
```

### For Team Collaboration:

**Team Lead (one time):**
```bash
# Download data
python main.py  # Downloads from Yahoo Finance

# Export to SQL
python export_to_sql.py  # Choose option 3

# Share the SQL file
# Upload to Google Drive / shared folder
```

**Team Members:**
```bash
# Get SQL file from team lead
# Load into your database
mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
mysql -u root -p etf_backtester_db < sql/price_data_20250119_143022.sql

# Run Python
python main.py  # Starts instantly, data already loaded!
```

---

## File You'll Get

**Price_Data.sql** contains:
- ~26,000 price records
- 50 ETFs (all real, tradeable securities)
- 10 years of weekly data
- OHLC prices (Open, High, Low, Close, Adjusted Close)
- Volume data
- File size: ~10-15 MB
- Format: SQL INSERT statements (1000 rows per batch)

**Sample structure:**
```sql
INSERT INTO Price_Data
(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)
VALUES
  (1, '2015-11-23', 205.5600, 207.5800, 203.5100, 206.8700, 206.8700, 35670100),
  (1, '2015-11-30', 206.5200, 209.5000, 203.5800, 208.8200, 208.8200, 38952300),
  ...
```

---

## Data Verification

After loading, verify the data:

```sql
-- Check total records
SELECT COUNT(*) FROM Price_Data;
-- Expected: ~26,000

-- Check date range
SELECT
    MIN(Price_Date) as Earliest,
    MAX(Price_Date) as Latest,
    COUNT(DISTINCT ETF_ID) as ETFs
FROM Price_Data;
-- Expected: ~10 years, 50 ETFs

-- Sample real data
SELECT pd.*, em.Ticker_Symbol, em.ETF_Name
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
ORDER BY pd.Price_Date DESC
LIMIT 10;
```

---

## Troubleshooting

### Q: Can I download directly without Python?

**A:** Not reliably. Yahoo Finance blocks direct downloads. You need:
- Either run Python program (which handles authentication)
- Or get SQL file from someone who already downloaded it

### Q: Can I use a pre-made SQL file?

**A:** Yes! If a team member or instructor provides a `price_data_*.sql` file with real Yahoo Finance data, you can load it directly:

```bash
mysql -u root -p etf_backtester_db < sql/price_data_YYYYMMDD_HHMMSS.sql
```

### Q: How do I know the data is real?

**A:** After loading, check the prices:
```sql
SELECT * FROM Price_Data
WHERE ETF_ID = 1  -- SPY
ORDER BY Price_Date DESC
LIMIT 5;
```

Compare with actual SPY prices on Yahoo Finance or Google Finance for those dates.

### Q: The export_to_sql.py requires database connection?

**A:** Yes, `export_to_sql.py` exports data that's already in your database. You must run `python main.py` first to download the Yahoo Finance data into the database.

---

## Quick Reference

| Method | Time | Internet | Pros |
|--------|------|----------|------|
| Python auto-init | 2-5 min | Required | Easiest, automatic, real data |
| Load from SQL file | 30-60 sec | Not required | Fastest, team sharing |
| Export from DB | 1-2 min | Not required | Backup existing data |

---

## Summary

**To get Price_Data.sql with real Yahoo Finance data:**

1. **Easiest:** Run `python main.py` → exports using `export_to_sql.py`
2. **Team:** Get SQL file from team member who ran step 1
3. **Future:** Load SQL file directly (no re-downloading needed)

**All data is 100% REAL from Yahoo Finance!** 📊

The Python program handles all Yahoo Finance authentication automatically through the yfinance library.
