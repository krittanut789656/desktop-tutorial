-- =====================================================
-- Simple 50-ETF Portfolio Backtester Database Schema
-- DADS 4002 Course Project
-- =====================================================

-- Drop existing database if exists and create fresh
DROP DATABASE IF EXISTS etf_backtester_db;
CREATE DATABASE etf_backtester_db;
USE etf_backtester_db;

-- =====================================================
-- Table 1: ETF_Master
-- Master table containing ETF metadata
-- =====================================================
CREATE TABLE ETF_Master (
    ETF_ID INT PRIMARY KEY AUTO_INCREMENT,
    Ticker_Symbol VARCHAR(10) NOT NULL UNIQUE,
    ETF_Name VARCHAR(100) NOT NULL,
    Asset_Type VARCHAR(50) NOT NULL,  -- e.g., 'Equity', 'Bond', 'Commodity', 'Mixed'
    Expense_Ratio DECIMAL(5,4),
    Inception_Date DATE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_type (Asset_Type),
    INDEX idx_ticker (Ticker_Symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table 2: Price_Data
-- Historical daily price data for all ETFs
-- =====================================================
CREATE TABLE Price_Data (
    Price_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    ETF_ID INT NOT NULL,
    Price_Date DATE NOT NULL,
    Open_Price DECIMAL(12,4),
    High_Price DECIMAL(12,4),
    Low_Price DECIMAL(12,4),
    Close_Price DECIMAL(12,4) NOT NULL,
    Adj_Close_Price DECIMAL(12,4),
    Volume BIGINT,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Key Constraint
    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Unique constraint to prevent duplicate data for same ETF on same date
    UNIQUE KEY unique_etf_date (ETF_ID, Price_Date),

    -- Indexes for query performance
    INDEX idx_etf_date (ETF_ID, Price_Date),
    INDEX idx_date (Price_Date),
    INDEX idx_etf_id (ETF_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table 3: Strategy_Log
-- Logs backtest runs and portfolio selections
-- =====================================================
CREATE TABLE Strategy_Log (
    Log_ID INT PRIMARY KEY AUTO_INCREMENT,
    Backtest_Run_ID VARCHAR(50) NOT NULL,
    Run_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Strategy_Name VARCHAR(100) DEFAULT 'Momentum Strategy',
    Lookback_Period_Days INT NOT NULL,
    Selection_Date DATE NOT NULL,
    ETF_ID INT NOT NULL,
    Ticker_Symbol VARCHAR(10) NOT NULL,
    Asset_Type VARCHAR(50),
    Momentum_Score DECIMAL(12,6),  -- Calculated return over lookback period
    Portfolio_Rank INT,  -- Rank 1-5 for top selections
    Portfolio_Weight DECIMAL(5,4) DEFAULT 0.2000,  -- Equal weight for simplicity
    Entry_Price DECIMAL(12,4),
    Exit_Price DECIMAL(12,4),
    Holding_Return DECIMAL(12,6),  -- Return during holding period
    Notes TEXT,

    -- Foreign Key Constraint
    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Indexes for query performance
    INDEX idx_run_id (Backtest_Run_ID),
    INDEX idx_selection_date (Selection_Date),
    INDEX idx_etf_id (ETF_ID),
    INDEX idx_lookback (Lookback_Period_Days),
    INDEX idx_asset_type (Asset_Type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Additional Views for Quick Analytics
-- =====================================================

-- View: Latest Price for Each ETF
CREATE VIEW vw_latest_prices AS
SELECT
    em.ETF_ID,
    em.Ticker_Symbol,
    em.ETF_Name,
    em.Asset_Type,
    pd.Price_Date,
    pd.Close_Price,
    pd.Volume
FROM ETF_Master em
INNER JOIN Price_Data pd ON em.ETF_ID = pd.ETF_ID
INNER JOIN (
    SELECT ETF_ID, MAX(Price_Date) as Max_Date
    FROM Price_Data
    GROUP BY ETF_ID
) latest ON pd.ETF_ID = latest.ETF_ID AND pd.Price_Date = latest.Max_Date;

-- View: Portfolio Performance Summary
CREATE VIEW vw_portfolio_summary AS
SELECT
    Backtest_Run_ID,
    Strategy_Name,
    Lookback_Period_Days,
    Selection_Date,
    COUNT(DISTINCT ETF_ID) as Num_ETFs_Selected,
    AVG(Momentum_Score) as Avg_Momentum_Score,
    AVG(Holding_Return) as Avg_Return,
    SUM(Holding_Return * Portfolio_Weight) as Weighted_Return
FROM Strategy_Log
WHERE Portfolio_Rank IS NOT NULL
GROUP BY Backtest_Run_ID, Strategy_Name, Lookback_Period_Days, Selection_Date
ORDER BY Selection_Date;

-- =====================================================
-- Sample Data Validation Triggers (Optional Enhancement)
-- =====================================================

DELIMITER $$

-- Trigger to validate price data (High >= Low, Close between High and Low)
CREATE TRIGGER validate_price_data
BEFORE INSERT ON Price_Data
FOR EACH ROW
BEGIN
    IF NEW.High_Price < NEW.Low_Price THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'High price cannot be less than Low price';
    END IF;

    IF NEW.Close_Price > NEW.High_Price OR NEW.Close_Price < NEW.Low_Price THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Close price must be between High and Low prices';
    END IF;
END$$

DELIMITER ;

-- =====================================================
-- Schema Creation Complete
-- =====================================================

-- Verify table creation
SHOW TABLES;

-- Display table structures
DESCRIBE ETF_Master;
DESCRIBE Price_Data;
DESCRIBE Strategy_Log;
