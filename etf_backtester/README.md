# ETF Portfolio Backtester

**DADS 4002 Course Project**
Simple 50-ETF Momentum Strategy Backtesting System

---

## 📋 Project Overview

This project implements a **Simple 50-ETF Portfolio Strategy Backtester** using:
- **Database**: MySQL (Relational Database)
- **Interface**: Python Command Line Interface (CLI)
- **Strategy**: Momentum-based ETF selection
- **Focus**: SQL-focused analytics and actionable insights

The system allows users to backtest momentum-based trading strategies on a portfolio of 50 ETFs across different asset classes (Equity, Bond, Commodity, Mixed) and generate actionable insights using complex SQL queries.

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
- [x] **Data Volume**: 30+ rows per table (Price_Data has 36,500+ rows)

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
   pip install mysql-connector-python
   ```

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

### Quick Start (First Time Setup)

1. **Run the main program**:
   ```bash
   python main.py
   ```

2. **Initialize the database** (Menu 1.1):
   - Creates all tables with proper schema
   - Sets up views and constraints

3. **Load sample data** (Menu 1.2):
   - Loads 50 ETFs across 4 asset types
   - Generates 730 days (2 years) of price data

4. **Run a backtest** (Menu 2.1):
   - Executes standard momentum strategy
   - Logs results to database and text file

5. **Generate insights** (Menu 3.1):
   - Produces all three analytical insights

### Main Menu Options

```
[1] Setup & Data Management
  1.1 - Initialize Database (Run SQL Schema)
  1.2 - Load Sample ETF Data
  1.3 - View Database Status

[2] Run Backtest
  2.1 - Run Standard Backtest (90-day lookback)
  2.2 - Run Custom Backtest (specify parameters)
  2.3 - Run Comparative Backtest (3M vs 6M)

[3] Analytics & Insights
  3.1 - Generate All Insights
  3.2 - Insight #1: Volatility Analysis
  3.3 - Insight #2: Lookback Period Comparison
  3.4 - Insight #3: Drawdown Analysis

[4] CRUD Operations
  4.1 - Read: View Backtest Results
  4.2 - Read: View All Backtest Runs
  4.3 - Read: View ETF Information
  4.4 - Update: Modify Price Data
  4.5 - Delete: Remove Old Backtest Logs

[5] Reports & Logs
  5.1 - View Text Logs
  5.2 - Export Latest Results to Text

[0] Exit
```

---

## 📊 Strategy Explanation

### Momentum Strategy

The backtester implements a **momentum-based portfolio selection strategy**:

1. **Lookback Period**: Analyze ETF performance over the past N days (e.g., 90 or 180 days)

2. **Selection**: Calculate momentum score for each ETF:
   ```
   Momentum Score = ((End_Price - Start_Price) / Start_Price) × 100
   ```

3. **Portfolio Construction**:
   - Select top 3-5 ETFs with highest momentum scores
   - Equal-weight allocation

4. **Rebalancing**: Re-evaluate and rebalance portfolio every N days (e.g., 30 days)

5. **Performance Tracking**: Calculate returns for each holding period

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

1. **Database Connectivity**:
   ```bash
   python main.py
   # Select menu 1.3 to view database status
   ```

2. **Data Loading**:
   ```bash
   # Menu 1.2 - Should load 50 ETFs and 36,500+ price records
   ```

3. **Backtesting**:
   ```bash
   # Menu 2.1 - Run standard backtest
   # Verify: Results logged to Strategy_Log table
   ```

4. **CRUD Operations**:
   ```bash
   # Menu 4.1 - Read results
   # Menu 4.4 - Update a price
   # Menu 4.5 - Delete old logs
   ```

5. **Analytics**:
   ```bash
   # Menu 3.1 - Generate all insights
   # Verify: Three complex SQL queries execute successfully
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
- Run Menu 1.2 to load sample data
- Verify: Menu 1.3 should show row counts

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

- ✅ Fully integrated Python + MySQL system
- ✅ SQL-focused momentum calculation
- ✅ 3 complex SQL analytics queries
- ✅ CRUD operations for data management
- ✅ Text file logging for record-keeping
- ✅ Clean, modular architecture
- ✅ Comprehensive CLI interface
- ✅ 50 ETFs across 4 asset types
- ✅ 730 days of historical data
- ✅ Multiple backtest configurations
- ✅ Actionable insights generation

---

**Made with ❤️ for DADS 4002**
