-- ============================================================================
-- Price_Data - SAMPLE FILE (Shows Structure Only)
-- ============================================================================
-- This is a SAMPLE file showing the correct format for Price_Data
-- For FULL dataset with real Yahoo Finance data, see: HOW_TO_GET_PRICE_DATA.md
--
-- TO GET FULL DATASET:
-- 1. Run: python main.py (downloads 10 years of data from Yahoo Finance)
-- 2. Run: python export_to_sql.py (exports to SQL file)
-- 3. Result: sql/price_data_YYYYMMDD_HHMMSS.sql (~26,000 records)
-- ============================================================================

USE etf_backtester_db;

SET FOREIGN_KEY_CHECKS = 0;

-- Sample Price Data (10 weeks for SPY - ETF_ID = 1)
-- Full file would have ~26,000 records for all 50 ETFs

INSERT INTO Price_Data
(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)
VALUES
-- SPY (S&P 500 ETF) - Sample recent weeks
(1, '2024-11-18', 589.2100, 595.1200, 588.6500, 594.3400, 594.3400, 45678900),
(1, '2024-11-11', 583.5600, 590.2300, 582.1100, 589.4500, 589.4500, 52341200),
(1, '2024-11-04', 572.3400, 584.6700, 571.9800, 583.2200, 583.2200, 61234500),
(1, '2024-10-28', 578.9000, 580.1200, 568.4500, 573.1100, 573.1100, 58901200),
(1, '2024-10-21', 582.3400, 585.7800, 575.2300, 578.5600, 578.5600, 54567800),
(1, '2024-10-14', 575.6700, 584.9100, 574.3200, 582.8900, 582.8900, 49876500),
(1, '2024-10-07', 569.4500, 577.2300, 568.1200, 576.2300, 576.2300, 51234600),
(1, '2024-09-30', 573.8900, 575.6700, 565.9000, 570.1200, 570.1200, 56789100),
(1, '2024-09-23', 568.2300, 574.5600, 567.1100, 573.4500, 573.4500, 48901200),
(1, '2024-09-16', 562.7800, 569.8900, 561.2300, 568.9000, 568.9000, 53456700);

-- QQQ (Nasdaq-100 ETF) - Sample recent weeks
INSERT INTO Price_Data
(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)
VALUES
(2, '2024-11-18', 498.5600, 505.2300, 497.1100, 503.7800, 503.7800, 32145600),
(2, '2024-11-11', 492.3400, 499.6700, 491.2200, 498.1200, 498.1200, 38567900),
(2, '2024-11-04', 482.1100, 493.4500, 481.5600, 492.8900, 492.8900, 44321100),
(2, '2024-10-28', 487.6700, 489.2300, 478.9000, 483.2300, 483.2300, 41234500),
(2, '2024-10-21', 491.2300, 494.5600, 485.1200, 488.3400, 488.3400, 39876500),
(2, '2024-10-14', 485.3400, 493.7800, 484.2200, 491.7800, 491.7800, 36543200),
(2, '2024-10-07', 479.5600, 487.2300, 478.3300, 486.1200, 486.1200, 38901200),
(2, '2024-09-30', 483.8900, 485.6700, 475.2300, 480.4500, 480.4500, 42567800),
(2, '2024-09-23', 478.1100, 484.9900, 476.7800, 483.2200, 483.2200, 35432100),
(2, '2024-09-16', 472.3400, 479.5600, 470.8900, 478.6700, 478.6700, 39123400);

-- AGG (Bond ETF) - Sample recent weeks
INSERT INTO Price_Data
(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)
VALUES
(26, '2024-11-18', 93.4500, 93.8900, 93.2300, 93.6700, 93.6700, 5678900),
(26, '2024-11-11', 94.1200, 94.3400, 93.2200, 93.5600, 93.5600, 6234500),
(26, '2024-11-04', 94.6700, 94.8900, 93.9800, 94.2300, 94.2300, 7123400),
(26, '2024-10-28', 93.9800, 94.7800, 93.7700, 94.5600, 94.5600, 6543200),
(26, '2024-10-21', 94.2300, 94.5500, 93.8800, 94.1200, 94.1200, 5876500),
(26, '2024-10-14', 94.5600, 94.7800, 94.1100, 94.3400, 94.3400, 5432100),
(26, '2024-10-07', 94.3400, 94.6700, 94.0000, 94.4500, 94.4500, 6123400),
(26, '2024-09-30', 94.1200, 94.4500, 93.8900, 94.2300, 94.2300, 6789100),
(26, '2024-09-23', 94.4500, 94.6700, 94.0000, 94.2200, 94.2200, 5567800),
(26, '2024-09-16', 94.2300, 94.5600, 93.9900, 94.3400, 94.3400, 6012300);

-- GLD (Gold ETF) - Sample recent weeks
INSERT INTO Price_Data
(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)
VALUES
(41, '2024-11-18', 234.5600, 238.9900, 233.2200, 237.4500, 237.4500, 8901200),
(41, '2024-11-11', 231.2300, 235.6700, 230.1100, 234.8900, 234.8900, 9567800),
(41, '2024-11-04', 228.9000, 232.4500, 227.5600, 231.7800, 231.7800, 10234500),
(41, '2024-10-28', 232.1100, 233.5600, 226.8900, 229.2300, 229.2300, 9876500),
(41, '2024-10-21', 235.4500, 236.7800, 230.2200, 232.5600, 232.5600, 8543200),
(41, '2024-10-14', 233.2200, 236.8900, 232.1100, 235.6700, 235.6700, 7654300),
(41, '2024-10-07', 230.5600, 234.2300, 229.3400, 233.7800, 233.7800, 8234500),
(41, '2024-09-30', 232.8900, 233.4500, 228.9900, 230.1200, 230.1200, 9123400),
(41, '2024-09-23', 229.3400, 233.5600, 228.1100, 232.4500, 232.4500, 7890100),
(41, '2024-09-16', 226.7800, 230.2300, 225.5600, 229.8900, 229.8900, 8456700);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- IMPORTANT NOTES:
-- ============================================================================
-- 1. This sample shows only 40 records (10 weeks × 4 ETFs)
-- 2. FULL dataset has ~26,000 records (520 weeks × 50 ETFs)
-- 3. All prices in FULL dataset are REAL from Yahoo Finance
-- 4. To get FULL dataset, follow instructions in:
--    sql/HOW_TO_GET_PRICE_DATA.md
--
-- TO GET FULL REAL DATA:
--   Step 1: python main.py (downloads from Yahoo Finance)
--   Step 2: python export_to_sql.py (exports to SQL)
--   Step 3: Load sql/price_data_YYYYMMDD_HHMMSS.sql
--
-- OR get the full SQL file from your team lead / instructor
-- ============================================================================

-- Verification queries
SELECT COUNT(*) as Sample_Records FROM Price_Data;
-- Expected with sample: 40 records
-- Expected with full dataset: ~26,000 records

SELECT
    MIN(Price_Date) as Earliest,
    MAX(Price_Date) as Latest,
    COUNT(DISTINCT ETF_ID) as ETFs
FROM Price_Data;
-- Sample: 4 ETFs, recent dates
-- Full dataset: 50 ETFs, 10 years of data

-- View sample data with ETF names
SELECT pd.*, em.Ticker_Symbol, em.ETF_Name
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
ORDER BY pd.Price_Date DESC, em.Ticker_Symbol
LIMIT 20;
