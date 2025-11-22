# ETF Backtester - DADS 4002 Course Project

A comprehensive portfolio backtesting system using 50 real ETFs across multiple asset classes, implementing momentum-based trading strategies.

## Project Overview

This project implements a database-driven backtesting system for ETF (Exchange-Traded Fund) portfolio strategies. The system tracks 50 real, tradeable ETFs and simulates momentum-based trading strategies using historical price data from Yahoo Finance.

### Key Features

- **50 Real ETFs** across 4 asset types (Equity, Bond, Commodity, Mixed)
- **MySQL Database** with normalized schema and performance views
- **Momentum Strategy** implementation with configurable lookback periods
- **Historical Price Data** support (weekly intervals)
- **Backtesting Framework** for portfolio performance analysis
- **Data Validation** with MySQL triggers

## Database Structure

### Tables

1. **ETF_Master** - Master table containing metadata for 50 ETFs
   - Ticker symbols, names, asset types
   - Expense ratios and inception dates
   - Indexed for fast lookup

2. **Price_Data** - Historical weekly price data
   - OHLCV (Open, High, Low, Close, Volume)
   - Adjusted close prices
   - Unique constraints to prevent duplicates

3. **Strategy_Log** - Backtest execution logs
   - Portfolio selections and rankings
   - Entry/exit prices and returns
   - Momentum scores and weights

### Views

- **vw_latest_prices** - Latest price for each ETF
- **vw_portfolio_summary** - Portfolio performance aggregation

### ETF Breakdown

- **Equity (25 ETFs)**: SPY, QQQ, IWM, VTI, VOO, DIA, IVV, VEA, VWO, EFA, VUG, VTV, XLF, XLE, XLK, XLV, XLI, XLY, XLP, XLU, ARKK, ARKW, ARKG, ARKF, SOXX
- **Bond (15 ETFs)**: AGG, BND, TLT, IEF, SHY, LQD, HYG, MUB, TIP, VCIT, VCSH, BNDX, EMB, JNK, GOVT
- **Commodity (5 ETFs)**: GLD, SLV, USO, DBA, DBC
- **Mixed (5 ETFs)**: AOR, AOM, AOK, GAL, INKM

## Quick Start

### Prerequisites

- MySQL 5.7+ or MariaDB 10.2+
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd desktop-tutorial
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   # Option 1: Using the setup script (recommended)
   cd database
   ./setup.sh

   # Option 2: Manual setup
   mysql -u root -p < database/schema/01_create_schema.sql
   mysql -u root -p < database/data/02_load_etf_master.sql
   ```

4. **Verify installation**
   ```bash
   mysql -u root -p etf_backtester_db -e "SELECT COUNT(*) as Total_ETFs FROM ETF_Master;"
   ```
   Expected output: `Total_ETFs: 50`

## Project Structure

```
desktop-tutorial/
├── database/
│   ├── schema/
│   │   └── 01_create_schema.sql       # Database schema
│   ├── data/
│   │   └── 02_load_etf_master.sql     # ETF master data
│   ├── setup.sh                        # Automated setup script
│   ├── example_connection.py          # Python connection example
│   └── README.md                       # Database documentation
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Usage Examples

### Python Database Connection

```python
from database.example_connection import ETFDatabase

# Connect to database
db = ETFDatabase(
    host='localhost',
    user='root',
    password='your_password',
    database='etf_backtester_db'
)

if db.connect():
    # Get all ETFs
    etfs = db.get_all_etfs()
    print(etfs)

    # Get equity ETFs only
    equity_etfs = db.get_etfs_by_asset_type('Equity')
    print(equity_etfs)

    # Get ETF summary
    summary = db.get_etf_summary()
    print(summary)

    db.disconnect()
```

### SQL Queries

```sql
-- Get all equity ETFs with low expense ratios
SELECT Ticker_Symbol, ETF_Name, Expense_Ratio
FROM ETF_Master
WHERE Asset_Type = 'Equity' AND Expense_Ratio < 0.10
ORDER BY Expense_Ratio;

-- View ETF distribution by asset type
SELECT
    Asset_Type,
    COUNT(*) as ETF_Count,
    AVG(Expense_Ratio) as Avg_Expense_Ratio
FROM ETF_Master
GROUP BY Asset_Type;
```

## Development Roadmap

### Phase 1: Database Setup ✅
- [x] Create database schema
- [x] Load ETF master data
- [x] Create setup scripts
- [x] Add example connection code

### Phase 2: Data Collection
- [ ] Implement Yahoo Finance data fetcher
- [ ] Load historical price data (2010-present)
- [ ] Validate price data integrity
- [ ] Set up automated data updates

### Phase 3: Backtesting Engine
- [ ] Implement momentum calculation
- [ ] Create portfolio selection logic
- [ ] Run historical backtests
- [ ] Generate performance reports

### Phase 4: Analysis & Visualization
- [ ] Create performance dashboards
- [ ] Generate statistical reports
- [ ] Compare strategy variants
- [ ] Export results

## Database Configuration

**Connection Details:**
- Database Name: `etf_backtester_db`
- Host: `localhost`
- Port: `3306`
- Character Set: `utf8mb4`
- Engine: `InnoDB`

**Security Notes:**
- Use strong passwords for production
- Create read-only users for analysis
- Regular backups recommended
- Be cautious with CASCADE DELETE

## Contributing

This is a course project for DADS 4002. For questions or issues:

1. Check the database README: `database/README.md`
2. Review SQL comments in schema files
3. Test queries using the example connection script

## Data Sources

- **ETF Data**: Yahoo Finance (via yfinance API)
- **All 50 ETFs**: Real, actively traded securities
- **Price Data**: Historical weekly OHLCV data
- **Expense Ratios**: Approximate annual percentages

## License

Educational project for DADS 4002 - For academic purposes only.

## Acknowledgments

- Yahoo Finance for providing free historical ETF data
- DADS 4002 Course instructors and teaching staff
