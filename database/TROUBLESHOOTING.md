# Troubleshooting Guide - ETF Backtester Database

## Error: "Unknown column 'Ticker_Symbol' in 'field list'"

This error occurs when trying to insert data into the ETF_Master table, but the table structure doesn't match the expected schema.

### Possible Causes

1. **Schema script not run** - The database schema wasn't created
2. **Wrong database** - You're connected to a different database
3. **Partial execution** - The schema script failed partway through
4. **Wrong order** - Data loading script ran before schema script

---

## Quick Fix

### Step 1: Run Diagnostic Script

```bash
mysql -u root -p < database/diagnose.sql
```

This will show you:
- If the database exists
- If the table exists
- The current table structure
- Any existing data

### Step 2: Clean Slate Approach

If the diagnostic shows issues, start fresh:

```bash
# Run schema creation (this will DROP and recreate the database)
mysql -u root -p < database/schema/01_create_schema.sql

# Then load the data
mysql -u root -p < database/data/02_load_etf_master.sql
```

### Step 3: Verify Success

```bash
mysql -u root -p etf_backtester_db -e "SELECT COUNT(*) as Total_ETFs FROM ETF_Master;"
```

Expected output: `Total_ETFs: 50`

---

## Detailed Troubleshooting Steps

### Check 1: Verify Database Exists

```sql
SHOW DATABASES LIKE 'etf_backtester_db';
```

**If empty:** Run the schema script first
```bash
mysql -u root -p < database/schema/01_create_schema.sql
```

### Check 2: Verify You're Using Correct Database

```sql
SELECT DATABASE();
```

**If NULL or wrong database:**
```sql
USE etf_backtester_db;
```

### Check 3: Verify Table Exists

```sql
USE etf_backtester_db;
SHOW TABLES;
```

**Expected output:**
- ETF_Master
- Price_Data
- Strategy_Log

**If tables missing:** Run the schema script

### Check 4: Verify Table Structure

```sql
DESCRIBE ETF_Master;
```

**Expected columns:**
- ETF_ID
- Ticker_Symbol
- ETF_Name
- Asset_Type
- Expense_Ratio
- Inception_Date
- Created_At
- Updated_At

**If structure is wrong:** Run the schema script to recreate

### Check 5: Check for Case Sensitivity

Some MySQL configurations are case-sensitive. Try:

```sql
-- Check actual table name
SHOW TABLES;

-- If it shows 'etf_master' instead of 'ETF_Master', use lowercase
SELECT * FROM etf_master;
```

---

## Common Scenarios

### Scenario 1: First Time Setup

**Error:** Database doesn't exist

**Solution:**
```bash
mysql -u root -p < database/schema/01_create_schema.sql
mysql -u root -p < database/data/02_load_etf_master.sql
```

### Scenario 2: Wrong Database Selected

**Error:** Column not found, but database exists

**Solution:**
```sql
-- Check current database
SELECT DATABASE();

-- Switch to correct database
USE etf_backtester_db;

-- Try your query again
SELECT * FROM ETF_Master;
```

### Scenario 3: Schema Partially Created

**Error:** Some tables exist, some don't

**Solution:**
```bash
# Drop and recreate everything
mysql -u root -p << EOF
DROP DATABASE IF EXISTS etf_backtester_db;
EOF

# Then run schema
mysql -u root -p < database/schema/01_create_schema.sql
mysql -u root -p < database/data/02_load_etf_master.sql
```

### Scenario 4: Using MySQL Workbench or GUI Tool

**Error:** Scripts run but data not loaded

**Solution:**
1. Open MySQL Workbench
2. File → Run SQL Script
3. Select `database/schema/01_create_schema.sql`
4. Execute
5. File → Run SQL Script
6. Select `database/data/02_load_etf_master.sql`
7. Execute

**Important:** Make sure to run the entire script, not just selected parts

---

## Manual Step-by-Step Setup

If automated scripts aren't working, try manual setup:

### Step 1: Create Database

```sql
DROP DATABASE IF EXISTS etf_backtester_db;
CREATE DATABASE etf_backtester_db;
USE etf_backtester_db;
```

### Step 2: Create ETF_Master Table

```sql
CREATE TABLE ETF_Master (
    ETF_ID INT PRIMARY KEY AUTO_INCREMENT,
    Ticker_Symbol VARCHAR(10) NOT NULL UNIQUE,
    ETF_Name VARCHAR(100) NOT NULL,
    Asset_Type VARCHAR(50) NOT NULL,
    Expense_Ratio DECIMAL(5,4),
    Inception_Date DATE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_type (Asset_Type),
    INDEX idx_ticker (Ticker_Symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Step 3: Verify Table

```sql
DESCRIBE ETF_Master;
```

### Step 4: Insert Sample Data

```sql
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date)
VALUES ('SPY', 'SPDR S&P 500 ETF Trust', 'Equity', 0.0945, '2010-01-01');

SELECT * FROM ETF_Master;
```

If this works, then run the full data loading script.

---

## Verification Checklist

After setup, verify everything is correct:

```sql
USE etf_backtester_db;

-- 1. Check table count
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'etf_backtester_db';
-- Expected: 3 tables (ETF_Master, Price_Data, Strategy_Log)

-- 2. Check ETF count
SELECT COUNT(*) FROM ETF_Master;
-- Expected: 50

-- 3. Check ETF breakdown
SELECT Asset_Type, COUNT(*) as Count
FROM ETF_Master
GROUP BY Asset_Type;
-- Expected:
-- Bond: 15
-- Commodity: 5
-- Equity: 25
-- Mixed: 5

-- 4. Check views exist
SHOW FULL TABLES WHERE Table_type = 'VIEW';
-- Expected: vw_latest_prices, vw_portfolio_summary

-- 5. Check triggers exist
SHOW TRIGGERS;
-- Expected: validate_price_data
```

---

## Getting More Help

### Check MySQL Error Log

```bash
# Linux
sudo tail -f /var/log/mysql/error.log

# macOS (Homebrew)
tail -f /usr/local/var/mysql/*.err

# Windows
# Check C:\ProgramData\MySQL\MySQL Server X.X\Data\*.err
```

### Check MySQL Version

```bash
mysql --version
```

Minimum required: MySQL 5.7+ or MariaDB 10.2+

### Check Permissions

```sql
SHOW GRANTS FOR CURRENT_USER();
```

You need at least:
- CREATE DATABASE
- CREATE TABLE
- INSERT, SELECT, UPDATE, DELETE

---

## Still Having Issues?

1. **Run the diagnostic script:**
   ```bash
   mysql -u root -p < database/diagnose.sql > diagnosis.txt
   ```

2. **Check the output in `diagnosis.txt`**

3. **Common fixes:**
   - Ensure MySQL is running
   - Check username/password
   - Verify user has sufficient privileges
   - Check MySQL configuration (my.cnf/my.ini)

4. **Nuclear option (fresh start):**
   ```bash
   # Backup any existing data first!
   mysql -u root -p -e "DROP DATABASE IF EXISTS etf_backtester_db;"
   mysql -u root -p < database/schema/01_create_schema.sql
   mysql -u root -p < database/data/02_load_etf_master.sql
   ```

---

## Success Indicators

You should see:

```
✓ Database 'etf_backtester_db' exists
✓ 3 tables created (ETF_Master, Price_Data, Strategy_Log)
✓ 2 views created (vw_latest_prices, vw_portfolio_summary)
✓ 1 trigger created (validate_price_data)
✓ 50 ETF records loaded
✓ Data validated successfully
```

Run this final check:

```sql
SELECT
    (SELECT COUNT(*) FROM ETF_Master) as ETF_Count,
    (SELECT COUNT(*) FROM information_schema.tables
     WHERE table_schema = 'etf_backtester_db'
     AND table_type = 'BASE TABLE') as Table_Count,
    (SELECT COUNT(*) FROM information_schema.views
     WHERE table_schema = 'etf_backtester_db') as View_Count;
```

Expected: `ETF_Count: 50, Table_Count: 3, View_Count: 2`
