-- ============================================================================
-- ETF Portfolio Backtesting System - Database Creation Script
-- Database: MySQL 8.0+
-- Description: Creates database and all tables with constraints and indexes
-- ============================================================================

-- Drop database if exists (use with caution in production)
DROP DATABASE IF EXISTS etf_backtesting;

-- Create database with UTF-8 encoding
CREATE DATABASE etf_backtesting
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Use the database
USE etf_backtesting;

-- ============================================================================
-- Table 1: users
-- Description: Store user information who create and manage portfolios
-- ============================================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,

    -- Constraints
    PRIMARY KEY (user_id),
    UNIQUE KEY uk_username (username),
    UNIQUE KEY uk_email (email),

    -- Indexes
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User accounts for portfolio management';

-- ============================================================================
-- Table 2: etfs
-- Description: Master table for ETF information
-- ============================================================================
CREATE TABLE etfs (
    ticker VARCHAR(10) NOT NULL,
    name VARCHAR(200) NOT NULL,
    asset_class VARCHAR(50) NOT NULL,
    expense_ratio DECIMAL(5, 4) DEFAULT 0.0000,
    inception_date DATE NOT NULL,
    description TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    PRIMARY KEY (ticker),

    -- Check constraints (MySQL 8.0.16+)
    CONSTRAINT chk_expense_ratio CHECK (expense_ratio >= 0 AND expense_ratio <= 100),

    -- Indexes
    INDEX idx_asset_class (asset_class),
    INDEX idx_inception_date (inception_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='ETF master data';

-- ============================================================================
-- Table 3: daily_prices
-- Description: Store historical daily price data for each ETF
-- ============================================================================
CREATE TABLE daily_prices (
    price_id BIGINT AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(12, 4) NOT NULL,
    high DECIMAL(12, 4) NOT NULL,
    low DECIMAL(12, 4) NOT NULL,
    close DECIMAL(12, 4) NOT NULL,
    volume BIGINT NOT NULL DEFAULT 0,
    adjusted_close DECIMAL(12, 4) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    PRIMARY KEY (price_id),
    UNIQUE KEY uk_ticker_date (ticker, date),

    -- Foreign Keys
    CONSTRAINT fk_daily_prices_ticker
        FOREIGN KEY (ticker)
        REFERENCES etfs(ticker)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Check constraints
    CONSTRAINT chk_prices_positive CHECK (
        open > 0 AND high > 0 AND low > 0 AND
        close > 0 AND adjusted_close > 0
    ),
    CONSTRAINT chk_high_low CHECK (high >= low),
    CONSTRAINT chk_volume_positive CHECK (volume >= 0),

    -- Indexes
    INDEX idx_ticker (ticker),
    INDEX idx_date (date),
    INDEX idx_ticker_date (ticker, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Daily OHLCV price data for ETFs';

-- ============================================================================
-- Table 4: portfolios
-- Description: Store portfolio configurations created by users
-- ============================================================================
CREATE TABLE portfolios (
    portfolio_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    -- Constraints
    PRIMARY KEY (portfolio_id),

    -- Foreign Keys
    CONSTRAINT fk_portfolios_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_creation_date (creation_date),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User portfolio configurations';

-- ============================================================================
-- Table 5: portfolio_allocations
-- Description: Define the weight/percentage of each ETF in a portfolio
-- ============================================================================
CREATE TABLE portfolio_allocations (
    allocation_id INT AUTO_INCREMENT,
    portfolio_id INT NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    weight DECIMAL(5, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Constraints
    PRIMARY KEY (allocation_id),
    UNIQUE KEY uk_portfolio_ticker (portfolio_id, ticker),

    -- Foreign Keys
    CONSTRAINT fk_allocations_portfolio_id
        FOREIGN KEY (portfolio_id)
        REFERENCES portfolios(portfolio_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_allocations_ticker
        FOREIGN KEY (ticker)
        REFERENCES etfs(ticker)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Check constraints
    CONSTRAINT chk_weight_range CHECK (weight >= 0 AND weight <= 100),

    -- Indexes
    INDEX idx_portfolio_id (portfolio_id),
    INDEX idx_ticker (ticker)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Portfolio allocation weights';

-- ============================================================================
-- Table 6: backtests
-- Description: Store backtest configuration and metadata
-- ============================================================================
CREATE TABLE backtests (
    backtest_id INT AUTO_INCREMENT,
    portfolio_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    initial_capital DECIMAL(15, 2) NOT NULL,
    strategy_type VARCHAR(50) NOT NULL DEFAULT 'Buy-and-Hold',
    rebalance_frequency VARCHAR(20) NOT NULL DEFAULT 'None',
    monthly_contribution DECIMAL(12, 2) DEFAULT 0.00,
    execution_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending',

    -- Constraints
    PRIMARY KEY (backtest_id),

    -- Foreign Keys
    CONSTRAINT fk_backtests_portfolio_id
        FOREIGN KEY (portfolio_id)
        REFERENCES portfolios(portfolio_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Check constraints
    CONSTRAINT chk_date_range CHECK (end_date >= start_date),
    CONSTRAINT chk_initial_capital_positive CHECK (initial_capital > 0),
    CONSTRAINT chk_monthly_contribution CHECK (monthly_contribution >= 0),
    CONSTRAINT chk_status CHECK (status IN ('Pending', 'Running', 'Completed', 'Failed')),
    CONSTRAINT chk_rebalance_frequency CHECK (
        rebalance_frequency IN ('None', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annually')
    ),

    -- Indexes
    INDEX idx_portfolio_id (portfolio_id),
    INDEX idx_execution_date (execution_date),
    INDEX idx_status (status),
    INDEX idx_date_range (start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Backtest configurations and execution metadata';

-- ============================================================================
-- Table 7: backtest_results
-- Description: Store daily results from running a backtest
-- ============================================================================
CREATE TABLE backtest_results (
    result_id BIGINT AUTO_INCREMENT,
    backtest_id INT NOT NULL,
    date DATE NOT NULL,
    portfolio_value DECIMAL(15, 2) NOT NULL,
    daily_return DECIMAL(10, 6) DEFAULT 0.000000,
    cumulative_return DECIMAL(10, 6) DEFAULT 0.000000,
    cash_balance DECIMAL(15, 2) DEFAULT 0.00,
    total_contributions DECIMAL(15, 2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    PRIMARY KEY (result_id),
    UNIQUE KEY uk_backtest_date (backtest_id, date),

    -- Foreign Keys
    CONSTRAINT fk_results_backtest_id
        FOREIGN KEY (backtest_id)
        REFERENCES backtests(backtest_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Check constraints
    CONSTRAINT chk_portfolio_value_positive CHECK (portfolio_value >= 0),
    CONSTRAINT chk_cash_balance CHECK (cash_balance >= 0),

    -- Indexes
    INDEX idx_backtest_id (backtest_id),
    INDEX idx_date (date),
    INDEX idx_backtest_date (backtest_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Daily backtest results';

-- ============================================================================
-- Table 8: rebalance_history
-- Description: Track when and how portfolio was rebalanced during backtest
-- ============================================================================
CREATE TABLE rebalance_history (
    rebalance_id INT AUTO_INCREMENT,
    backtest_id INT NOT NULL,
    rebalance_date DATE NOT NULL,
    rebalance_details JSON NULL,
    transaction_cost DECIMAL(12, 2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    PRIMARY KEY (rebalance_id),

    -- Foreign Keys
    CONSTRAINT fk_rebalance_backtest_id
        FOREIGN KEY (backtest_id)
        REFERENCES backtests(backtest_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Check constraints
    CONSTRAINT chk_transaction_cost CHECK (transaction_cost >= 0),

    -- Indexes
    INDEX idx_backtest_id (backtest_id),
    INDEX idx_rebalance_date (rebalance_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Portfolio rebalancing history';

-- ============================================================================
-- Create Views for Common Queries
-- ============================================================================

-- View: Portfolio Summary with Allocations
CREATE OR REPLACE VIEW vw_portfolio_summary AS
SELECT
    p.portfolio_id,
    p.user_id,
    u.username,
    p.name AS portfolio_name,
    p.description,
    p.creation_date,
    COUNT(pa.allocation_id) AS num_etfs,
    SUM(pa.weight) AS total_weight,
    p.is_active
FROM portfolios p
LEFT JOIN users u ON p.user_id = u.user_id
LEFT JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
GROUP BY p.portfolio_id, p.user_id, u.username, p.name, p.description, p.creation_date, p.is_active;

-- View: Backtest Performance Summary
CREATE OR REPLACE VIEW vw_backtest_performance AS
SELECT
    b.backtest_id,
    b.portfolio_id,
    p.name AS portfolio_name,
    b.strategy_type,
    b.rebalance_frequency,
    b.start_date,
    b.end_date,
    b.initial_capital,
    b.monthly_contribution,
    MIN(br.portfolio_value) AS min_portfolio_value,
    MAX(br.portfolio_value) AS max_portfolio_value,
    (SELECT portfolio_value FROM backtest_results
     WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1) AS final_portfolio_value,
    (SELECT cumulative_return FROM backtest_results
     WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1) AS final_return,
    COUNT(br.result_id) AS num_trading_days,
    b.status,
    b.execution_date
FROM backtests b
LEFT JOIN portfolios p ON b.portfolio_id = p.portfolio_id
LEFT JOIN backtest_results br ON b.backtest_id = br.backtest_id
GROUP BY b.backtest_id, b.portfolio_id, p.name, b.strategy_type, b.rebalance_frequency,
         b.start_date, b.end_date, b.initial_capital, b.monthly_contribution,
         b.status, b.execution_date;

-- ============================================================================
-- Create Stored Procedures
-- ============================================================================

-- Procedure: Validate Portfolio Weights
DELIMITER //

CREATE PROCEDURE sp_validate_portfolio_weights(IN p_portfolio_id INT)
BEGIN
    DECLARE total_weight DECIMAL(10,2);

    SELECT SUM(weight) INTO total_weight
    FROM portfolio_allocations
    WHERE portfolio_id = p_portfolio_id;

    IF total_weight IS NULL THEN
        SELECT 'No allocations found for this portfolio' AS message;
    ELSEIF total_weight != 100.00 THEN
        SELECT CONCAT('Warning: Total weight is ', total_weight, '%. Should be 100%') AS message;
    ELSE
        SELECT 'Portfolio weights are valid (100%)' AS message;
    END IF;
END //

DELIMITER ;

-- ============================================================================
-- Insert Default Data
-- ============================================================================

-- Insert a default admin user (password: admin123 - hashed with bcrypt)
INSERT INTO users (username, email, password_hash) VALUES
('admin', 'admin@etfbacktest.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'),
('demo_user', 'demo@etfbacktest.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');

-- ============================================================================
-- Show Database Structure
-- ============================================================================

-- Show all tables
SHOW TABLES;

-- Display table information
SELECT
    TABLE_NAME,
    ENGINE,
    TABLE_ROWS,
    AVG_ROW_LENGTH,
    DATA_LENGTH,
    INDEX_LENGTH,
    TABLE_COMMENT
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'etf_backtesting'
ORDER BY TABLE_NAME;

-- ============================================================================
-- End of Script
-- ============================================================================
