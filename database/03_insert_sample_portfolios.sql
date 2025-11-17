-- ============================================================================
-- ETF Portfolio Backtesting System - Sample Portfolios and Test Data
-- Description: Create sample portfolios with allocations for testing
-- ============================================================================

USE etf_backtesting;

-- ============================================================================
-- Insert Sample Portfolios
-- ============================================================================

-- Portfolio 1: Classic 60/40 (60% Stocks, 40% Bonds)
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(1, 'Classic 60/40 Portfolio', 'Traditional balanced portfolio with 60% US stocks and 40% US bonds', TRUE);

SET @portfolio_60_40 = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_60_40, 'VOO', 60.00),
(@portfolio_60_40, 'BND', 40.00);

-- Portfolio 2: Aggressive Growth (100% Equity)
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(1, 'Aggressive Growth Portfolio', '100% equity portfolio focused on growth and technology', TRUE);

SET @portfolio_growth = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_growth, 'QQQ', 40.00),
(@portfolio_growth, 'VUG', 30.00),
(@portfolio_growth, 'VB', 20.00),
(@portfolio_growth, 'VWO', 10.00);

-- Portfolio 3: Three-Fund Portfolio (Global Diversification)
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(1, 'Three-Fund Portfolio', 'Simple globally diversified portfolio with US stocks, international stocks, and bonds', TRUE);

SET @portfolio_three_fund = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_three_fund, 'VTI', 40.00),
(@portfolio_three_fund, 'IEFA', 30.00),
(@portfolio_three_fund, 'BND', 30.00);

-- Portfolio 4: Conservative Income (70% Bonds, 30% Stocks)
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(1, 'Conservative Income Portfolio', 'Low-risk portfolio focused on income generation', TRUE);

SET @portfolio_conservative = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_conservative, 'BND', 50.00),
(@portfolio_conservative, 'LQD', 20.00),
(@portfolio_conservative, 'VOO', 20.00),
(@portfolio_conservative, 'VNQ', 10.00);

-- Portfolio 5: All-Weather Portfolio (Risk Parity Inspired)
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(1, 'All-Weather Portfolio', 'Diversified across multiple asset classes to handle various market conditions', TRUE);

SET @portfolio_all_weather = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_all_weather, 'SPY', 30.00),
(@portfolio_all_weather, 'TLT', 40.00),
(@portfolio_all_weather, 'IEF', 15.00),
(@portfolio_all_weather, 'GLD', 7.50),
(@portfolio_all_weather, 'DBC', 7.50);

-- Portfolio 6: Global Equity Portfolio
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(2, 'Global Equity Portfolio', 'Diversified global equity exposure across developed and emerging markets', TRUE);

SET @portfolio_global = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_global, 'VTI', 50.00),
(@portfolio_global, 'VEA', 30.00),
(@portfolio_global, 'VWO', 20.00);

-- Portfolio 7: Dividend Growth Portfolio
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(2, 'Dividend Growth Portfolio', 'Focus on value stocks and REITs for dividend income', TRUE);

SET @portfolio_dividend = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_dividend, 'VTV', 40.00),
(@portfolio_dividend, 'SCHV', 30.00),
(@portfolio_dividend, 'VNQ', 20.00),
(@portfolio_dividend, 'XLF', 10.00);

-- Portfolio 8: Sector Rotation Portfolio
INSERT INTO portfolios (user_id, name, description, is_active) VALUES
(2, 'Sector Rotation Portfolio', 'Tactical allocation across different sectors', TRUE);

SET @portfolio_sector = LAST_INSERT_ID();

INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@portfolio_sector, 'XLK', 30.00),
(@portfolio_sector, 'XLV', 25.00),
(@portfolio_sector, 'XLF', 20.00),
(@portfolio_sector, 'XLE', 15.00),
(@portfolio_sector, 'VNQ', 10.00);

-- ============================================================================
-- Insert Sample Backtests
-- ============================================================================

-- Backtest 1: 60/40 Portfolio - 10 Year Buy and Hold
INSERT INTO backtests (
    portfolio_id, start_date, end_date, initial_capital,
    strategy_type, rebalance_frequency, monthly_contribution, status
) VALUES (
    @portfolio_60_40, '2014-01-01', '2023-12-31', 100000.00,
    'Buy-and-Hold', 'None', 0.00, 'Completed'
);

SET @backtest_1 = LAST_INSERT_ID();

-- Backtest 2: 60/40 Portfolio - 10 Year with Annual Rebalancing
INSERT INTO backtests (
    portfolio_id, start_date, end_date, initial_capital,
    strategy_type, rebalance_frequency, monthly_contribution, status
) VALUES (
    @portfolio_60_40, '2014-01-01', '2023-12-31', 100000.00,
    'Rebalanced', 'Annually', 0.00, 'Completed'
);

SET @backtest_2 = LAST_INSERT_ID();

-- Backtest 3: Aggressive Growth - 5 Year with DCA
INSERT INTO backtests (
    portfolio_id, start_date, end_date, initial_capital,
    strategy_type, rebalance_frequency, monthly_contribution, status
) VALUES (
    @portfolio_growth, '2019-01-01', '2023-12-31', 50000.00,
    'Dollar-Cost-Averaging', 'None', 1000.00, 'Completed'
);

SET @backtest_3 = LAST_INSERT_ID();

-- Backtest 4: Three-Fund Portfolio - 10 Year with Quarterly Rebalancing
INSERT INTO backtests (
    portfolio_id, start_date, end_date, initial_capital,
    strategy_type, rebalance_frequency, monthly_contribution, status
) VALUES (
    @portfolio_three_fund, '2014-01-01', '2023-12-31', 100000.00,
    'Rebalanced', 'Quarterly', 500.00, 'Completed'
);

SET @backtest_4 = LAST_INSERT_ID();

-- Backtest 5: All-Weather Portfolio - 10 Year with Monthly Rebalancing
INSERT INTO backtests (
    portfolio_id, start_date, end_date, initial_capital,
    strategy_type, rebalance_frequency, monthly_contribution, status
) VALUES (
    @portfolio_all_weather, '2014-01-01', '2023-12-31', 100000.00,
    'Rebalanced', 'Monthly', 0.00, 'Pending'
);

-- ============================================================================
-- Insert Sample Backtest Results (for demonstration)
-- Note: In real scenario, these would be generated by the backtesting engine
-- ============================================================================

-- Sample results for Backtest 1 (just a few days for demonstration)
INSERT INTO backtest_results (
    backtest_id, date, portfolio_value, daily_return,
    cumulative_return, cash_balance, total_contributions
) VALUES
(@backtest_1, '2014-01-02', 100000.00, 0.000000, 0.000000, 0.00, 100000.00),
(@backtest_1, '2014-01-03', 100250.00, 0.002500, 0.002500, 0.00, 100000.00),
(@backtest_1, '2014-01-06', 100100.00, -0.001496, 0.001000, 0.00, 100000.00),
(@backtest_1, '2014-01-07', 100500.00, 0.003994, 0.005000, 0.00, 100000.00),
(@backtest_1, '2014-01-08', 100750.00, 0.002488, 0.007500, 0.00, 100000.00);

-- Sample results for Backtest 3 (with monthly contributions)
INSERT INTO backtest_results (
    backtest_id, date, portfolio_value, daily_return,
    cumulative_return, cash_balance, total_contributions
) VALUES
(@backtest_3, '2019-01-02', 50000.00, 0.000000, 0.000000, 0.00, 50000.00),
(@backtest_3, '2019-01-31', 51250.00, 0.008000, 0.025000, 1000.00, 51000.00),
(@backtest_3, '2019-02-28', 52600.00, 0.006000, 0.052000, 1000.00, 52000.00),
(@backtest_3, '2019-03-29', 54100.00, 0.005000, 0.082000, 1000.00, 53000.00);

-- ============================================================================
-- Insert Sample Rebalance History
-- ============================================================================

INSERT INTO rebalance_history (backtest_id, rebalance_date, rebalance_details, transaction_cost) VALUES
(@backtest_2, '2015-01-02', JSON_OBJECT(
    'action', 'annual_rebalance',
    'trades', JSON_ARRAY(
        JSON_OBJECT('ticker', 'VOO', 'shares', -50, 'price', 205.50),
        JSON_OBJECT('ticker', 'BND', 'shares', 150, 'price', 82.30)
    ),
    'reason', 'Stocks outperformed, rebalancing to 60/40'
), 12.50),

(@backtest_2, '2016-01-04', JSON_OBJECT(
    'action', 'annual_rebalance',
    'trades', JSON_ARRAY(
        JSON_OBJECT('ticker', 'VOO', 'shares', 75, 'price', 201.02),
        JSON_OBJECT('ticker', 'BND', 'shares', -200, 'price', 83.15)
    ),
    'reason', 'Bonds outperformed, rebalancing to 60/40'
), 10.75),

(@backtest_4, '2014-04-01', JSON_OBJECT(
    'action', 'quarterly_rebalance',
    'trades', JSON_ARRAY(
        JSON_OBJECT('ticker', 'VTI', 'shares', -30, 'price', 98.50),
        JSON_OBJECT('ticker', 'IEFA', 'shares', 20, 'price', 52.30),
        JSON_OBJECT('ticker', 'BND', 'shares', 15, 'price', 81.20)
    ),
    'reason', 'Quarterly rebalance to target allocation'
), 8.25);

-- ============================================================================
-- Validation Queries
-- ============================================================================

-- Validate all portfolio weights sum to 100%
SELECT
    p.portfolio_id,
    p.name,
    SUM(pa.weight) AS total_weight,
    CASE
        WHEN SUM(pa.weight) = 100.00 THEN 'Valid'
        ELSE 'Invalid - Should be 100%'
    END AS status
FROM portfolios p
LEFT JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
GROUP BY p.portfolio_id, p.name
ORDER BY p.portfolio_id;

-- Show all portfolios with their allocations
SELECT
    p.name AS portfolio_name,
    e.ticker,
    e.name AS etf_name,
    pa.weight AS weight_pct,
    e.asset_class
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
JOIN etfs e ON pa.ticker = e.ticker
ORDER BY p.portfolio_id, pa.weight DESC;

-- Show backtest summary
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    b.rebalance_frequency,
    b.start_date,
    b.end_date,
    DATEDIFF(b.end_date, b.start_date) AS days,
    CONCAT('$', FORMAT(b.initial_capital, 2)) AS initial_capital,
    CONCAT('$', FORMAT(b.monthly_contribution, 2)) AS monthly_contribution,
    b.status
FROM backtests b
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
ORDER BY b.backtest_id;

-- Show sample backtest results
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    br.date,
    CONCAT('$', FORMAT(br.portfolio_value, 2)) AS portfolio_value,
    CONCAT(ROUND(br.daily_return * 100, 2), '%') AS daily_return,
    CONCAT(ROUND(br.cumulative_return * 100, 2), '%') AS cumulative_return
FROM backtest_results br
JOIN backtests b ON br.backtest_id = b.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
ORDER BY b.backtest_id, br.date
LIMIT 20;

-- ============================================================================
-- End of Script
-- ============================================================================
