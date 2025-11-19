-- ========================================
-- Import Mini Dataset (3 ETFs, 1 Year)
-- ใช้เวลา: 5-10 วินาที
-- ========================================

-- ลบข้อมูลเก่า (ถ้ามี)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE price_history;
TRUNCATE TABLE benchmark_holdings;
TRUNCATE TABLE benchmark_portfolios;
TRUNCATE TABLE etf_master;
SET FOREIGN_KEY_CHECKS = 1;

-- ========================================
-- 1. Import ETF Master (3 ETFs)
-- ========================================

INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, expense_ratio, inception_date)
VALUES
('SPY', 'SPDR S&P 500 ETF Trust', 'US Equity', 0.0945, '1993-01-22'),
('AGG', 'iShares Core U.S. Aggregate Bond ETF', 'US Bonds', 0.03, '2003-09-22'),
('GLD', 'SPDR Gold Trust', 'Commodities', 0.4, '2004-11-18');

-- ========================================
-- 2. Import Benchmark Portfolios (2)
-- ========================================

INSERT INTO benchmark_portfolios (benchmark_name, description, rebalance_frequency)
VALUES
('Traditional 60/40', '60% Stocks / 40% Bonds', 'quarterly'),
('All Weather', 'Ray Dalio''s All Weather Portfolio', 'quarterly');

-- ========================================
-- 3. Import Benchmark Holdings (5)
-- ========================================

-- Traditional 60/40
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6000
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Traditional 60/40' AND e.ticker_symbol = 'SPY';

INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4000
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Traditional 60/40' AND e.ticker_symbol = 'AGG';

-- All Weather
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3000
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather' AND e.ticker_symbol = 'SPY';

INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4000
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather' AND e.ticker_symbol = 'AGG';

INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3000
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather' AND e.ticker_symbol = 'GLD';

-- ========================================
-- 4. ตรวจสอบผลลัพธ์
-- ========================================

SELECT 'etf_master' AS table_name, COUNT(*) AS row_count FROM etf_master
UNION ALL
SELECT 'benchmark_portfolios', COUNT(*) FROM benchmark_portfolios
UNION ALL
SELECT 'benchmark_holdings', COUNT(*) FROM benchmark_holdings
UNION ALL
SELECT 'price_history', COUNT(*) FROM price_history;

-- คาดหวัง:
-- etf_master: 3
-- benchmark_portfolios: 2
-- benchmark_holdings: 5
-- price_history: 0 (ยังไม่ได้ import)

-- ========================================
-- 💡 ขั้นตอนถัดไป:
--
-- รัน: python import_mini_price_history.py
-- หรือ: IMPORT_MINI_PRICE_HISTORY.sql
--
-- เพื่อ import price_history (756 rows)
-- ========================================
