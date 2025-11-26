-- ============================================================================
-- ETF BACKTESTER DATABASE SCHEMA
-- MySQL Database Schema with All Required Tables
-- ============================================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS etf_backtester_db;
USE etf_backtester_db;

-- ============================================================================
-- TABLE 1: ETF_Master
-- Stores master list of ETFs
-- ============================================================================
CREATE TABLE IF NOT EXISTS ETF_Master (
    ETF_ID INT PRIMARY KEY,
    Ticker_Symbol VARCHAR(10) NOT NULL UNIQUE,
    ETF_Name VARCHAR(255) NOT NULL,
    Asset_Type VARCHAR(50) NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_ticker (Ticker_Symbol),
    INDEX idx_asset_type (Asset_Type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 2: Price_Data
-- Stores daily price data for all ETFs
-- ============================================================================
CREATE TABLE IF NOT EXISTS Price_Data (
    Price_ID INT AUTO_INCREMENT PRIMARY KEY,
    ETF_ID INT NOT NULL,
    Price_Date DATE NOT NULL,
    Open_Price DECIMAL(12, 4),
    High_Price DECIMAL(12, 4),
    Low_Price DECIMAL(12, 4),
    Close_Price DECIMAL(12, 4) NOT NULL,
    Volume BIGINT,
    Daily_Return DECIMAL(10, 6),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID) ON DELETE CASCADE,
    UNIQUE KEY unique_etf_date (ETF_ID, Price_Date),
    INDEX idx_date (Price_Date),
    INDEX idx_etf_date (ETF_ID, Price_Date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- TABLE 3: Strategy_Log
-- Stores backtest results and strategy selections
-- ============================================================================
CREATE TABLE IF NOT EXISTS Strategy_Log (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    Backtest_Run_ID VARCHAR(50) NOT NULL,
    ETF_ID INT NOT NULL,
    Selection_Date DATE NOT NULL,
    Momentum_Score DECIMAL(10, 4),
    Portfolio_Rank INT,
    Asset_Type VARCHAR(50),
    Entry_Price DECIMAL(12, 4),
    Exit_Price DECIMAL(12, 4),
    Holding_Return DECIMAL(10, 6),
    Run_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID) ON DELETE CASCADE,
    INDEX idx_backtest_run (Backtest_Run_ID),
    INDEX idx_selection_date (Selection_Date),
    INDEX idx_run_date (Run_Date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- SAMPLE DATA INSERTION (Optional - for testing)
-- ============================================================================

-- Insert Sample ETFs
INSERT INTO ETF_Master (ETF_ID, Ticker_Symbol, ETF_Name, Asset_Type) VALUES
(1, 'SPY', 'SPDR S&P 500 ETF Trust', 'Equity'),
(2, 'QQQ', 'Invesco QQQ Trust', 'Equity'),
(3, 'AGG', 'iShares Core U.S. Aggregate Bond ETF', 'Fixed Income'),
(4, 'GLD', 'SPDR Gold Trust', 'Commodity'),
(5, 'TLT', 'iShares 20+ Year Treasury Bond ETF', 'Fixed Income'),
(6, 'VTI', 'Vanguard Total Stock Market ETF', 'Equity'),
(7, 'IWM', 'iShares Russell 2000 ETF', 'Equity'),
(8, 'EFA', 'iShares MSCI EAFE ETF', 'Equity'),
(9, 'SHY', 'iShares 1-3 Year Treasury Bond ETF', 'Fixed Income'),
(10, 'DBC', 'Invesco DB Commodity Index Tracking Fund', 'Commodity')
ON DUPLICATE KEY UPDATE ETF_Name = VALUES(ETF_Name);

-- ============================================================================
-- USEFUL QUERIES
-- ============================================================================

-- View all ETFs
-- SELECT * FROM ETF_Master ORDER BY Ticker_Symbol;

-- View latest prices
-- SELECT em.Ticker_Symbol, pd.Price_Date, pd.Close_Price
-- FROM Price_Data pd
-- JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
-- WHERE pd.Price_Date = (SELECT MAX(Price_Date) FROM Price_Data)
-- ORDER BY em.Ticker_Symbol;

-- View backtest summary
-- SELECT
--     Backtest_Run_ID,
--     COUNT(*) as Total_Selections,
--     AVG(Momentum_Score) as Avg_Momentum,
--     MIN(Selection_Date) as Start_Date,
--     MAX(Selection_Date) as End_Date
-- FROM Strategy_Log
-- GROUP BY Backtest_Run_ID
-- ORDER BY Run_Date DESC;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
