# ✅ Project Import Checklist

## 📦 Portfolio Backtesting System - DADS 4002

---

## Current Status

✅ Database schema created (9 tables)
✅ Sample data generated (Excel, CSV files)
✅ Import scripts ready
⏳ **Next: Import data to MySQL**

---

## Step-by-Step Import Guide

### ✅ Step 1: Import First 3 Tables (2 minutes)

**File to use**: `IMPORT_ALL_DATA.sql`

**Instructions**:
1. Open MySQL Workbench
2. Connect to `portfolio_backtesting` database
3. Open file `IMPORT_ALL_DATA.sql`
4. Copy entire file (Ctrl+A, Ctrl+C)
5. Paste in MySQL Workbench
6. Execute (Ctrl+Shift+Enter)
7. Wait 2-3 seconds

**Expected result**:
```
✅ 50 rows inserted into etf_master
✅ 35 rows inserted into benchmark_portfolios
✅ 114 rows inserted into benchmark_holdings
```

**Verify**:
```sql
SELECT COUNT(*) FROM etf_master;           -- Should be 50
SELECT COUNT(*) FROM benchmark_portfolios; -- Should be 35
SELECT COUNT(*) FROM benchmark_holdings;   -- Should be 114
```

---

### ✅ Step 2: Import Price History (2-3 minutes)

**File to use**: `import_price_history.ipynb`

**Instructions**:
1. Open Terminal/Command Prompt
2. Navigate to project folder:
   ```bash
   cd desktop-tutorial
   ```
3. Start Jupyter:
   ```bash
   jupyter notebook
   ```
4. Open `import_price_history.ipynb`
5. Run cells in order:
   - **Cell 1**: Setup (check password = `krittanut123456`)
   - **Cell 2**: Connect to MySQL
   - **Cell 3**: Import 208,700 rows (1-2 minutes)
   - **Cell 4**: Verify results

**Expected result**:
```
[████████████████████████████████████████] 100.0% | 208,700/208,700 rows
✅ Import เสร็จสมบูรณ์!
⏱️  ใช้เวลา: 90.5 วินาที (1.5 นาที)
📦 Import: 208,700 rows
```

**Verify**:
```sql
SELECT COUNT(*) FROM price_history; -- Should be 208,700
```

---

### ✅ Step 3: Final Verification

**Run this query**:
```sql
SELECT 'etf_master' AS table_name, COUNT(*) AS row_count FROM etf_master
UNION ALL
SELECT 'benchmark_portfolios', COUNT(*) FROM benchmark_portfolios
UNION ALL
SELECT 'benchmark_holdings', COUNT(*) FROM benchmark_holdings
UNION ALL
SELECT 'price_history', COUNT(*) FROM price_history;
```

**Expected results**:
| table_name            | row_count |
|-----------------------|-----------|
| etf_master            | 50        |
| benchmark_portfolios  | 35        |
| benchmark_holdings    | 114       |
| price_history         | 208,700   |

---

## 🎉 After Import Complete

### Test the system:

1. **Open main.ipynb** - Main backtesting notebook
2. **Open analytics.ipynb** - Analytics and visualization
3. **Run all cells** - Should work without errors

---

## ❌ Troubleshooting

### Problem: IMPORT_ALL_DATA.sql gives Error 1064

**Solution**: Make sure you're using the latest version with `row_count` instead of `rows`

### Problem: import_price_history.ipynb can't find CSV file

**Solution**:
```bash
# Make sure you're in the right directory
cd /path/to/desktop-tutorial
pwd  # Should show desktop-tutorial folder
jupyter notebook
```

### Problem: "ต้อง import 3 ตารางแรกก่อน" error

**Solution**: Run Step 1 first (IMPORT_ALL_DATA.sql) before Step 2

### Problem: Duplicate entry error

**Solution**: Clear existing data first:
```sql
TRUNCATE TABLE price_history;
TRUNCATE TABLE benchmark_holdings;
TRUNCATE TABLE benchmark_portfolios;
TRUNCATE TABLE etf_master;
```

Then start from Step 1 again.

---

## 📁 Files Overview

### Import Files (Ready to use):
- ✅ `IMPORT_ALL_DATA.sql` - Step 1 (3 tables)
- ✅ `import_price_history.ipynb` - Step 2 (price history)

### Alternative Methods (if needed):
- `import_price_history.py` - Python script version
- `IMPORT_PRICE_HISTORY.sql` - SQL with LOAD DATA INFILE
- `EASIEST_IMPORT_GUIDE.md` - MySQL Workbench manual import

### Documentation:
- `IMPORT_PRICE_HISTORY_README.md` - Detailed troubleshooting
- `PROJECT_CHECKLIST.md` - This file

### Data Files:
- `data/etf_price_history.csv` - Price data (208,700 rows)
- `excel_files/*.xlsx` - Excel versions (for manual import)

---

## ⏱️ Total Time Estimate

- Step 1: **2 minutes**
- Step 2: **2-3 minutes**
- Verification: **1 minute**

**Total: 5-6 minutes** to complete all imports! 🚀

---

## 💡 Tips

1. **Run steps in order** - Don't skip Step 1
2. **Check MySQL is running** before starting
3. **Close other apps** during import to speed up
4. **Don't interrupt** Cell 3 in import_price_history.ipynb
5. **Verify each step** with SELECT COUNT(*) queries

---

## 📞 Need Help?

If you encounter issues:
1. Note which step you're at
2. Copy the error message
3. Check row counts with SELECT COUNT(*)
4. Review troubleshooting section above

---

**Ready to start?** Begin with Step 1! ✅
