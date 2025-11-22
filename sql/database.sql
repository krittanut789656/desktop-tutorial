-- ===================================================================
-- ETF Backtester Database Schema
-- ===================================================================
-- Description: MySQL database schema for ETF backtesting system
--              with real Yahoo Finance data
-- Created: 2025-01-19
-- Database: etf_backtester_db
-- Tables: ETF_Master, Price_Data, Strategy_Log
-- ===================================================================

-- Drop database if exists and create new one
DROP DATABASE IF EXISTS etf_backtester_db;
CREATE DATABASE etf_backtester_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE etf_backtester_db;

-- ===================================================================
-- Table: ETF_Master
-- ===================================================================
-- Description: Master table for ETF definitions and metadata
-- Contains: 50 real tradeable ETFs across 4 asset types
-- Asset Types:
--   - Equity: 25 ETFs (SPY, QQQ, IWM, VOO, VTI, sector ETFs, ARK funds)
--   - Bond: 15 ETFs (AGG, BND, TLT, corporate bonds, muni bonds)
--   - Commodity: 5 ETFs (GLD, SLV, USO, DBA, DBC)
--   - Mixed: 5 ETFs (AOR, AOM, AOK, allocation funds)
-- ===================================================================

CREATE TABLE ETF_Master (
    ETF_ID INT AUTO_INCREMENT PRIMARY KEY,
    Ticker VARCHAR(10) NOT NULL UNIQUE,
    ETF_Name VARCHAR(255) NOT NULL,
    Asset_Type ENUM('Equity', 'Bond', 'Commodity', 'Mixed') NOT NULL,
    Expense_Ratio DECIMAL(5, 4) NULL COMMENT 'Annual expense ratio (e.g., 0.0003 = 0.03%)',
    Inception_Date DATE NULL COMMENT 'ETF inception date',
    Description TEXT NULL COMMENT 'ETF description and strategy',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_asset_type (Asset_Type),
    INDEX idx_ticker (Ticker)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Master table containing ETF definitions and metadata';

-- ===================================================================
-- Table: Price_Data
-- ===================================================================
-- Description: Historical price data from Yahoo Finance
-- Data Source: Yahoo Finance API (via yfinance)
-- Frequency: Weekly (every Monday or first trading day of week)
-- History: 10 years from current date
-- Fields: OHLC prices (Open, High, Low, Close, Adjusted Close, Volume)
-- Expected Records: 26,000+ (50 ETFs × ~520 weeks)
-- ===================================================================

CREATE TABLE Price_Data (
    Price_ID INT AUTO_INCREMENT PRIMARY KEY,
    ETF_ID INT NOT NULL,
    Price_Date DATE NOT NULL,
    Open_Price DECIMAL(12, 4) NOT NULL COMMENT 'Opening price',
    High_Price DECIMAL(12, 4) NOT NULL COMMENT 'Highest price of the day',
    Low_Price DECIMAL(12, 4) NOT NULL COMMENT 'Lowest price of the day',
    Close_Price DECIMAL(12, 4) NOT NULL COMMENT 'Closing price',
    Adj_Close DECIMAL(12, 4) NOT NULL COMMENT 'Adjusted closing price (accounts for splits, dividends)',
    Volume BIGINT NOT NULL COMMENT 'Trading volume',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    UNIQUE KEY unique_etf_date (ETF_ID, Price_Date),
    INDEX idx_etf_id (ETF_ID),
    INDEX idx_price_date (Price_Date),
    INDEX idx_etf_date (ETF_ID, Price_Date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Historical weekly price data from Yahoo Finance';

-- ===================================================================
-- Table: Strategy_Log
-- ===================================================================
-- Description: Log table for backtesting strategies and system events
-- Purpose: Track strategy execution, performance, and system activities
-- ===================================================================

CREATE TABLE Strategy_Log (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    ETF_ID INT NULL,
    Strategy_Name VARCHAR(100) NULL COMMENT 'Name of the strategy being tested',
    Backtest_ID VARCHAR(50) NULL COMMENT 'Unique identifier for backtest run',
    Log_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Start_Date DATE NULL COMMENT 'Strategy backtest start date',
    End_Date DATE NULL COMMENT 'Strategy backtest end date',
    Initial_Capital DECIMAL(15, 2) NULL COMMENT 'Starting capital for backtest',
    Final_Value DECIMAL(15, 2) NULL COMMENT 'Ending portfolio value',
    Total_Return DECIMAL(10, 4) NULL COMMENT 'Total return percentage',
    Sharpe_Ratio DECIMAL(10, 4) NULL COMMENT 'Risk-adjusted return metric',
    Max_Drawdown DECIMAL(10, 4) NULL COMMENT 'Maximum drawdown percentage',
    Number_Of_Trades INT NULL COMMENT 'Total number of trades executed',
    Log_Type ENUM('INFO', 'WARNING', 'ERROR', 'SUCCESS') DEFAULT 'INFO',
    Description TEXT NULL COMMENT 'Detailed log message or notes',
    Parameters JSON NULL COMMENT 'Strategy parameters in JSON format',

    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    INDEX idx_strategy_name (Strategy_Name),
    INDEX idx_backtest_id (Backtest_ID),
    INDEX idx_log_date (Log_Date),
    INDEX idx_log_type (Log_Type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Log table for strategy backtesting and system events';

-- ===================================================================
-- Sample Verification Queries
-- ===================================================================
-- Uncomment to test after loading data:

-- Check ETF count (Expected: 50)
-- SELECT COUNT(*) as Total_ETFs FROM ETF_Master;

-- Check ETF breakdown by asset type
-- SELECT Asset_Type, COUNT(*) as Count
-- FROM ETF_Master
-- GROUP BY Asset_Type
-- ORDER BY Asset_Type;

-- Check price data count (Expected: 26,000+)
-- SELECT COUNT(*) as Total_Price_Records FROM Price_Data;

-- Check date range and coverage
-- SELECT
--     MIN(Price_Date) as Earliest_Date,
--     MAX(Price_Date) as Latest_Date,
--     COUNT(DISTINCT Price_Date) as Unique_Dates,
--     COUNT(DISTINCT ETF_ID) as Unique_ETFs
-- FROM Price_Data;

-- Check data completeness per ETF
-- SELECT
--     e.Ticker,
--     e.ETF_Name,
--     COUNT(p.Price_ID) as Price_Records,
--     MIN(p.Price_Date) as First_Date,
--     MAX(p.Price_Date) as Last_Date
-- FROM ETF_Master e
-- LEFT JOIN Price_Data p ON e.ETF_ID = p.ETF_ID
-- GROUP BY e.ETF_ID, e.Ticker, e.ETF_Name
-- ORDER BY e.Ticker;

-- ===================================================================
-- Usage Instructions
-- ===================================================================
--
-- Load this schema file:
--   mysql -u root -p < sql/database.sql
--
-- Or from MySQL prompt:
--   SOURCE sql/database.sql;
--
-- Next steps:
--   1. Load ETF Master data: SOURCE sql/etf_master_data.sql;
--   2. Load Price data: SOURCE sql/price_data_YYYYMMDD_HHMMSS.sql;
--   Or load complete dataset: SOURCE sql/complete_data_YYYYMMDD_HHMMSS.sql;
--
-- ===================================================================

-- Success message
SELECT 'Database schema created successfully!' as Status,
       'etf_backtester_db' as Database_Name,
       '3 tables created: ETF_Master, Price_Data, Strategy_Log' as Tables;
