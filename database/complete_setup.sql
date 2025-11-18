-- ============================================================
-- Portfolio Backtesting System - Complete Setup Script
-- ============================================================
-- This script will:
-- 1. Create database
-- 2. Create all tables
-- 3. Insert benchmark portfolios
-- 4. You need to import ETF data separately using Python script
-- ============================================================

-- Create database
DROP DATABASE IF EXISTS portfolio_backtesting;
CREATE DATABASE portfolio_backtesting
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE portfolio_backtesting;

-- ============================================================
-- Table 1: etf_master
-- ============================================================
CREATE TABLE etf_master (
    etf_id INT AUTO_INCREMENT PRIMARY KEY,
    ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
    etf_name VARCHAR(255) NOT NULL,
    asset_class VARCHAR(50) NOT NULL,
    region VARCHAR(50),
    sector VARCHAR(100),
    expense_ratio DECIMAL(5,4),
    inception_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticker (ticker_symbol),
    INDEX idx_asset_class (asset_class),
    INDEX idx_sector (sector)
) ENGINE=InnoDB;

-- ============================================================
-- Table 2: price_history
-- ============================================================
CREATE TABLE price_history (
    price_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    etf_id INT NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(12,4) NOT NULL,
    high DECIMAL(12,4) NOT NULL,
    low DECIMAL(12,4) NOT NULL,
    close DECIMAL(12,4) NOT NULL,
    adj_close DECIMAL(12,4) NOT NULL,
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (etf_id) REFERENCES etf_master(etf_id) ON DELETE CASCADE,
    UNIQUE KEY unique_etf_date (etf_id, date),
    INDEX idx_date (date),
    INDEX idx_etf_date (etf_id, date)
) ENGINE=InnoDB;

-- ============================================================
-- Table 3: benchmark_portfolios
-- ============================================================
CREATE TABLE benchmark_portfolios (
    benchmark_id INT AUTO_INCREMENT PRIMARY KEY,
    benchmark_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    risk_level ENUM('Conservative', 'Moderate', 'Aggressive') NOT NULL,
    target_return DECIMAL(5,2),
    asset_allocation VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB;

-- ============================================================
-- Table 4: benchmark_holdings
-- ============================================================
CREATE TABLE benchmark_holdings (
    holding_id INT AUTO_INCREMENT PRIMARY KEY,
    benchmark_id INT NOT NULL,
    etf_id INT NOT NULL,
    target_weight DECIMAL(5,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (benchmark_id) REFERENCES benchmark_portfolios(benchmark_id) ON DELETE CASCADE,
    FOREIGN KEY (etf_id) REFERENCES etf_master(etf_id) ON DELETE CASCADE,
    UNIQUE KEY unique_benchmark_etf (benchmark_id, etf_id),
    INDEX idx_benchmark (benchmark_id)
) ENGINE=InnoDB;

-- ============================================================
-- Table 5: backtest_scenarios
-- ============================================================
CREATE TABLE backtest_scenarios (
    scenario_id INT AUTO_INCREMENT PRIMARY KEY,
    benchmark_id INT,
    created_by VARCHAR(100) NOT NULL,
    scenario_name VARCHAR(200) NOT NULL,
    initial_capital DECIMAL(15,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    strategy_type ENUM('BUY_HOLD', 'REBALANCE', 'DCA') NOT NULL,
    rebalance_freq ENUM('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL'),
    monthly_contribution DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (benchmark_id) REFERENCES benchmark_portfolios(benchmark_id) ON DELETE SET NULL,
    INDEX idx_created_by (created_by),
    INDEX idx_strategy (strategy_type),
    INDEX idx_dates (start_date, end_date)
) ENGINE=InnoDB;

-- ============================================================
-- Table 6: scenario_holdings
-- ============================================================
CREATE TABLE scenario_holdings (
    holding_id INT AUTO_INCREMENT PRIMARY KEY,
    scenario_id INT NOT NULL,
    etf_id INT NOT NULL,
    target_weight DECIMAL(5,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES backtest_scenarios(scenario_id) ON DELETE CASCADE,
    FOREIGN KEY (etf_id) REFERENCES etf_master(etf_id) ON DELETE CASCADE,
    UNIQUE KEY unique_scenario_etf (scenario_id, etf_id),
    INDEX idx_scenario (scenario_id)
) ENGINE=InnoDB;

-- ============================================================
-- Table 7: backtest_results
-- ============================================================
CREATE TABLE backtest_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    scenario_id INT NOT NULL,
    total_return DECIMAL(10,2),
    annualized_return DECIMAL(8,4),
    volatility DECIMAL(8,4),
    max_drawdown DECIMAL(8,4),
    sharpe_ratio DECIMAL(8,4),
    final_value DECIMAL(15,2),
    vs_benchmark_alpha DECIMAL(8,4),
    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES backtest_scenarios(scenario_id) ON DELETE CASCADE,
    UNIQUE KEY unique_scenario_result (scenario_id),
    INDEX idx_execution_date (execution_date)
) ENGINE=InnoDB;

-- ============================================================
-- Table 8: portfolio_snapshots
-- ============================================================
CREATE TABLE portfolio_snapshots (
    snapshot_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    scenario_id INT NOT NULL,
    etf_id INT NOT NULL,
    snapshot_date DATE NOT NULL,
    shares_held DECIMAL(15,6),
    market_value DECIMAL(15,2),
    portfolio_weight DECIMAL(5,4),
    unrealized_gain DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES backtest_scenarios(scenario_id) ON DELETE CASCADE,
    FOREIGN KEY (etf_id) REFERENCES etf_master(etf_id) ON DELETE CASCADE,
    INDEX idx_scenario_date (scenario_id, snapshot_date),
    INDEX idx_snapshot_date (snapshot_date)
) ENGINE=InnoDB;

-- ============================================================
-- Table 9: transaction_log
-- ============================================================
CREATE TABLE transaction_log (
    transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    scenario_id INT NOT NULL,
    etf_id INT NOT NULL,
    trans_date DATE NOT NULL,
    trans_type ENUM('BUY', 'SELL', 'REBALANCE') NOT NULL,
    shares DECIMAL(15,6) NOT NULL,
    price DECIMAL(12,4) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES backtest_scenarios(scenario_id) ON DELETE CASCADE,
    FOREIGN KEY (etf_id) REFERENCES etf_master(etf_id) ON DELETE CASCADE,
    INDEX idx_scenario (scenario_id),
    INDEX idx_trans_date (trans_date),
    INDEX idx_trans_type (trans_type)
) ENGINE=InnoDB;

-- ============================================================
-- Show table summary
-- ============================================================
SELECT 'Database and tables created successfully!' AS Status;
SHOW TABLES;
