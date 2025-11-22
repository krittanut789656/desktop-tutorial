-- ETF Master Data - Real ETFs from Yahoo Finance
-- DADS 4002 Course Project
-- 50 Real, Tradeable ETFs across 4 Asset Types

-- Use the database
USE etf_backtester_db;

-- Clear existing data (optional - remove if you want to keep existing data)
-- DELETE FROM Strategy_Log;
-- DELETE FROM Price_Data;
-- DELETE FROM ETF_Master;

-- Reset auto-increment (optional)
-- ALTER TABLE ETF_Master AUTO_INCREMENT = 1;

-- Insert 50 Real ETFs
-- ====================

-- EQUITY ETFs (25)
-- ================
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
-- ==============
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
-- ==================
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date) VALUES
('GLD', 'SPDR Gold Shares', 'Commodity', 0.40, '2010-01-01'),
('SLV', 'iShares Silver Trust', 'Commodity', 0.50, '2010-01-01'),
('USO', 'United States Oil Fund', 'Commodity', 0.75, '2010-01-01'),
('DBA', 'Invesco DB Agriculture Fund', 'Commodity', 0.93, '2010-01-01'),
('DBC', 'Invesco DB Commodity Index Tracking', 'Commodity', 0.87, '2010-01-01');

-- MIXED/BALANCED ETFs (5)
-- =======================
INSERT INTO ETF_Master (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date) VALUES
('AOR', 'iShares Core Growth Allocation ETF', 'Mixed', 0.15, '2010-01-01'),
('AOM', 'iShares Core Moderate Allocation ETF', 'Mixed', 0.15, '2010-01-01'),
('AOK', 'iShares Core Conservative Allocation', 'Mixed', 0.15, '2010-01-01'),
('GAL', 'SPDR SSgA Global Allocation ETF', 'Mixed', 0.30, '2010-01-01'),
('INKM', 'SPDR SSgA Income Allocation ETF', 'Mixed', 0.70, '2010-01-01');

-- Verify the data
SELECT
    Asset_Type,
    COUNT(*) as ETF_Count
FROM ETF_Master
GROUP BY Asset_Type
ORDER BY Asset_Type;

-- Show total count
SELECT COUNT(*) as Total_ETFs FROM ETF_Master;

-- ============================================================================
-- SUMMARY
-- ============================================================================
-- Total ETFs: 50
--   - Equity:    25 ETFs (Large-cap, Mid-cap, Sector, Growth, Value, Int'l)
--   - Bond:      15 ETFs (Government, Corporate, High-Yield, Municipal, Int'l)
--   - Commodity:  5 ETFs (Gold, Silver, Oil, Agriculture, Commodities)
--   - Mixed:      5 ETFs (Balanced allocation funds)
--
-- Data Source: Yahoo Finance
-- All ETFs are real, actively traded securities
-- Expense ratios are approximate annual percentages
-- ============================================================================
