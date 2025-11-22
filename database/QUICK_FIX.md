# Quick Fix - "Unknown column 'Ticker_Symbol'" Error

## The Problem
You're getting this error:
```
Error Code: 1054. Unknown column 'Ticker_Symbol' in 'field list'
```

## The Cause
The database schema wasn't created before trying to load data.

## The Solution (Choose One)

### ⚡ Option 1: Automated Fix (Fastest)

```bash
cd database
./fix_schema.sh
```

This script will:
1. Diagnose the problem
2. Offer to fix it automatically
3. Verify the fix worked

---

### 🔧 Option 2: Manual Fix

Run these commands in order:

```bash
# Step 1: Create the schema
mysql -u root -p < database/schema/01_create_schema.sql

# Step 2: Load the data
mysql -u root -p < database/data/02_load_etf_master.sql

# Step 3: Verify it worked
mysql -u root -p < database/verify.sql
```

---

### 🖥️ Option 3: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your server
3. **File → Run SQL Script**
4. Select: `database/schema/01_create_schema.sql`
5. Click **Run**
6. Wait for completion
7. **File → Run SQL Script**
8. Select: `database/data/02_load_etf_master.sql`
9. Click **Run**
10. Done!

---

### 🔍 Option 4: Command Line (MySQL)

```bash
# Connect to MySQL
mysql -u root -p

# Then run these commands:
```

```sql
-- Drop old database (if exists)
DROP DATABASE IF EXISTS etf_backtester_db;

-- Create fresh database
CREATE DATABASE etf_backtester_db;

-- Use it
USE etf_backtester_db;

-- Run schema script
SOURCE database/schema/01_create_schema.sql;

-- Load data
SOURCE database/data/02_load_etf_master.sql;

-- Verify
SELECT COUNT(*) FROM ETF_Master;
-- Should show: 50

-- Exit
EXIT;
```

---

## Verify Success

After running any of the above options, verify with:

```bash
mysql -u root -p etf_backtester_db -e "SELECT COUNT(*) as Total_ETFs FROM ETF_Master;"
```

**Expected output:**
```
+-----------+
| Total_ETFs|
+-----------+
|        50 |
+-----------+
```

If you see `50`, you're good to go! ✅

---

## Still Not Working?

### Check 1: Are you using the right database?

```sql
USE etf_backtester_db;
SELECT DATABASE();  -- Should show: etf_backtester_db
```

### Check 2: Does the table exist?

```sql
SHOW TABLES;  -- Should show: ETF_Master, Price_Data, Strategy_Log
```

### Check 3: Does the column exist?

```sql
DESCRIBE ETF_Master;  -- Should show Ticker_Symbol column
```

### Get Full Diagnostics

```bash
mysql -u root -p < database/diagnose.sql
```

---

## Common Mistakes

❌ **Running data script before schema script**
- Fix: Always run `01_create_schema.sql` before `02_load_etf_master.sql`

❌ **Connected to wrong database**
- Fix: Run `USE etf_backtester_db;` before your queries

❌ **Partial script execution**
- Fix: Run the entire schema script, don't just run selected parts

❌ **Case sensitivity issues**
- Fix: Use exact case as in schema: `ETF_Master` not `etf_master`

---

## Need More Help?

See detailed troubleshooting guide:
- **database/TROUBLESHOOTING.md** - Comprehensive troubleshooting
- **database/diagnose.sql** - Diagnostic queries
- **database/verify.sql** - Verification tests

---

## One-Liner Fix

If you just want to start fresh:

```bash
mysql -u root -p < database/schema/01_create_schema.sql && \
mysql -u root -p < database/data/02_load_etf_master.sql && \
echo "Done! Run: mysql -u root -p etf_backtester_db"
```

**Note:** This will DROP the existing database if it exists!
