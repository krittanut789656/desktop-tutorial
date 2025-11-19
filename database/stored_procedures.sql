-- ============================================================
-- Portfolio Backtesting System - Stored Procedures & Views
-- ตามโจทย์อาจารย์: ใช้ SQL เป็นหลักในการวิเคราะห์
-- ============================================================

USE portfolio_backtesting;

-- ============================================================
-- View 1: vw_weekly_returns - คำนวณ Weekly Returns
-- ============================================================
DROP VIEW IF EXISTS vw_weekly_returns;

CREATE VIEW vw_weekly_returns AS
SELECT
    e.ticker_symbol,
    e.etf_id,
    ph.date,
    ph.adj_close,
    LAG(ph.adj_close) OVER (PARTITION BY e.ticker_symbol ORDER BY ph.date) AS prev_close,
    CASE
        WHEN LAG(ph.adj_close) OVER (PARTITION BY e.ticker_symbol ORDER BY ph.date) IS NOT NULL
        THEN (ph.adj_close - LAG(ph.adj_close) OVER (PARTITION BY e.ticker_symbol ORDER BY ph.date))
             / LAG(ph.adj_close) OVER (PARTITION BY e.ticker_symbol ORDER BY ph.date)
        ELSE NULL
    END AS weekly_return
FROM price_history ph
JOIN etf_master e ON ph.etf_id = e.etf_id
ORDER BY e.ticker_symbol, ph.date;

-- ============================================================
-- View 2: vw_portfolio_summary - สรุปข้อมูล Portfolio
-- ============================================================
DROP VIEW IF EXISTS vw_portfolio_summary;

CREATE VIEW vw_portfolio_summary AS
SELECT
    b.benchmark_id,
    b.benchmark_name,
    b.risk_level,
    COUNT(bh.etf_id) AS num_holdings,
    SUM(bh.target_weight) AS total_weight,
    GROUP_CONCAT(CONCAT(e.ticker_symbol, ':', ROUND(bh.target_weight * 100, 1), '%')
                 ORDER BY bh.target_weight DESC SEPARATOR ', ') AS holdings_detail
FROM benchmark_portfolios b
LEFT JOIN benchmark_holdings bh ON b.benchmark_id = bh.benchmark_id
LEFT JOIN etf_master e ON bh.etf_id = e.etf_id
GROUP BY b.benchmark_id, b.benchmark_name, b.risk_level;

-- ============================================================
-- View 3: vw_etf_performance - Performance ของแต่ละ ETF
-- ============================================================
DROP VIEW IF EXISTS vw_etf_performance;

CREATE VIEW vw_etf_performance AS
WITH etf_stats AS (
    SELECT
        ticker_symbol,
        etf_id,
        COUNT(*) AS num_periods,
        AVG(weekly_return) AS avg_return,
        STDDEV(weekly_return) AS volatility,
        MIN(weekly_return) AS min_return,
        MAX(weekly_return) AS max_return
    FROM vw_weekly_returns
    WHERE weekly_return IS NOT NULL
    GROUP BY ticker_symbol, etf_id
)
SELECT
    e.ticker_symbol,
    e.etf_name,
    e.asset_class,
    s.num_periods,
    ROUND(s.avg_return * 52 * 100, 2) AS annualized_return_pct,
    ROUND(s.volatility * SQRT(52) * 100, 2) AS annualized_volatility_pct,
    ROUND((s.avg_return * 52) / (s.volatility * SQRT(52)), 2) AS sharpe_ratio_approx,
    ROUND(s.min_return * 100, 2) AS worst_week_pct,
    ROUND(s.max_return * 100, 2) AS best_week_pct
FROM etf_stats s
JOIN etf_master e ON s.etf_id = e.etf_id
ORDER BY sharpe_ratio_approx DESC;

-- ============================================================
-- Stored Procedure 1: sp_calculate_portfolio_return
-- คำนวณ Portfolio Return จาก weights
-- ============================================================
DROP PROCEDURE IF EXISTS sp_calculate_portfolio_return;

DELIMITER //
CREATE PROCEDURE sp_calculate_portfolio_return(
    IN p_benchmark_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    OUT p_total_return DECIMAL(10,4),
    OUT p_annualized_return DECIMAL(10,4)
)
BEGIN
    DECLARE v_num_periods INT;

    -- คำนวณ weighted average return
    SELECT
        COUNT(DISTINCT wr.date),
        AVG(portfolio_return),
        AVG(portfolio_return) * 52
    INTO
        v_num_periods,
        p_total_return,
        p_annualized_return
    FROM (
        SELECT
            wr.date,
            SUM(wr.weekly_return * bh.target_weight) AS portfolio_return
        FROM vw_weekly_returns wr
        JOIN benchmark_holdings bh ON wr.etf_id = bh.etf_id
        WHERE bh.benchmark_id = p_benchmark_id
          AND wr.date BETWEEN p_start_date AND p_end_date
          AND wr.weekly_return IS NOT NULL
        GROUP BY wr.date
    ) AS portfolio_returns;

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 2: sp_calculate_sharpe_ratio
-- คำนวณ Sharpe Ratio สำหรับ ETF หรือ Portfolio
-- ============================================================
DROP PROCEDURE IF EXISTS sp_calculate_sharpe_ratio;

DELIMITER //
CREATE PROCEDURE sp_calculate_sharpe_ratio(
    IN p_ticker_symbol VARCHAR(10),
    IN p_risk_free_rate DECIMAL(5,4),
    OUT p_sharpe_ratio DECIMAL(8,4)
)
BEGIN
    DECLARE v_avg_return DECIMAL(10,6);
    DECLARE v_stddev DECIMAL(10,6);
    DECLARE v_excess_return DECIMAL(10,6);

    -- คำนวณ average return และ standard deviation
    SELECT
        AVG(weekly_return),
        STDDEV(weekly_return)
    INTO
        v_avg_return,
        v_stddev
    FROM vw_weekly_returns
    WHERE ticker_symbol = p_ticker_symbol
      AND weekly_return IS NOT NULL;

    -- คำนวณ Sharpe Ratio
    -- Sharpe = (Avg Return - Risk Free Rate) / Volatility * sqrt(52)
    SET v_excess_return = v_avg_return - (p_risk_free_rate / 52);

    IF v_stddev > 0 THEN
        SET p_sharpe_ratio = (v_excess_return / v_stddev) * SQRT(52);
    ELSE
        SET p_sharpe_ratio = 0;
    END IF;

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 3: sp_calculate_max_drawdown
-- คำนวณ Maximum Drawdown
-- ============================================================
DROP PROCEDURE IF EXISTS sp_calculate_max_drawdown;

DELIMITER //
CREATE PROCEDURE sp_calculate_max_drawdown(
    IN p_ticker_symbol VARCHAR(10),
    OUT p_max_drawdown DECIMAL(8,4)
)
BEGIN
    -- ใช้ CTE คำนวณ cumulative returns และหา max drawdown
    WITH cumulative_returns AS (
        SELECT
            date,
            weekly_return,
            EXP(SUM(LN(1 + IFNULL(weekly_return, 0))) OVER (ORDER BY date)) AS cumulative_value
        FROM vw_weekly_returns
        WHERE ticker_symbol = p_ticker_symbol
        ORDER BY date
    ),
    drawdowns AS (
        SELECT
            date,
            cumulative_value,
            MAX(cumulative_value) OVER (ORDER BY date) AS running_max,
            (cumulative_value - MAX(cumulative_value) OVER (ORDER BY date))
                / MAX(cumulative_value) OVER (ORDER BY date) AS drawdown
        FROM cumulative_returns
    )
    SELECT MIN(drawdown)
    INTO p_max_drawdown
    FROM drawdowns;

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 4: sp_calculate_volatility
-- คำนวณ Annualized Volatility
-- ============================================================
DROP PROCEDURE IF EXISTS sp_calculate_volatility;

DELIMITER //
CREATE PROCEDURE sp_calculate_volatility(
    IN p_ticker_symbol VARCHAR(10),
    OUT p_annual_volatility DECIMAL(8,4)
)
BEGIN
    DECLARE v_weekly_stddev DECIMAL(10,6);

    SELECT STDDEV(weekly_return)
    INTO v_weekly_stddev
    FROM vw_weekly_returns
    WHERE ticker_symbol = p_ticker_symbol
      AND weekly_return IS NOT NULL;

    -- Annualized Volatility = Weekly Stddev * sqrt(52)
    SET p_annual_volatility = v_weekly_stddev * SQRT(52);

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 5: sp_get_etf_correlation
-- คำนวณ Correlation ระหว่าง 2 ETFs
-- ============================================================
DROP PROCEDURE IF EXISTS sp_get_etf_correlation;

DELIMITER //
CREATE PROCEDURE sp_get_etf_correlation(
    IN p_ticker1 VARCHAR(10),
    IN p_ticker2 VARCHAR(10),
    OUT p_correlation DECIMAL(8,4)
)
BEGIN
    -- คำนวณ correlation ระหว่าง 2 ETFs
    WITH paired_returns AS (
        SELECT
            w1.date,
            w1.weekly_return AS return1,
            w2.weekly_return AS return2
        FROM vw_weekly_returns w1
        JOIN vw_weekly_returns w2 ON w1.date = w2.date
        WHERE w1.ticker_symbol = p_ticker1
          AND w2.ticker_symbol = p_ticker2
          AND w1.weekly_return IS NOT NULL
          AND w2.weekly_return IS NOT NULL
    )
    SELECT
        (COUNT(*) * SUM(return1 * return2) - SUM(return1) * SUM(return2)) /
        SQRT(
            (COUNT(*) * SUM(return1 * return1) - SUM(return1) * SUM(return1)) *
            (COUNT(*) * SUM(return2 * return2) - SUM(return2) * SUM(return2))
        )
    INTO p_correlation
    FROM paired_returns;

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 6: sp_get_top_performers
-- หา Top N ETFs ที่มี Performance ดีที่สุด
-- ============================================================
DROP PROCEDURE IF EXISTS sp_get_top_performers;

DELIMITER //
CREATE PROCEDURE sp_get_top_performers(
    IN p_metric VARCHAR(20),  -- 'return', 'sharpe', 'volatility'
    IN p_top_n INT,
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    IF p_metric = 'return' THEN
        SELECT
            ticker_symbol,
            etf_name,
            annualized_return_pct,
            annualized_volatility_pct,
            sharpe_ratio_approx
        FROM vw_etf_performance
        ORDER BY annualized_return_pct DESC
        LIMIT p_top_n;

    ELSEIF p_metric = 'sharpe' THEN
        SELECT
            ticker_symbol,
            etf_name,
            annualized_return_pct,
            annualized_volatility_pct,
            sharpe_ratio_approx
        FROM vw_etf_performance
        ORDER BY sharpe_ratio_approx DESC
        LIMIT p_top_n;

    ELSEIF p_metric = 'volatility' THEN
        SELECT
            ticker_symbol,
            etf_name,
            annualized_return_pct,
            annualized_volatility_pct,
            sharpe_ratio_approx
        FROM vw_etf_performance
        ORDER BY annualized_volatility_pct ASC
        LIMIT p_top_n;
    END IF;

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 7: sp_compare_portfolios
-- เปรียบเทียบ Performance ของ Portfolios
-- ============================================================
DROP PROCEDURE IF EXISTS sp_compare_portfolios;

DELIMITER //
CREATE PROCEDURE sp_compare_portfolios(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT
        b.benchmark_name,
        b.risk_level,
        COUNT(DISTINCT wr.date) AS num_periods,
        ROUND(AVG(portfolio_return) * 52 * 100, 2) AS annual_return_pct,
        ROUND(STDDEV(portfolio_return) * SQRT(52) * 100, 2) AS annual_volatility_pct,
        ROUND(
            (AVG(portfolio_return) * 52) / (STDDEV(portfolio_return) * SQRT(52)),
            2
        ) AS sharpe_ratio
    FROM benchmark_portfolios b
    JOIN benchmark_holdings bh ON b.benchmark_id = bh.benchmark_id
    JOIN vw_weekly_returns wr ON bh.etf_id = wr.etf_id
    WHERE wr.date BETWEEN p_start_date AND p_end_date
      AND wr.weekly_return IS NOT NULL
    GROUP BY b.benchmark_id, b.benchmark_name, b.risk_level
    ORDER BY sharpe_ratio DESC;

END //
DELIMITER ;

-- ============================================================
-- Stored Procedure 8: sp_get_portfolio_weights
-- ดูน้ำหนักของ ETFs ใน Portfolio
-- ============================================================
DROP PROCEDURE IF EXISTS sp_get_portfolio_weights;

DELIMITER //
CREATE PROCEDURE sp_get_portfolio_weights(
    IN p_benchmark_id INT
)
BEGIN
    SELECT
        e.ticker_symbol,
        e.etf_name,
        e.asset_class,
        bh.target_weight,
        ROUND(bh.target_weight * 100, 2) AS weight_pct
    FROM benchmark_holdings bh
    JOIN etf_master e ON bh.etf_id = e.etf_id
    WHERE bh.benchmark_id = p_benchmark_id
    ORDER BY bh.target_weight DESC;

END //
DELIMITER ;

-- ============================================================
-- VERIFICATION: ทดสอบว่า Stored Procedures ทำงานได้
-- ============================================================

-- Test 1: คำนวณ Sharpe Ratio ของ SPY
CALL sp_calculate_sharpe_ratio('SPY', 0.02, @sharpe);
SELECT 'Sharpe Ratio (SPY)' AS metric, ROUND(@sharpe, 2) AS value;

-- Test 2: คำนวณ Volatility ของ AGG
CALL sp_calculate_volatility('AGG', @vol);
SELECT 'Annual Volatility (AGG)' AS metric, ROUND(@vol * 100, 2) AS value_pct;

-- Test 3: ดู Top 5 ETFs ที่มี Sharpe Ratio สูงสุด
CALL sp_get_top_performers('sharpe', 5, '2009-01-01', '2025-01-01');

-- Test 4: เปรียบเทียบ Portfolios
CALL sp_compare_portfolios('2020-01-01', '2025-01-01');

-- ============================================================
-- SUMMARY
-- ============================================================
SELECT 'SQL Stored Procedures & Views Created Successfully!' AS status;
SELECT 'Total Views: 3' AS summary;
SELECT 'Total Stored Procedures: 8' AS summary;
