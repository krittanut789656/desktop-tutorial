-- ============================================================================
-- ETF Portfolio Backtesting System - Sample Queries
-- Description: Useful queries for analyzing portfolios and backtests
-- ============================================================================

USE etf_backtesting;

-- ============================================================================
-- SECTION 1: ETF Analysis Queries
-- ============================================================================

-- Query 1.1: List all ETFs by asset class with expense ratios
SELECT
    asset_class,
    ticker,
    name,
    CONCAT(expense_ratio, '%') AS expense_ratio,
    YEAR(CURDATE()) - YEAR(inception_date) AS years_active,
    inception_date
FROM etfs
ORDER BY asset_class, expense_ratio ASC;

-- Query 1.2: Find lowest expense ratio ETFs by asset class
SELECT
    asset_class,
    ticker,
    name,
    CONCAT(expense_ratio, '%') AS expense_ratio
FROM etfs e1
WHERE expense_ratio = (
    SELECT MIN(expense_ratio)
    FROM etfs e2
    WHERE e2.asset_class = e1.asset_class
)
ORDER BY asset_class;

-- Query 1.3: Compare ETFs tracking similar indexes (e.g., S&P 500)
SELECT
    ticker,
    name,
    CONCAT(expense_ratio, '%') AS expense_ratio,
    inception_date,
    DATEDIFF(CURDATE(), inception_date) AS days_since_inception
FROM etfs
WHERE asset_class = 'US Large Cap Equity'
ORDER BY expense_ratio ASC;

-- Query 1.4: ETF statistics by asset class
SELECT
    asset_class,
    COUNT(*) AS num_etfs,
    CONCAT(ROUND(AVG(expense_ratio), 4), '%') AS avg_expense_ratio,
    CONCAT(ROUND(MIN(expense_ratio), 4), '%') AS min_expense_ratio,
    CONCAT(ROUND(MAX(expense_ratio), 4), '%') AS max_expense_ratio,
    MIN(inception_date) AS oldest_etf,
    MAX(inception_date) AS newest_etf
FROM etfs
GROUP BY asset_class
ORDER BY num_etfs DESC;

-- ============================================================================
-- SECTION 2: Portfolio Analysis Queries
-- ============================================================================

-- Query 2.1: Show all portfolios with allocation details
SELECT
    p.portfolio_id,
    p.name AS portfolio_name,
    u.username,
    p.description,
    COUNT(pa.allocation_id) AS num_holdings,
    SUM(pa.weight) AS total_weight,
    p.creation_date,
    CASE WHEN p.is_active THEN 'Active' ELSE 'Inactive' END AS status
FROM portfolios p
LEFT JOIN users u ON p.user_id = u.user_id
LEFT JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
GROUP BY p.portfolio_id, p.name, u.username, p.description, p.creation_date, p.is_active
ORDER BY p.portfolio_id;

-- Query 2.2: Detailed portfolio allocation with ETF information
SELECT
    p.portfolio_id,
    p.name AS portfolio_name,
    pa.ticker,
    e.name AS etf_name,
    e.asset_class,
    CONCAT(pa.weight, '%') AS allocation,
    CONCAT(e.expense_ratio, '%') AS expense_ratio,
    CASE
        WHEN pa.weight >= 30 THEN 'Core Holding'
        WHEN pa.weight >= 10 THEN 'Moderate Holding'
        ELSE 'Small Holding'
    END AS holding_size
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
JOIN etfs e ON pa.ticker = e.ticker
ORDER BY p.portfolio_id, pa.weight DESC;

-- Query 2.3: Portfolio diversification analysis
SELECT
    p.portfolio_id,
    p.name AS portfolio_name,
    COUNT(DISTINCT e.asset_class) AS num_asset_classes,
    COUNT(pa.allocation_id) AS num_holdings,
    GROUP_CONCAT(DISTINCT e.asset_class ORDER BY e.asset_class SEPARATOR ', ') AS asset_classes,
    CONCAT(ROUND(SUM(pa.weight * e.expense_ratio) / SUM(pa.weight), 4), '%') AS weighted_avg_expense_ratio
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
JOIN etfs e ON pa.ticker = e.ticker
GROUP BY p.portfolio_id, p.name
ORDER BY p.portfolio_id;

-- Query 2.4: Asset class allocation by portfolio
SELECT
    p.name AS portfolio_name,
    e.asset_class,
    SUM(pa.weight) AS total_weight,
    COUNT(pa.ticker) AS num_etfs,
    GROUP_CONCAT(pa.ticker ORDER BY pa.weight DESC SEPARATOR ', ') AS tickers
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
JOIN etfs e ON pa.ticker = e.ticker
GROUP BY p.portfolio_id, p.name, e.asset_class
ORDER BY p.portfolio_id, total_weight DESC;

-- Query 2.5: Find portfolios using specific ETF
SELECT
    p.portfolio_id,
    p.name AS portfolio_name,
    pa.ticker,
    CONCAT(pa.weight, '%') AS allocation,
    p.description
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
WHERE pa.ticker = 'VOO'  -- Change ticker as needed
ORDER BY pa.weight DESC;

-- ============================================================================
-- SECTION 3: Backtest Analysis Queries
-- ============================================================================

-- Query 3.1: Backtest summary with performance metrics
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    b.rebalance_frequency,
    CONCAT('$', FORMAT(b.initial_capital, 2)) AS initial_capital,
    CONCAT('$', FORMAT(b.monthly_contribution, 2)) AS monthly_contribution,
    b.start_date,
    b.end_date,
    DATEDIFF(b.end_date, b.start_date) AS days,
    ROUND(DATEDIFF(b.end_date, b.start_date) / 365.25, 1) AS years,
    b.status,
    b.execution_date
FROM backtests b
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
ORDER BY b.backtest_id;

-- Query 3.2: Backtest performance comparison
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    CONCAT('$', FORMAT(b.initial_capital, 2)) AS initial_capital,
    CONCAT('$', FORMAT(MIN(br.portfolio_value), 2)) AS min_value,
    CONCAT('$', FORMAT(MAX(br.portfolio_value), 2)) AS max_value,
    CONCAT('$', FORMAT(
        (SELECT portfolio_value FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1), 2
    )) AS final_value,
    CONCAT(ROUND(
        (SELECT cumulative_return FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1) * 100, 2
    ), '%') AS total_return,
    COUNT(br.result_id) AS trading_days
FROM backtests b
LEFT JOIN backtest_results br ON b.backtest_id = br.backtest_id
WHERE b.status = 'Completed'
GROUP BY b.backtest_id, p.name, b.strategy_type, b.initial_capital
ORDER BY b.backtest_id;

-- Query 3.3: Daily returns analysis for a specific backtest
SELECT
    date,
    CONCAT('$', FORMAT(portfolio_value, 2)) AS portfolio_value,
    CONCAT(ROUND(daily_return * 100, 4), '%') AS daily_return,
    CONCAT(ROUND(cumulative_return * 100, 2), '%') AS cumulative_return,
    CONCAT('$', FORMAT(cash_balance, 2)) AS cash_balance,
    CONCAT('$', FORMAT(total_contributions, 2)) AS total_contributions
FROM backtest_results
WHERE backtest_id = 1
ORDER BY date DESC
LIMIT 30;

-- Query 3.4: Monthly performance summary
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    DATE_FORMAT(br.date, '%Y-%m') AS month,
    CONCAT('$', FORMAT(MIN(br.portfolio_value), 2)) AS month_start_value,
    CONCAT('$', FORMAT(MAX(br.portfolio_value), 2)) AS month_end_value,
    CONCAT(ROUND(
        (MAX(br.portfolio_value) - MIN(br.portfolio_value)) / MIN(br.portfolio_value) * 100, 2
    ), '%') AS monthly_return,
    COUNT(*) AS trading_days
FROM backtest_results br
JOIN backtests b ON br.backtest_id = b.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.backtest_id = 1
GROUP BY b.backtest_id, p.name, DATE_FORMAT(br.date, '%Y-%m')
ORDER BY month DESC
LIMIT 12;

-- Query 3.5: Volatility analysis (standard deviation of returns)
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    COUNT(br.result_id) AS num_days,
    CONCAT(ROUND(AVG(br.daily_return) * 100, 4), '%') AS avg_daily_return,
    CONCAT(ROUND(STDDEV(br.daily_return) * 100, 4), '%') AS daily_volatility,
    CONCAT(ROUND(MIN(br.daily_return) * 100, 4), '%') AS worst_day,
    CONCAT(ROUND(MAX(br.daily_return) * 100, 4), '%') AS best_day,
    CONCAT(ROUND(STDDEV(br.daily_return) * SQRT(252) * 100, 2), '%') AS annualized_volatility
FROM backtests b
JOIN backtest_results br ON b.backtest_id = br.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.status = 'Completed'
GROUP BY b.backtest_id, p.name, b.strategy_type
ORDER BY b.backtest_id;

-- Query 3.6: Maximum drawdown analysis
WITH portfolio_peaks AS (
    SELECT
        backtest_id,
        date,
        portfolio_value,
        MAX(portfolio_value) OVER (
            PARTITION BY backtest_id
            ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS peak_value
    FROM backtest_results
)
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    CONCAT('$', FORMAT(MAX(pp.peak_value), 2)) AS highest_value,
    CONCAT('$', FORMAT(MIN(pp.portfolio_value), 2)) AS lowest_value,
    CONCAT(ROUND(MIN((pp.portfolio_value - pp.peak_value) / pp.peak_value * 100), 2), '%') AS max_drawdown,
    (SELECT date FROM portfolio_peaks
     WHERE backtest_id = b.backtest_id
     AND (portfolio_value - peak_value) / peak_value =
         (SELECT MIN((portfolio_value - peak_value) / peak_value)
          FROM portfolio_peaks WHERE backtest_id = b.backtest_id)
     LIMIT 1) AS max_drawdown_date
FROM portfolio_peaks pp
JOIN backtests b ON pp.backtest_id = b.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.status = 'Completed'
GROUP BY b.backtest_id, p.name
ORDER BY b.backtest_id;

-- ============================================================================
-- SECTION 4: Rebalancing Analysis Queries
-- ============================================================================

-- Query 4.1: Rebalancing history
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    rh.rebalance_date,
    CONCAT('$', FORMAT(rh.transaction_cost, 2)) AS transaction_cost,
    rh.rebalance_details->>'$.action' AS action,
    rh.rebalance_details->>'$.reason' AS reason
FROM rebalance_history rh
JOIN backtests b ON rh.backtest_id = b.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
ORDER BY rh.rebalance_date DESC;

-- Query 4.2: Total rebalancing costs by backtest
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    b.rebalance_frequency,
    COUNT(rh.rebalance_id) AS num_rebalances,
    CONCAT('$', FORMAT(SUM(rh.transaction_cost), 2)) AS total_transaction_costs,
    CONCAT('$', FORMAT(AVG(rh.transaction_cost), 2)) AS avg_cost_per_rebalance
FROM backtests b
LEFT JOIN rebalance_history rh ON b.backtest_id = rh.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
GROUP BY b.backtest_id, p.name, b.strategy_type, b.rebalance_frequency
HAVING num_rebalances > 0
ORDER BY total_transaction_costs DESC;

-- ============================================================================
-- SECTION 5: Comparative Analysis Queries
-- ============================================================================

-- Query 5.1: Compare same portfolio with different strategies
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    b.rebalance_frequency,
    CONCAT('$', FORMAT(b.initial_capital, 2)) AS initial_capital,
    CONCAT('$', FORMAT(
        (SELECT portfolio_value FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1), 2
    )) AS final_value,
    CONCAT(ROUND(
        ((SELECT portfolio_value FROM backtest_results
          WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1)
         - b.initial_capital) / b.initial_capital * 100, 2
    ), '%') AS roi
FROM backtests b
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE p.portfolio_id = 1 AND b.status = 'Completed'
ORDER BY roi DESC;

-- Query 5.2: Risk-adjusted returns (Sharpe Ratio approximation)
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    b.strategy_type,
    CONCAT(ROUND(AVG(br.daily_return) * 252 * 100, 2), '%') AS annualized_return,
    CONCAT(ROUND(STDDEV(br.daily_return) * SQRT(252) * 100, 2), '%') AS annualized_volatility,
    ROUND(
        (AVG(br.daily_return) * 252) /
        (STDDEV(br.daily_return) * SQRT(252)), 2
    ) AS sharpe_ratio_approx
FROM backtests b
JOIN backtest_results br ON b.backtest_id = br.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.status = 'Completed'
GROUP BY b.backtest_id, p.name, b.strategy_type
ORDER BY sharpe_ratio_approx DESC;

-- Query 5.3: Year-over-year performance
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    YEAR(br.date) AS year,
    CONCAT('$', FORMAT(MIN(br.portfolio_value), 2)) AS start_value,
    CONCAT('$', FORMAT(MAX(br.portfolio_value), 2)) AS end_value,
    CONCAT(ROUND(
        (MAX(br.portfolio_value) - MIN(br.portfolio_value)) / MIN(br.portfolio_value) * 100, 2
    ), '%') AS yearly_return
FROM backtests b
JOIN backtest_results br ON b.backtest_id = br.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.status = 'Completed'
GROUP BY b.backtest_id, p.name, YEAR(br.date)
ORDER BY b.backtest_id, year;

-- ============================================================================
-- SECTION 6: Advanced Analytics Queries
-- ============================================================================

-- Query 6.1: Calculate portfolio beta (assuming SPY as market benchmark)
-- Note: Requires daily price data for SPY and portfolio
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    ROUND(
        COVAR_POP(br.daily_return, spy.daily_return) /
        VAR_POP(spy.daily_return), 4
    ) AS beta_vs_spy
FROM backtests b
JOIN backtest_results br ON b.backtest_id = br.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
LEFT JOIN (
    SELECT
        date,
        (close - LAG(close) OVER (ORDER BY date)) / LAG(close) OVER (ORDER BY date) AS daily_return
    FROM daily_prices
    WHERE ticker = 'SPY'
) spy ON br.date = spy.date
WHERE b.status = 'Completed'
GROUP BY b.backtest_id, p.name;

-- Query 6.2: Top performing portfolios
SELECT
    p.portfolio_id,
    p.name AS portfolio_name,
    COUNT(b.backtest_id) AS num_backtests,
    CONCAT(ROUND(AVG(
        (SELECT cumulative_return FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1)
    ) * 100, 2), '%') AS avg_return,
    CONCAT(ROUND(MAX(
        (SELECT cumulative_return FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1)
    ) * 100, 2), '%') AS best_return
FROM portfolios p
LEFT JOIN backtests b ON p.portfolio_id = b.portfolio_id AND b.status = 'Completed'
GROUP BY p.portfolio_id, p.name
HAVING num_backtests > 0
ORDER BY avg_return DESC;

-- Query 6.3: User portfolio summary
SELECT
    u.username,
    COUNT(DISTINCT p.portfolio_id) AS num_portfolios,
    COUNT(DISTINCT b.backtest_id) AS num_backtests,
    COUNT(DISTINCT CASE WHEN b.status = 'Completed' THEN b.backtest_id END) AS completed_backtests,
    MAX(b.execution_date) AS last_backtest_date
FROM users u
LEFT JOIN portfolios p ON u.user_id = p.user_id
LEFT JOIN backtests b ON p.portfolio_id = b.portfolio_id
GROUP BY u.user_id, u.username
ORDER BY num_backtests DESC;

-- ============================================================================
-- End of Sample Queries
-- ============================================================================
