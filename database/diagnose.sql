-- =====================================================
-- Diagnostic Script for ETF Backtester Database
-- Run this to troubleshoot schema issues
-- =====================================================

-- Check if database exists
SHOW DATABASES LIKE 'etf_backtester_db';

-- Use the database (if this fails, the database doesn't exist)
USE etf_backtester_db;

-- Show all tables
SHOW TABLES;

-- Check if ETF_Master table exists and show its structure
SHOW CREATE TABLE ETF_Master;

-- Show columns in ETF_Master
DESCRIBE ETF_Master;

-- Show columns with more details
SHOW COLUMNS FROM ETF_Master;

-- Count records in ETF_Master (if any)
SELECT COUNT(*) as Record_Count FROM ETF_Master;

-- Show sample data (if any)
SELECT * FROM ETF_Master LIMIT 5;

-- Check all table structures
DESCRIBE Price_Data;
DESCRIBE Strategy_Log;

-- =====================================================
-- If you see errors above, run this fix:
-- =====================================================
-- SOURCE database/schema/01_create_schema.sql;
-- SOURCE database/data/02_load_etf_master.sql;
