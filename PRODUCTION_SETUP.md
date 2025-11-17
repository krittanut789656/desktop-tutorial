# Full Production Setup Guide

**Complete step-by-step guide to setup and run the ETF Portfolio Backtesting System in production**

---

## 🚀 Quick Start (Automated)

### Option 1: One-Command Setup (Recommended)

```bash
python3 setup_production.py
```

This will:
- ✅ Test MySQL connection
- ✅ Create database and tables
- ✅ Insert 40 sample ETFs
- ✅ Insert 8 sample portfolios
- ✅ Install Python dependencies
- ✅ Create config.ini file
- ✅ Run data collection (ETF prices)
- ✅ Verify setup
- ✅ Launch application

**Time required:** 15-20 minutes (most time is data collection)

---

## 📋 Prerequisites

### 1. MySQL Server
**Your Configuration:**
- Host: `127.0.0.1`
- Port: `3306`
- User: `root`
- Password: (you'll enter during setup)

**Check MySQL is running:**
```bash
# Linux/Mac
sudo systemctl status mysql
# or
sudo service mysql status

# Windows
# Check Services app for MySQL service
```

### 2. Python 3.8+
```bash
python3 --version
# Should show Python 3.8 or higher
```

### 3. pip (Python package manager)
```bash
pip3 --version
# or
python3 -m pip --version
```

---

## 🔧 Manual Setup (Step by Step)

If you prefer manual control or automated setup fails:

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- mysql-connector-python (Database)
- pandas, numpy (Data analysis)
- yfinance (Stock data)
- matplotlib, seaborn (Visualization)
- colorama, tabulate (Console UI)
- tqdm (Progress bars)

**Verify installation:**
```bash
python3 check_system.py
```

### Step 2: Setup MySQL Database

#### 2.1 Create Database and Tables

```bash
cd database

# Enter your MySQL password when prompted
mysql -u root -h 127.0.0.1 -P 3306 -p < 01_create_database.sql
```

This creates:
- Database: `etf_backtesting`
- 8 tables: etfs, daily_prices, portfolios, portfolio_etfs, backtests, backtest_transactions, backtest_portfolio_values, backtest_metrics

#### 2.2 Insert Sample ETFs (40 ETFs)

```bash
mysql -u root -h 127.0.0.1 -P 3306 -p etf_backtesting < 02_insert_sample_etfs.sql
```

Categories:
- US Equity (SPY, QQQ, IWM, etc.)
- International (VEA, EEM, VWO, etc.)
- Fixed Income (AGG, BND, TLT, etc.)
- Commodities (GLD, SLV, DBC, etc.)
- Real Estate (VNQ, IYR, REM, etc.)
- Alternatives (VXX, VIXY, TAIL, etc.)

#### 2.3 Insert Sample Portfolios (8 portfolios) - Optional

```bash
mysql -u root -h 127.0.0.1 -P 3306 -p etf_backtesting < 03_insert_sample_portfolios.sql
```

Portfolios:
1. Conservative 60/40
2. Moderate Balanced
3. Aggressive Growth
4. All Weather
5. Income Focus
6. Global Diversified
7. Tech Heavy
8. Hedged Portfolio

### Step 3: Create Configuration File

#### Option A: Manual config.ini

Create `config.ini` in project root:

```ini
[database]
host = 127.0.0.1
user = root
password = YOUR_MYSQL_PASSWORD
database = etf_backtesting
port = 3306

[application]
log_level = INFO
default_initial_capital = 100000.0
default_transaction_cost = 0.001
default_risk_free_rate = 0.02

[analytics]
default_benchmark = SPY
chart_dpi = 300

[data_collection]
default_start_date = 2009-01-01
default_end_date = 2025-12-31
max_retries = 3
```

#### Option B: Generate Template

```bash
python3 config.py --create-template
cp config.ini.template config.ini
# Edit config.ini with your password
```

### Step 4: Fetch ETF Price Data

**This is the longest step (~10-15 minutes)**

```bash
cd data_collection
python3 data_collection.py
```

This will:
- Fetch historical prices for 40+ ETFs
- Date range: 2009-01-01 to 2025-12-31
- Source: Yahoo Finance (yfinance)
- ~400,000+ price records

**Monitor progress:**
```bash
# In another terminal
tail -f data_collection/data_collection.log
```

### Step 5: Verify Setup

```bash
cd ..
python3 check_system.py
```

Expected output:
```
✓ Dependencies: 9/9 packages installed
✓ Configuration: All files present
✓ Modules: All accessible
✓ Database: Connected
  ├─ ETFs: 40+
  ├─ Price Records: 400,000+
  ├─ Portfolios: 8
  └─ Date Range: 2009-01-01 to 2025-12-31

✓ System is ready for production use!
```

---

## 🎯 Running the System

### Option 1: Main Application (Recommended)

```bash
python3 main.py
```

**Interactive Menu:**
```
1. Portfolio Management
2. ETF Management
3. Run Backtest
4. Analytics & Insights
5. Reports & Export
6. System Settings
0. Exit
```

### Option 2: Analytics Examples

```bash
cd analytics
python3 example_analytics.py
```

**Available Analyses:**
1. Risk-Adjusted Performance Analysis
2. Optimal Rebalancing Frequency
3. DCA vs Lump Sum Market Timing
4. Run All Insights
5. Custom Analysis

### Option 3: Backtesting Examples

```bash
cd backtesting
python3 example_backtest.py
```

### Option 4: Quick Start Script

```bash
./quick_start.sh
```

Interactive launcher with menu options.

---

## 🔍 Troubleshooting

### Problem: MySQL Connection Failed

**Error:** `Access denied for user 'root'@'127.0.0.1'`

**Solutions:**
1. Check password is correct
2. Try without host: `mysql -u root -p`
3. Check MySQL is running: `sudo systemctl status mysql`
4. Reset password if needed:
   ```bash
   sudo mysql
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   ```

### Problem: Database Already Exists

**Error:** `Database 'etf_backtesting' already exists`

**Solutions:**
1. Use existing database (safe)
2. Drop and recreate:
   ```bash
   mysql -u root -p -e "DROP DATABASE IF EXISTS etf_backtesting;"
   mysql -u root -p < database/01_create_database.sql
   ```

### Problem: pip install fails

**Error:** `ERROR: Could not find a version that satisfies the requirement...`

**Solutions:**
1. Upgrade pip:
   ```bash
   python3 -m pip install --upgrade pip
   ```

2. Install packages individually:
   ```bash
   pip install mysql-connector-python
   pip install pandas numpy
   pip install yfinance
   pip install matplotlib seaborn
   pip install colorama tabulate tqdm
   ```

### Problem: yfinance fails to fetch data

**Error:** `[*********************100%***********************]  1 of 1 failed`

**Solutions:**
1. Check internet connection
2. Retry later (Yahoo Finance rate limiting)
3. Run data collection again:
   ```bash
   cd data_collection
   python3 data_collection.py
   ```

### Problem: Module Import Error

**Error:** `ModuleNotFoundError: No module named 'crud_operations'`

**Solution:**
Make sure you're running from project root directory:
```bash
cd /home/user/desktop-tutorial
python3 main.py
```

### Problem: No Price Data

**Check:**
```bash
python3 check_system.py
```

If "Price Records: 0" or low number:
```bash
cd data_collection
python3 data_collection.py
```

---

## 📊 Verify Production Readiness

Run comprehensive system check:

```bash
python3 check_system.py
```

**Green light indicators:**
- ✅ All dependencies installed
- ✅ All configuration files present
- ✅ All modules accessible
- ✅ Database connected
- ✅ 40+ ETFs loaded
- ✅ 400,000+ price records
- ✅ 8 sample portfolios
- ✅ Date range: 2009-2025

---

## 🎓 Usage Examples

### Example 1: View Your Portfolios

```bash
python3 main.py
# Select: 1.2 (View Portfolios)
# Select portfolio ID to view details
```

### Example 2: Run Risk Analysis

```bash
cd analytics
python3 example_analytics.py
# Select: 1 (Risk-Adjusted Performance Analysis)
# Follow prompts
# View: insight1_risk_adjusted_report.txt
```

### Example 3: Compare Rebalancing Strategies

```bash
cd analytics
python3 example_analytics.py
# Select: 2 (Optimal Rebalancing Analysis)
# View: insight2_rebalancing_analysis.txt
```

### Example 4: Test DCA vs Lump Sum

```bash
cd analytics
python3 example_analytics.py
# Select: 3 (DCA vs Lump Sum Analysis)
# View: insight3_dca_vs_lumpsum.txt
```

### Example 5: Create Custom Portfolio

```bash
python3 main.py
# Select: 1.1 (Create New Portfolio)
# Enter name: "My Tech Portfolio"
# Select ETFs: QQQ, VGT, ARKK
# Enter weights: 50%, 30%, 20%
# Confirm creation
```

---

## 📈 Performance Expectations

**System Performance:**
- Portfolio creation: <0.1 seconds
- Backtest (5 years, daily): 5-10 seconds
- Analytics (all 3 insights): 15-30 seconds
- Data collection (40 ETFs, 16 years): 10-15 minutes

**Database Size:**
- Empty database: ~5 MB
- With price data: ~50-100 MB
- With backtests: varies by usage

---

## 🔐 Security Notes

**Production Best Practices:**

1. **Never commit config.ini to git** (already in .gitignore)

2. **Use environment variables for sensitive data:**
   ```bash
   export DB_PASSWORD=your_password
   ```

3. **Create a dedicated MySQL user:**
   ```sql
   CREATE USER 'etf_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON etf_backtesting.* TO 'etf_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Enable SSL for MySQL connections** (for remote databases)

5. **Regular backups:**
   ```bash
   mysqldump -u root -p etf_backtesting > backup_$(date +%Y%m%d).sql
   ```

---

## 🚀 Production Deployment Checklist

- [ ] MySQL server running and accessible
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (`01_create_database.sql`)
- [ ] Sample data loaded (`02_insert_sample_etfs.sql`)
- [ ] Configuration file created (`config.ini`)
- [ ] Price data fetched (`data_collection.py`)
- [ ] System check passes (`check_system.py`)
- [ ] Main application runs (`main.py`)
- [ ] Logs directory writable
- [ ] Backups configured

---

## 📞 Support

**If you encounter issues:**

1. Run system check:
   ```bash
   python3 check_system.py
   ```

2. Check logs:
   ```bash
   tail -f main_app.log
   tail -f analytics/analytics.log
   tail -f backtesting/backtest.log
   tail -f data_collection/data_collection.log
   ```

3. Verify MySQL:
   ```bash
   mysql -u root -h 127.0.0.1 -P 3306 -p -e "SHOW DATABASES;"
   ```

4. Check documentation:
   - Main: `README.md`
   - Database: `database/README.md`
   - Analytics: `analytics/README.md`
   - Backtesting: `backtesting/README.md`

---

## 🎉 You're Ready!

Once setup is complete, you have a **full production-ready** ETF portfolio backtesting and analytics system!

**Start trading smarter with data-driven insights! 📊🚀**

---

**Next Steps:**
1. Explore sample portfolios
2. Run analytics on existing portfolios
3. Create your own custom portfolios
4. Backtest different strategies
5. Make informed investment decisions

**Happy Investing!**
