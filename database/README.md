# ETF Backtester Database Setup

## Overview
This directory contains the database schema and data files for the ETF Backtester project (DADS 4002 Course Project).

## Database Structure

### Tables
1. **ETF_Master** - Master table containing metadata for 50 real ETFs
2. **Price_Data** - Historical weekly price data from Yahoo Finance
3. **Strategy_Log** - Logs for backtest runs and portfolio selections

### Views
- **vw_latest_prices** - Latest price for each ETF
- **vw_portfolio_summary** - Portfolio performance summary

### Triggers
- **validate_price_data** - Validates price data integrity before insertion

## Directory Structure
```
database/
├── schema/
│   └── 01_create_schema.sql    # Database and table creation
├── data/
│   └── 02_load_etf_master.sql  # ETF master data (50 ETFs)
├── setup.sh                     # Helper script to run all SQL files
└── README.md                    # This file
```

## Setup Instructions

### Prerequisites
- MySQL 5.7+ or MariaDB 10.2+
- Database user with CREATE DATABASE privileges

### Option 1: Using the Setup Script (Recommended)

```bash
# Make the script executable
chmod +x database/setup.sh

# Run with default settings (localhost, root user)
./database/setup.sh

# Run with custom settings
./database/setup.sh <host> <username> <password>
```

### Option 2: Manual Setup

```bash
# 1. Create the database and schema
mysql -u root -p < database/schema/01_create_schema.sql

# 2. Load ETF master data
mysql -u root -p < database/data/02_load_etf_master.sql
```

### Option 3: Using MySQL Command Line

```bash
# Connect to MySQL
mysql -u root -p

# Run the SQL files
source database/schema/01_create_schema.sql;
source database/data/02_load_etf_master.sql;
```

## Verification

After running the setup, verify the data was loaded correctly:

```sql
USE etf_backtester_db;

-- Check total number of ETFs
SELECT COUNT(*) as Total_ETFs FROM ETF_Master;
-- Expected: 50

-- Check ETFs by asset type
SELECT
    Asset_Type,
    COUNT(*) as ETF_Count
FROM ETF_Master
GROUP BY Asset_Type
ORDER BY Asset_Type;
-- Expected:
-- Bond: 15
-- Commodity: 5
-- Equity: 25
-- Mixed: 5

-- View all tables
SHOW TABLES;
-- Expected: ETF_Master, Price_Data, Strategy_Log, vw_latest_prices, vw_portfolio_summary

-- View sample ETFs
SELECT * FROM ETF_Master LIMIT 10;
```

## ETF Data Summary

### Total: 50 Real, Tradeable ETFs

- **Equity (25)**: Large-cap, Mid-cap, Sector funds, Growth, Value, International
  - Examples: SPY, QQQ, IWM, VTI, VOO, ARKK, XLF, XLE, XLK

- **Bond (15)**: Government, Corporate, High-Yield, Municipal, International
  - Examples: AGG, BND, TLT, IEF, SHY, LQD, HYG, MUB, TIP

- **Commodity (5)**: Gold, Silver, Oil, Agriculture, Commodity Index
  - Examples: GLD, SLV, USO, DBA, DBC

- **Mixed (5)**: Balanced allocation funds
  - Examples: AOR, AOM, AOK, GAL, INKM

All ETFs are sourced from Yahoo Finance and are actively traded securities.

## Next Steps

After loading the ETF master data, you'll need to:

1. **Load Historical Price Data** - Import weekly price data for all 50 ETFs
2. **Implement Backtesting Logic** - Create Python/R scripts to calculate momentum scores
3. **Run Backtests** - Execute strategy and populate Strategy_Log table
4. **Analyze Results** - Query the database for performance metrics

## Database Configuration

### Connection Settings
- **Database Name**: `etf_backtester_db`
- **Default Host**: `localhost`
- **Default Port**: `3306`
- **Character Set**: `utf8mb4`
- **Collation**: `utf8mb4_unicode_ci`
- **Engine**: `InnoDB`

### Security Notes
- The schema includes CASCADE DELETE - be careful when deleting ETFs
- Triggers validate price data integrity
- Consider creating a read-only user for analysis queries

## Troubleshooting

### Common Issues

1. **"Access denied" error**
   - Ensure your MySQL user has CREATE DATABASE privileges
   - Check username and password

2. **"Database exists" error**
   - The schema script drops and recreates the database
   - Ensure you have backup if you have existing data

3. **Character encoding issues**
   - Ensure your MySQL server supports utf8mb4
   - Check client connection charset settings

4. **Trigger creation fails**
   - Ensure DELIMITER is supported in your MySQL client
   - Some GUI tools may require manual delimiter handling

## Support

For questions or issues:
- Review the SQL comments in the schema files
- Check MySQL error logs: `/var/log/mysql/error.log`
- Verify MySQL version compatibility

## License

DADS 4002 Course Project - For Educational Purposes
