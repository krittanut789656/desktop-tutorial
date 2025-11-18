# Portfolio Backtesting System

Portfolio backtesting system with SQL-focused analytics and benchmark comparison.

## 📋 Project Structure

```
desktop-tutorial/
├── data/
│   ├── etf_list.csv                    # 50 ETFs metadata
│   ├── etf_price_history.csv           # 208,700 price records (local only)
│   ├── benchmark_portfolios.csv        # 35 benchmark portfolios
│   └── benchmark_holdings.csv          # 117 holdings (weights)
├── database/
│   └── schema.sql                      # MySQL schema (9 tables)
├── scripts/
│   ├── download_etf_data.py            # Download real data (yfinance)
│   ├── download_etf_data_simple.py     # Download using requests
│   ├── generate_sample_data.py         # Generate simulated data
│   └── import_to_mysql.py              # Import all data to MySQL
└── requirements.txt                    # Python dependencies
```

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download ETF Data (Optional - already have sample data)

```bash
cd scripts
python download_etf_data.py
```

Or use sample data already generated (208,700 rows).

### Step 3: Setup MySQL Database

Make sure MySQL is running on your machine, then update credentials in `scripts/import_to_mysql.py`:

```python
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password'
}
```

### Step 4: Import Data to MySQL

```bash
cd scripts
python import_to_mysql.py
```

This will:
- ✅ Create database `portfolio_backtesting`
- ✅ Create 9 tables with proper relationships
- ✅ Import 50 ETFs
- ✅ Import 208,700+ price records
- ✅ Import 35 benchmark portfolios
- ✅ Import 117 benchmark holdings

## 📊 Database Schema

### Tables Overview

| Table | Rows | Description |
|-------|------|-------------|
| `etf_master` | 50 | ETF metadata |
| `price_history` | 208,700+ | Historical prices |
| `benchmark_portfolios` | 35 | Famous portfolios |
| `benchmark_holdings` | 117 | Portfolio allocations |
| `backtest_scenarios` | User-created | Backtest scenarios |
| `scenario_holdings` | User-created | Scenario allocations |
| `backtest_results` | Calculated | Backtest results |
| `portfolio_snapshots` | Generated | Portfolio snapshots |
| `transaction_log` | Generated | Transaction history |

**Total: 9 tables with Primary Keys, Foreign Keys, and proper indexes**

## 🎯 Key Features

### 1. Comprehensive ETF Coverage

- **US Equity**: 27 ETFs (Large/Small Cap, Growth/Value, Sectors)
- **International**: 6 ETFs (Developed + Emerging Markets)
- **Bonds**: 10 ETFs (Government, Corporate, International)
- **Commodities**: 5 ETFs (Gold, Silver, Oil, Gas)
- **REITs**: 2 ETFs (US + International)

### 2. Famous Benchmark Portfolios (35)

- Traditional 60/40, 80/20, 40/60
- Ray Dalio's All Weather
- Harry Browne's Permanent Portfolio
- Bogleheads Three-Fund
- And 28 more...

### 3. SQL-Focused Analytics (11 Insights)

1. Best Performing ETFs
2. Volatility Analysis
3. Correlation Analysis
4. Maximum Drawdown
5. Asset Class Performance
6. Rebalancing vs Buy & Hold
7. Optimal Rebalancing Frequency
8. Expense Ratio Impact
9. Concentration Risk
10. Dollar Cost Averaging Effectiveness
11. **Portfolio vs Benchmark Comparison** (NEW!)

## 📦 Data Files

### ETF List (`data/etf_list.csv`)
50 ETFs with metadata (ticker, name, asset class, sector, expense ratio)

### Price History (`data/etf_price_history.csv`)
- **Rows**: 208,700
- **Period**: 2009-01-01 to 2024-12-31
- **Columns**: ticker, date, open, high, low, close, adj_close, volume

### Benchmark Portfolios (`data/benchmark_portfolios.csv`)
35 famous portfolios with risk levels and descriptions

### Benchmark Holdings (`data/benchmark_holdings.csv`)
117 allocation weights (which ETFs in which portfolio)

## 🔧 Next Steps

After importing data:

1. Create Python modules (main.py, analytics.py)
2. Implement 11 SQL insights
3. Build CRUD operations
4. Add text file operations
5. Create ER Diagram
6. Test and demo

## 📝 Notes

- **Sample data** is simulated using Geometric Brownian Motion
- For **real data**, use `download_etf_data.py` with yfinance
- All SQL queries emphasize SQL over pandas
- Benchmark comparison is the unique feature

## 👥 Team

- สมาชิก 1: ETF Analysis & Performance Metrics
- สมาชิก 2: Strategy Comparison & Risk Analysis
- สมาชิก 3: Benchmark Comparison & Insights

## 🤖 AI Tool

Using **Claude Code** for:
- SQL query generation
- Database schema design
- Code debugging
- Documentation
