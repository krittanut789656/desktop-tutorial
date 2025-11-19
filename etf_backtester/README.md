# ETF Portfolio Backtester

**DADS 4002 Course Project**
Simple 50-ETF Momentum Strategy Backtesting System

---

## 📋 Project Overview

This project implements a **Simple 50-ETF Portfolio Strategy Backtester** using:
- **Database**: MySQL (Relational Database)
- **Interface**: Python Command Line Interface (CLI)
- **Data Source**: Real market data from Yahoo Finance
- **Data Frequency**: Weekly price data (10 years historical)
- **Strategy**: Momentum-based ETF selection
- **Focus**: SQL-focused analytics and actionable insights

The system allows users to backtest momentum-based trading strategies on a portfolio of 50 real ETFs across different asset classes (Equity, Bond, Commodity, Mixed) using actual historical data from Yahoo Finance, and generate actionable insights using complex SQL queries.

---

## ✅ Project Requirements Checklist

### A. Core System & Interface

- [x] **Integrated System**: Single Python script (`main.py`) as entry point
- [x] **Python Interface**: All operations run via Python CLI
- [x] **No Manual SQL/File Editing**: Everything controlled through the CLI

### B. Database Requirements

- [x] **Relational DB Setup**: MySQL database with proper schema
- [x] **Table Count**: Minimum 3 tables implemented:
  - `ETF_Master`: Master ETF information
  - `Price_Data`: Historical price data
  - `Strategy_Log`: Backtest execution logs
- [x] **Keys**: Primary Key (PK) and Foreign Key (FK) constraints implemented
- [x] **Data Volume**: 30+ rows per table (Price_Data has 26,000+ weekly records from 10 years of real market data)

### C. Functional Features (CRUD & Analytics)

- [x] **CRUD - Read**: Display backtest results from Strategy_Log
- [x] **CRUD - Update**: Update price data and strategy notes
- [x] **CRUD - Delete**: Delete old backtest logs
- [x] **Data Analytics**: Three complex SQL queries for insights:
  1. **Volatility Analysis**: Calculate volatility by asset type
  2. **Lookback Period Optimization**: Compare CAGR across lookback periods
  3. **Drawdown Analysis**: Analyze asset exposure during drawdowns

### D. Supporting Features

- [x] **Text File Integration**: Log backtest summaries to .txt files
- [x] **Excel Export**: Export database tables to Excel for analysis
- [x] **SQL Data Files**: Real Yahoo Finance data available as SQL INSERT statements
- [x] **SQL-Focused**: Core momentum calculation uses SQL queries
- [x] **Modular Design**: Clean separation of concerns

---

## 🛠️ Installation & Setup

### Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **MySQL Server 5.7+** or **MariaDB 10.3+**
   ```bash
   mysql --version
   ```

3. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `mysql-connector-python`: Database connectivity
   - `yfinance`: Yahoo Finance data downloader
   - `pandas`: Data manipulation
   - `numpy`: Numerical operations

### Database Setup

1. **Create MySQL User and Database** (if needed):
   ```sql
   CREATE USER 'etf_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON etf_backtester_db.* TO 'etf_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Configure Database Connection**:

   The system uses the following default configuration:
   - Host: `localhost`
   - Port: `3306`
   - Database: `etf_backtester_db`
   - User: `root`
   - Password: `password`

   To change these settings, you can:
   - Set environment variables:
     ```bash
     export DB_HOST=localhost
     export DB_USER=your_username
     export DB_PASSWORD=your_password
     export DB_NAME=etf_backtester_db
     ```
   - Or modify `modules/db_connector.py` directly

### Project Setup

1. **Clone/Download the project**:
   ```bash
   cd etf_backtester
   ```

2. **Verify file structure**:
   ```
   etf_backtester/
   ├── main.py                 # Main CLI entry point
   ├── README.md               # This file
   ├── sql/
   │   └── database.sql        # Database schema
   ├── modules/
   │   ├── db_connector.py     # Database connection handler
   │   ├── data_loader.py      # Sample data generator
   │   ├── backtest_engine.py  # Core backtesting logic
   │   ├── analytics.py        # SQL-based analytics
   │   ├── crud_operations.py  # CRUD operations
   │   └── text_logger.py      # Text file logging
   ├── logs/                   # Text log files (auto-created)
   └── data/                   # Data files (if needed)
   ```

---

## 🚀 Usage Guide

### Quick Start with Auto-Initialization

**The system automatically sets up everything on first run!**

1. **Run the main program**:
   ```bash
   python main.py
   ```

2. **First Time Run** (2-5 minutes):
   - System auto-detects no database exists
   - Automatically creates database schema (3 tables with PK/FK)
   - Automatically downloads 50 ETFs from Yahoo Finance
   - Loads 26,000+ weekly price records (10 years of data)
   - Ready to use immediately after setup!

3. **Subsequent Runs** (instant):
   - System detects existing database and data
   - Starts in ~2 seconds
   - Ready to use immediately!

4. **Start Using**:
   - Run a backtest (Menu 1.1)
   - Generate insights (Menu 2.1)
   - Perform CRUD operations (Menu 3.x)
   - Export to Excel (Menu 4.5)

### Alternative: Load Data from SQL Files

**For faster setup, team collaboration, or offline work:**

1. **Load ETF Master data** (instant):
   ```bash
   mysql -u root -p etf_backtester_db < sql/etf_master_data.sql
   ```

2. **Generate Price Data SQL** (one time):
   ```bash
   python generate_price_data_sql.py
   # Downloads from Yahoo Finance and creates SQL file
   ```

3. **Load Price Data** (30-60 seconds):
   ```bash
   mysql -u root -p etf_backtester_db < sql/price_data_YYYYMMDD_HHMMSS.sql
   ```

**Benefits:** Share exact same dataset with team, work offline, faster reset

**See:** `sql/README_SQL_DATA.md` for complete SQL data guide

### Main Menu Options

```
[1] Run Backtest
  1.1 - Run Standard Backtest (90-day lookback)
  1.2 - Run Custom Backtest (specify parameters)
  1.3 - Run Comparative Backtest (3M vs 6M)

[2] Analytics & Insights
  2.1 - Generate All Insights
  2.2 - Insight #1: Volatility Analysis
  2.3 - Insight #2: Lookback Period Comparison
  2.4 - Insight #3: Drawdown Analysis

[3] CRUD Operations
  3.1 - Read: View Backtest Results
  3.2 - Read: View All Backtest Runs
  3.3 - Read: View ETF Information
  3.4 - Update: Modify Price Data
  3.5 - Delete: Remove Old Backtest Logs

[4] Reports & Export
  4.1 - View Text Logs
  4.2 - Export Latest Results to Text
  4.3 - Export ETF_Master to Excel
  4.4 - Export Price_Data to Excel
  4.5 - Export All Tables to Excel

[0] Exit
```

**Note**: No manual setup required! Database and data are auto-initialized on first run.

---

## 📊 Strategy Explanation

### Momentum Strategy

The backtester implements a **momentum-based portfolio selection strategy** using **real weekly market data from Yahoo Finance**:

1. **Lookback Period**: Analyze ETF performance over the past N days (e.g., 90 or 180 days)
   - Works with weekly data: system finds closest weekly price to target date
   - 90 days ≈ 13 weeks (3 months)
   - 180 days ≈ 26 weeks (6 months)

2. **Selection**: Calculate momentum score for each ETF:
   ```
   Momentum Score = ((End_Price - Start_Price) / Start_Price) × 100
   ```

3. **Portfolio Construction**:
   - Select top 3-5 ETFs with highest momentum scores
   - Equal-weight allocation

4. **Rebalancing**: Re-evaluate and rebalance portfolio every N days (e.g., 30 days ≈ 4 weeks)

5. **Performance Tracking**: Calculate returns for each holding period using real market prices

### SQL-Focused Implementation

The core momentum calculation is performed **entirely in SQL** using Common Table Expressions (CTEs):

```sql
-- Simplified example
WITH StartPrices AS (
    SELECT ETF_ID, Close_Price as Start_Price
    FROM Price_Data
    WHERE Price_Date = lookback_date
),
EndPrices AS (
    SELECT ETF_ID, Close_Price as End_Price
    FROM Price_Data
    WHERE Price_Date = selection_date
)
SELECT
    ETF_ID,
    ((End_Price - Start_Price) / Start_Price * 100) as Momentum_Score
FROM StartPrices
JOIN EndPrices USING (ETF_ID)
ORDER BY Momentum_Score DESC
LIMIT 5;
```

---

## 🔍 Analytics Insights

### Insight #1: Volatility Analysis by Asset Type

**Question**: Which Asset_Type has the highest price volatility?

**SQL Implementation**:
- Calculate daily returns for each ETF
- Compute standard deviation grouped by Asset_Type
- Annualize volatility using √252 scaling

**Actionable Output**:
- Identifies riskiest asset classes
- Helps with risk management decisions

### Insight #2: Lookback Period Optimization

**Question**: Which Lookback Period (3M vs 6M) yields higher CAGR?

**SQL Implementation**:
- Aggregate performance by lookback period
- Calculate CAGR: `(1 + Total_Return)^(365/Days) - 1`
- Compare results

**Actionable Output**:
- Optimizes strategy parameters
- Data-driven period selection

### Insight #3: Drawdown Analysis

**Question**: What Asset_Type was held during Max Drawdown periods?

**SQL Implementation**:
- Calculate cumulative returns
- Identify maximum drawdown dates
- Analyze asset type exposure during those periods

**Actionable Output**:
- Identifies assets contributing to losses
- Informs defensive positioning

---

## 🗂️ Database Schema

### Table: ETF_Master

| Column | Type | Constraints |
|--------|------|-------------|
| ETF_ID | INT | PRIMARY KEY, AUTO_INCREMENT |
| Ticker_Symbol | VARCHAR(10) | NOT NULL, UNIQUE |
| ETF_Name | VARCHAR(100) | NOT NULL |
| Asset_Type | VARCHAR(50) | NOT NULL |
| Expense_Ratio | DECIMAL(5,4) | |
| Inception_Date | DATE | |

### Table: Price_Data

| Column | Type | Constraints |
|--------|------|-------------|
| Price_ID | BIGINT | PRIMARY KEY, AUTO_INCREMENT |
| ETF_ID | INT | FOREIGN KEY → ETF_Master(ETF_ID) |
| Price_Date | DATE | NOT NULL |
| Close_Price | DECIMAL(12,4) | NOT NULL |
| Open_Price | DECIMAL(12,4) | |
| High_Price | DECIMAL(12,4) | |
| Low_Price | DECIMAL(12,4) | |
| Adj_Close_Price | DECIMAL(12,4) | |
| Volume | BIGINT | |

**Unique Constraint**: (ETF_ID, Price_Date)

### Table: Strategy_Log

| Column | Type | Constraints |
|--------|------|-------------|
| Log_ID | INT | PRIMARY KEY, AUTO_INCREMENT |
| Backtest_Run_ID | VARCHAR(50) | NOT NULL |
| Selection_Date | DATE | NOT NULL |
| Lookback_Period_Days | INT | NOT NULL |
| ETF_ID | INT | FOREIGN KEY → ETF_Master(ETF_ID) |
| Ticker_Symbol | VARCHAR(10) | NOT NULL |
| Asset_Type | VARCHAR(50) | |
| Momentum_Score | DECIMAL(12,6) | |
| Portfolio_Rank | INT | |
| Portfolio_Weight | DECIMAL(5,4) | |
| Entry_Price | DECIMAL(12,4) | |
| Exit_Price | DECIMAL(12,4) | |
| Holding_Return | DECIMAL(12,6) | |

---

## 🧪 Testing

### Manual Testing Steps

1. **Auto-Initialization** (First Run):
   ```bash
   python main.py
   # System automatically creates database and loads data
   # Verify: See "✓ System setup complete!" message
   ```

2. **Backtesting**:
   ```bash
   # Menu 1.1 - Run standard backtest
   # Verify: Results logged to Strategy_Log table
   ```

3. **Analytics**:
   ```bash
   # Menu 2.1 - Generate all insights
   # Verify: Three complex SQL queries execute successfully
   ```

4. **CRUD Operations**:
   ```bash
   # Menu 3.1 - Read results
   # Menu 3.4 - Update a price
   # Menu 3.5 - Delete old logs
   ```

5. **Excel Export**:
   ```bash
   # Menu 4.5 - Export all tables to Excel
   # Verify: Excel files created in data/ folder
   ```

---

## 📝 Project Structure

```
etf_backtester/
│
├── main.py                    # CLI entry point
│
├── sql/
│   └── database.sql           # Database schema with PK/FK
│
├── modules/
│   ├── db_connector.py        # Database connection pooling
│   ├── data_loader.py         # Generate & load sample data
│   ├── backtest_engine.py     # SQL-focused momentum strategy
│   ├── analytics.py           # 3 complex SQL analytics queries
│   ├── crud_operations.py     # CRUD operations
│   └── text_logger.py         # Text file logging
│
└── logs/
    └── backtest_log_*.txt     # Generated log files
```

---

## 👥 Team Responsibilities

| Member | Responsibility | SQL Insight Focus |
|--------|---------------|-------------------|
| Member #1 | Volatility Analysis | Calculate standard deviation of returns by Asset_Type |
| Member #2 | Lookback Optimization | Compare CAGR across different lookback periods |
| Member #3 | Drawdown Analysis | Identify asset types held during max drawdown |

---

## ⚠️ Troubleshooting

### Connection Error

**Error**: `Cannot connect to database`

**Solution**:
- Verify MySQL is running: `sudo service mysql status`
- Check credentials in `modules/db_connector.py`
- Ensure database exists: `SHOW DATABASES;`

### Import Error

**Error**: `ModuleNotFoundError: No module named 'mysql.connector'`

**Solution**:
```bash
pip install mysql-connector-python
```

### Empty Data Error

**Error**: `No price data available`

**Solution**:
- Drop the database and re-run: `DROP DATABASE etf_backtester_db;`
- Restart the program: `python main.py`
- System will auto-initialize and reload all data

---

## 📚 References

- MySQL Documentation: https://dev.mysql.com/doc/
- Python mysql-connector: https://dev.mysql.com/doc/connector-python/en/
- Momentum Strategy Research: https://www.investopedia.com/momentum-investing-4161380

---

## 📄 License

This project is created for educational purposes as part of the DADS 4002 course.

---

## ✨ Features Summary

- ✅ **Auto-initialization**: Intelligent setup on first run (no manual configuration!)
- ✅ **SQL Data Files**: Load real Yahoo Finance data via SQL INSERT statements
- ✅ Fully integrated Python + MySQL system
- ✅ SQL-focused momentum calculation
- ✅ 3 complex SQL analytics queries
- ✅ CRUD operations for data management
- ✅ Text file logging for record-keeping
- ✅ Excel export functionality for data sharing
- ✅ Clean, modular architecture
- ✅ Comprehensive CLI interface
- ✅ 50 real ETFs across 4 asset types
- ✅ 10 years of weekly historical data from Yahoo Finance
- ✅ Real market data (not synthetic)
- ✅ Multiple backtest configurations
- ✅ Actionable insights generation
- ✅ Production-ready user experience
- ✅ Team collaboration support (share identical datasets)

---

**Made with ❤️ for DADS 4002**
