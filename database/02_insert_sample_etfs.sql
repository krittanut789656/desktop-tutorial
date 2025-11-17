-- ============================================================================
-- ETF Portfolio Backtesting System - Sample ETF Data
-- Description: Insert 40 popular ETFs across different asset classes
-- ============================================================================

USE etf_backtesting;

-- ============================================================================
-- Insert Sample ETFs (40 popular ETFs)
-- Categories: US Equity, International Equity, Bonds, Commodities, Real Estate
-- ============================================================================

INSERT INTO etfs (ticker, name, asset_class, expense_ratio, inception_date, description) VALUES

-- ========== US Equity ETFs - Large Cap ==========
('SPY', 'SPDR S&P 500 ETF Trust', 'US Large Cap Equity', 0.0945, '1993-01-22',
 'Tracks the S&P 500 index, representing the 500 largest US companies'),

('VOO', 'Vanguard S&P 500 ETF', 'US Large Cap Equity', 0.03, '2010-09-07',
 'Low-cost S&P 500 index fund from Vanguard'),

('IVV', 'iShares Core S&P 500 ETF', 'US Large Cap Equity', 0.03, '2000-05-15',
 'Tracks the S&P 500 index with low expense ratio'),

('VTI', 'Vanguard Total Stock Market ETF', 'US Total Market Equity', 0.03, '2001-05-24',
 'Covers the entire US stock market including small, mid, and large cap'),

('QQQ', 'Invesco QQQ Trust', 'US Technology', 0.20, '1999-03-10',
 'Tracks the Nasdaq-100 index, heavy in technology stocks'),

-- ========== US Equity ETFs - Growth ==========
('VUG', 'Vanguard Growth ETF', 'US Growth Equity', 0.04, '2004-01-26',
 'Focuses on large-cap US growth stocks'),

('IWF', 'iShares Russell 1000 Growth ETF', 'US Growth Equity', 0.19, '2000-05-22',
 'Tracks large and mid-cap US growth stocks'),

('SCHG', 'Schwab U.S. Large-Cap Growth ETF', 'US Growth Equity', 0.04, '2009-12-11',
 'Low-cost large-cap growth stocks'),

-- ========== US Equity ETFs - Value ==========
('VTV', 'Vanguard Value ETF', 'US Value Equity', 0.04, '2004-01-26',
 'Large-cap US value stocks with lower P/E ratios'),

('IWD', 'iShares Russell 1000 Value ETF', 'US Value Equity', 0.19, '2000-05-22',
 'Large and mid-cap value stocks from Russell 1000'),

('SCHV', 'Schwab U.S. Large-Cap Value ETF', 'US Value Equity', 0.04, '2009-12-11',
 'Low-cost large-cap value exposure'),

-- ========== US Equity ETFs - Mid & Small Cap ==========
('VO', 'Vanguard Mid-Cap ETF', 'US Mid Cap Equity', 0.04, '2004-01-26',
 'US mid-cap stocks representing medium-sized companies'),

('IJH', 'iShares Core S&P Mid-Cap ETF', 'US Mid Cap Equity', 0.05, '2000-05-22',
 'Tracks S&P MidCap 400 index'),

('VB', 'Vanguard Small-Cap ETF', 'US Small Cap Equity', 0.05, '2004-01-26',
 'Small-cap US companies with growth potential'),

('IWM', 'iShares Russell 2000 ETF', 'US Small Cap Equity', 0.19, '2000-05-22',
 'Tracks the Russell 2000 small-cap index'),

-- ========== International Equity ETFs - Developed Markets ==========
('VEA', 'Vanguard FTSE Developed Markets ETF', 'International Developed Equity', 0.05, '2007-07-20',
 'Large and mid-cap stocks from developed markets excluding US'),

('IEFA', 'iShares Core MSCI EAFE ETF', 'International Developed Equity', 0.07, '2012-10-18',
 'Developed markets in Europe, Australasia, and Far East'),

('EFA', 'iShares MSCI EAFE ETF', 'International Developed Equity', 0.32, '2001-08-14',
 'International developed markets equity exposure'),

('VGK', 'Vanguard FTSE Europe ETF', 'European Equity', 0.08, '2005-03-04',
 'European stocks from developed markets'),

('EWJ', 'iShares MSCI Japan ETF', 'Japan Equity', 0.51, '1996-03-12',
 'Japanese equity exposure'),

-- ========== International Equity ETFs - Emerging Markets ==========
('VWO', 'Vanguard FTSE Emerging Markets ETF', 'Emerging Markets Equity', 0.08, '2005-03-04',
 'Large and mid-cap stocks from emerging markets'),

('IEMG', 'iShares Core MSCI Emerging Markets ETF', 'Emerging Markets Equity', 0.09, '2012-10-18',
 'Broad emerging markets exposure'),

('EEM', 'iShares MSCI Emerging Markets ETF', 'Emerging Markets Equity', 0.68, '2003-04-07',
 'Emerging markets equity across Asia, Latin America, and other regions'),

-- ========== Bond ETFs - US Government ==========
('BND', 'Vanguard Total Bond Market ETF', 'US Aggregate Bonds', 0.03, '2007-04-03',
 'Broad US investment-grade bond market'),

('AGG', 'iShares Core U.S. Aggregate Bond ETF', 'US Aggregate Bonds', 0.03, '2003-09-22',
 'US investment-grade bonds including government and corporate'),

('SHY', 'iShares 1-3 Year Treasury Bond ETF', 'US Short-Term Treasury', 0.15, '2002-07-22',
 'Short-term US Treasury bonds with 1-3 year maturity'),

('IEF', 'iShares 7-10 Year Treasury Bond ETF', 'US Intermediate Treasury', 0.15, '2002-07-22',
 'Intermediate-term Treasury bonds'),

('TLT', 'iShares 20+ Year Treasury Bond ETF', 'US Long-Term Treasury', 0.15, '2002-07-22',
 'Long-term Treasury bonds for duration exposure'),

-- ========== Bond ETFs - Corporate & High Yield ==========
('LQD', 'iShares iBoxx Investment Grade Corporate Bond ETF', 'US Corporate Bonds', 0.14, '2002-07-22',
 'Investment-grade corporate bonds'),

('HYG', 'iShares iBoxx High Yield Corporate Bond ETF', 'US High Yield Bonds', 0.49, '2007-04-04',
 'High-yield corporate bonds (junk bonds)'),

('TIP', 'iShares TIPS Bond ETF', 'US TIPS', 0.19, '2003-12-04',
 'Treasury Inflation-Protected Securities'),

-- ========== Sector ETFs ==========
('XLK', 'Technology Select Sector SPDR Fund', 'US Technology', 0.10, '1998-12-16',
 'Technology sector stocks from S&P 500'),

('XLF', 'Financial Select Sector SPDR Fund', 'US Financials', 0.10, '1998-12-16',
 'Financial sector stocks from S&P 500'),

('XLV', 'Health Care Select Sector SPDR Fund', 'US Healthcare', 0.10, '1998-12-16',
 'Healthcare sector stocks from S&P 500'),

('XLE', 'Energy Select Sector SPDR Fund', 'US Energy', 0.10, '1998-12-16',
 'Energy sector stocks from S&P 500'),

-- ========== Real Estate & Commodities ==========
('VNQ', 'Vanguard Real Estate ETF', 'US Real Estate', 0.12, '2004-09-23',
 'US real estate investment trusts (REITs)'),

('GLD', 'SPDR Gold Shares', 'Gold', 0.40, '2004-11-18',
 'Physical gold bullion'),

('SLV', 'iShares Silver Trust', 'Silver', 0.50, '2006-04-28',
 'Physical silver bullion'),

('DBC', 'Invesco DB Commodity Index Tracking Fund', 'Commodities', 0.87, '2006-02-03',
 'Broad commodity exposure'),

('USO', 'United States Oil Fund', 'Oil', 0.79, '2006-04-10',
 'Crude oil futures exposure');

-- ============================================================================
-- Verify Inserted Data
-- ============================================================================

-- Show count by asset class
SELECT
    asset_class,
    COUNT(*) AS num_etfs,
    AVG(expense_ratio) AS avg_expense_ratio,
    MIN(inception_date) AS oldest_etf,
    MAX(inception_date) AS newest_etf
FROM etfs
GROUP BY asset_class
ORDER BY num_etfs DESC;

-- Show all inserted ETFs
SELECT
    ticker,
    name,
    asset_class,
    CONCAT(expense_ratio, '%') AS expense_ratio,
    inception_date,
    YEAR(CURDATE()) - YEAR(inception_date) AS years_active
FROM etfs
ORDER BY asset_class, ticker;

-- Count total ETFs
SELECT COUNT(*) AS total_etfs FROM etfs;

-- ============================================================================
-- End of Script
-- ============================================================================
