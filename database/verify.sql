-- =====================================================
-- Verification Script - ETF Backtester Database
-- Run this to verify database setup is correct
-- =====================================================

-- Use the database
USE etf_backtester_db;

-- =====================================================
-- Test 1: Check Tables Exist
-- =====================================================
SELECT 'Test 1: Checking Tables...' as Test;

SELECT
    table_name as 'Tables in etf_backtester_db'
FROM information_schema.tables
WHERE table_schema = 'etf_backtester_db'
    AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Expected: ETF_Master, Price_Data, Strategy_Log

-- =====================================================
-- Test 2: Check Views Exist
-- =====================================================
SELECT 'Test 2: Checking Views...' as Test;

SELECT
    table_name as 'Views in etf_backtester_db'
FROM information_schema.tables
WHERE table_schema = 'etf_backtester_db'
    AND table_type = 'VIEW'
ORDER BY table_name;

-- Expected: vw_latest_prices, vw_portfolio_summary

-- =====================================================
-- Test 3: Check ETF_Master Structure
-- =====================================================
SELECT 'Test 3: Checking ETF_Master Structure...' as Test;

DESCRIBE ETF_Master;

-- Expected Columns:
-- ETF_ID, Ticker_Symbol, ETF_Name, Asset_Type,
-- Expense_Ratio, Inception_Date, Created_At, Updated_At

-- =====================================================
-- Test 4: Check ETF Record Count
-- =====================================================
SELECT 'Test 4: Checking ETF Record Count...' as Test;

SELECT COUNT(*) as Total_ETFs FROM ETF_Master;

-- Expected: 50

-- =====================================================
-- Test 5: Check ETF Distribution by Asset Type
-- =====================================================
SELECT 'Test 5: Checking ETF Distribution...' as Test;

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

-- =====================================================
-- Test 6: Sample ETF Data
-- =====================================================
SELECT 'Test 6: Sample ETF Data (Top 10)...' as Test;

SELECT
    ETF_ID,
    Ticker_Symbol,
    ETF_Name,
    Asset_Type,
    Expense_Ratio
FROM ETF_Master
ORDER BY Ticker_Symbol
LIMIT 10;

-- =====================================================
-- Test 7: Check for Key ETFs
-- =====================================================
SELECT 'Test 7: Checking Key ETFs...' as Test;

SELECT
    Ticker_Symbol,
    ETF_Name,
    Asset_Type
FROM ETF_Master
WHERE Ticker_Symbol IN ('SPY', 'QQQ', 'AGG', 'GLD', 'AOR')
ORDER BY Ticker_Symbol;

-- Expected: 5 rows (SPY, QQQ, AGG, GLD, AOR)

-- =====================================================
-- Test 8: Check Indexes
-- =====================================================
SELECT 'Test 8: Checking Indexes on ETF_Master...' as Test;

SHOW INDEX FROM ETF_Master;

-- Expected indexes on:
-- ETF_ID (PRIMARY)
-- Ticker_Symbol (UNIQUE)
-- Asset_Type (INDEX)

-- =====================================================
-- Test 9: Check Expense Ratio Statistics
-- =====================================================
SELECT 'Test 9: Expense Ratio Statistics...' as Test;

SELECT
    Asset_Type,
    COUNT(*) as ETF_Count,
    MIN(Expense_Ratio) as Min_Expense,
    AVG(Expense_Ratio) as Avg_Expense,
    MAX(Expense_Ratio) as Max_Expense
FROM ETF_Master
GROUP BY Asset_Type
ORDER BY Asset_Type;

-- =====================================================
-- Test 10: Check Triggers
-- =====================================================
SELECT 'Test 10: Checking Triggers...' as Test;

SHOW TRIGGERS FROM etf_backtester_db;

-- Expected: validate_price_data

-- =====================================================
-- Summary Report
-- =====================================================
SELECT 'SUMMARY REPORT' as Test;

SELECT
    'Database Setup' as Component,
    CASE
        WHEN (SELECT COUNT(*) FROM information_schema.tables
              WHERE table_schema = 'etf_backtester_db'
              AND table_type = 'BASE TABLE') = 3
        THEN 'PASS ✓'
        ELSE 'FAIL ✗'
    END as Status,
    CONCAT(
        (SELECT COUNT(*) FROM information_schema.tables
         WHERE table_schema = 'etf_backtester_db'
         AND table_type = 'BASE TABLE'),
        ' tables'
    ) as Details

UNION ALL

SELECT
    'ETF Master Data' as Component,
    CASE
        WHEN (SELECT COUNT(*) FROM ETF_Master) = 50
        THEN 'PASS ✓'
        ELSE 'FAIL ✗'
    END as Status,
    CONCAT((SELECT COUNT(*) FROM ETF_Master), ' ETFs') as Details

UNION ALL

SELECT
    'Views Created' as Component,
    CASE
        WHEN (SELECT COUNT(*) FROM information_schema.tables
              WHERE table_schema = 'etf_backtester_db'
              AND table_type = 'VIEW') = 2
        THEN 'PASS ✓'
        ELSE 'FAIL ✗'
    END as Status,
    CONCAT(
        (SELECT COUNT(*) FROM information_schema.tables
         WHERE table_schema = 'etf_backtester_db'
         AND table_type = 'VIEW'),
        ' views'
    ) as Details

UNION ALL

SELECT
    'Triggers Created' as Component,
    CASE
        WHEN (SELECT COUNT(*) FROM information_schema.triggers
              WHERE trigger_schema = 'etf_backtester_db') >= 1
        THEN 'PASS ✓'
        ELSE 'FAIL ✗'
    END as Status,
    CONCAT(
        (SELECT COUNT(*) FROM information_schema.triggers
         WHERE trigger_schema = 'etf_backtester_db'),
        ' triggers'
    ) as Details;

-- =====================================================
-- End of Verification
-- =====================================================
SELECT 'Verification Complete!' as Status;
SELECT 'If all tests show PASS ✓, your database is ready!' as Message;
