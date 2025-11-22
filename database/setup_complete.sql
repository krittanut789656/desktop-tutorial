-- =====================================================
-- ETF Backtester - Complete Setup (All-in-One)
-- DADS 4002 Course Project
--
-- This file contains EVERYTHING:
-- 1. Database creation
-- 2. Schema creation (tables, views, triggers)
-- 3. Data loading (50 ETFs)
--
-- Just run this ONE file and everything will be ready!
-- =====================================================

-- =====================================================
-- STEP 1: CREATE DATABASE
-- =====================================================

-- Drop existing database if exists
DROP DATABASE IF EXISTS etf_backtester_db;

-- Create fresh database
CREATE DATABASE etf_backtester_db;

-- Use the database
USE etf_backtester_db;

-- =====================================================
-- STEP 2: CREATE TABLES
-- =====================================================

-- Table 1: ETF_Master
CREATE TABLE ETF_Master (
    ETF_ID INT PRIMARY KEY AUTO_INCREMENT,
    Ticker_Symbol VARCHAR(10) NOT NULL UNIQUE,
    ETF_Name VARCHAR(100) NOT NULL,
    Asset_Type VARCHAR(50) NOT NULL,
    Expense_Ratio DECIMAL(5,4),
    Inception_Date DATE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_type (Asset_Type),
    INDEX idx_ticker (Ticker_Symbol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 2: Price_Data
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
    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY unique_etf_date (ETF_ID, Price_Date),
    INDEX idx_etf_date (ETF_ID, Price_Date),
    INDEX idx_date (Price_Date),
    INDEX idx_etf_id (ETF_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 3: Strategy_Log
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
    Momentum_Score DECIMAL(12,6),
    Portfolio_Rank INT,
    Portfolio_Weight DECIMAL(5,4) DEFAULT 0.2000,
    Entry_Price DECIMAL(12,4),
    Exit_Price DECIMAL(12,4),
    Holding_Return DECIMAL(12,6),
    Notes TEXT,
    FOREIGN KEY (ETF_ID) REFERENCES ETF_Master(ETF_ID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_run_id (Backtest_Run_ID),
    INDEX idx_selection_date (Selection_Date),
    INDEX idx_etf_id (ETF_ID),
    INDEX idx_lookback (Lookback_Period_Days),
    INDEX idx_asset_type (Asset_Type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- STEP 3: CREATE VIEWS
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
-- STEP 4: CREATE TRIGGERS
-- =====================================================

DELIMITER $$

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
-- STEP 5: INSERT ETF DATA (50 ETFs)
-- =====================================================

-- EQUITY ETFs (25)
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date) VALUES
('SPY', 'SPDR S&P 500 ETF Trust', 'Equity', 0.0945, '2010-01-01'),
('QQQ', 'Invesco QQQ Trust', 'Equity', 0.20, '2010-01-01'),
('IWM', 'iShares Russell 2000 ETF', 'Equity', 0.19, '2010-01-01'),
('VTI', 'Vanguard Total Stock Market ETF', 'Equity', 0.03, '2010-01-01'),
('VOO', 'Vanguard S&P 500 ETF', 'Equity', 0.03, '2010-01-01'),
('DIA', 'SPDR Dow Jones Industrial Average ETF', 'Equity', 0.16, '2010-01-01'),
('IVV', 'iShares Core S&P 500 ETF', 'Equity', 0.03, '2010-01-01'),
('VEA', 'Vanguard FTSE Developed Markets ETF', 'Equity', 0.05, '2010-01-01'),
('VWO', 'Vanguard FTSE Emerging Markets ETF', 'Equity', 0.08, '2010-01-01'),
('EFA', 'iShares MSCI EAFE ETF', 'Equity', 0.32, '2010-01-01'),
('VUG', 'Vanguard Growth ETF', 'Equity', 0.04, '2010-01-01'),
('VTV', 'Vanguard Value ETF', 'Equity', 0.04, '2010-01-01'),
('XLF', 'Financial Select Sector SPDR Fund', 'Equity', 0.10, '2010-01-01'),
('XLE', 'Energy Select Sector SPDR Fund', 'Equity', 0.10, '2010-01-01'),
('XLK', 'Technology Select Sector SPDR Fund', 'Equity', 0.10, '2010-01-01'),
('XLV', 'Health Care Select Sector SPDR Fund', 'Equity', 0.10, '2010-01-01'),
('XLI', 'Industrial Select Sector SPDR Fund', 'Equity', 0.10, '2010-01-01'),
('XLY', 'Consumer Discretionary Select SPDR', 'Equity', 0.10, '2010-01-01'),
('XLP', 'Consumer Staples Select SPDR', 'Equity', 0.10, '2010-01-01'),
('XLU', 'Utilities Select Sector SPDR Fund', 'Equity', 0.10, '2010-01-01'),
('ARKK', 'ARK Innovation ETF', 'Equity', 0.75, '2010-01-01'),
('ARKW', 'ARK Next Generation Internet ETF', 'Equity', 0.75, '2010-01-01'),
('ARKG', 'ARK Genomic Revolution ETF', 'Equity', 0.75, '2010-01-01'),
('ARKF', 'ARK Fintech Innovation ETF', 'Equity', 0.75, '2010-01-01'),
('SOXX', 'iShares Semiconductor ETF', 'Equity', 0.35, '2010-01-01');

-- BOND ETFs (15)
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date) VALUES
('AGG', 'iShares Core U.S. Aggregate Bond ETF', 'Bond', 0.03, '2010-01-01'),
('BND', 'Vanguard Total Bond Market ETF', 'Bond', 0.03, '2010-01-01'),
('TLT', 'iShares 20+ Year Treasury Bond ETF', 'Bond', 0.15, '2010-01-01'),
('IEF', 'iShares 7-10 Year Treasury Bond ETF', 'Bond', 0.15, '2010-01-01'),
('SHY', 'iShares 1-3 Year Treasury Bond ETF', 'Bond', 0.15, '2010-01-01'),
('LQD', 'iShares iBoxx Investment Grade Corp Bond', 'Bond', 0.14, '2010-01-01'),
('HYG', 'iShares iBoxx High Yield Corporate Bond', 'Bond', 0.49, '2010-01-01'),
('MUB', 'iShares National Muni Bond ETF', 'Bond', 0.05, '2010-01-01'),
('TIP', 'iShares TIPS Bond ETF', 'Bond', 0.19, '2010-01-01'),
('VCIT', 'Vanguard Intermediate-Term Corp Bond', 'Bond', 0.04, '2010-01-01'),
('VCSH', 'Vanguard Short-Term Corporate Bond', 'Bond', 0.04, '2010-01-01'),
('BNDX', 'Vanguard Total International Bond', 'Bond', 0.07, '2010-01-01'),
('EMB', 'iShares J.P. Morgan USD Emerging Bond', 'Bond', 0.39, '2010-01-01'),
('JNK', 'SPDR Bloomberg High Yield Bond ETF', 'Bond', 0.40, '2010-01-01'),
('GOVT', 'iShares U.S. Treasury Bond ETF', 'Bond', 0.05, '2010-01-01');

-- COMMODITY ETFs (5)
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date) VALUES
('GLD', 'SPDR Gold Shares', 'Commodity', 0.40, '2010-01-01'),
('SLV', 'iShares Silver Trust', 'Commodity', 0.50, '2010-01-01'),
('USO', 'United States Oil Fund', 'Commodity', 0.75, '2010-01-01'),
('DBA', 'Invesco DB Agriculture Fund', 'Commodity', 0.93, '2010-01-01'),
('DBC', 'Invesco DB Commodity Index Tracking', 'Commodity', 0.87, '2010-01-01');

-- MIXED/BALANCED ETFs (5)
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date) VALUES
('AOR', 'iShares Core Growth Allocation ETF', 'Mixed', 0.15, '2010-01-01'),
('AOM', 'iShares Core Moderate Allocation ETF', 'Mixed', 0.15, '2010-01-01'),
('AOK', 'iShares Core Conservative Allocation', 'Mixed', 0.15, '2010-01-01'),
('GAL', 'SPDR SSgA Global Allocation ETF', 'Mixed', 0.30, '2010-01-01'),
('INKM', 'SPDR SSgA Income Allocation ETF', 'Mixed', 0.70, '2010-01-01');

-- =====================================================
-- STEP 6: VERIFY SETUP
-- =====================================================

-- Show tables created
SELECT '=== TABLES CREATED ===' as Status;
SHOW TABLES;

-- Show ETF count
SELECT '=== ETF COUNT ===' as Status;
SELECT COUNT(*) as Total_ETFs FROM ETF_Master;

-- Show breakdown by asset type
SELECT '=== ETF BREAKDOWN BY ASSET TYPE ===' as Status;
SELECT
    Asset_Type,
    COUNT(*) as ETF_Count
FROM ETF_Master
GROUP BY Asset_Type
ORDER BY Asset_Type;

-- Show sample data
SELECT '=== SAMPLE ETF DATA (First 10) ===' as Status;
SELECT
    ETF_ID,
    Ticker_Symbol,
    ETF_Name,
    Asset_Type,
    Expense_Ratio
FROM ETF_Master
ORDER BY Ticker_Symbol
LIMIT 10;

-- Success message
SELECT '=== SETUP COMPLETE! ===' as Status;
SELECT 'Database: etf_backtester_db' as Info
UNION ALL
SELECT CONCAT('Total ETFs: ', COUNT(*)) FROM ETF_Master
UNION ALL
SELECT 'Status: Ready to use!' as Info;

-- =====================================================
-- SETUP COMPLETE!
-- =====================================================
-- You can now:
-- 1. Load historical price data
-- 2. Run backtesting strategies
-- 3. Query the database
-- =====================================================
