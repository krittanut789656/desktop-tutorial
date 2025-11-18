-- ===============================================
-- SQL Script สำหรับ Import ข้อมูลทั้งหมด
-- Portfolio Backtesting System
-- ===============================================
-- วิธีใช้:
-- 1. เปิดไฟล์นี้ด้วย Text Editor (Notepad, VS Code)
-- 2. Copy ทั้งหมด (Ctrl+A, Ctrl+C)
-- 3. Paste ใน MySQL Workbench
-- 4. กด Execute (Ctrl+Shift+Enter)
-- 5. รอ 2-3 นาที
-- 6. เสร็จ!
-- ===============================================

USE portfolio_backtesting;

-- ลบข้อมูลเก่า (ถ้ามี)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE price_history;
TRUNCATE TABLE benchmark_holdings;
TRUNCATE TABLE benchmark_portfolios;
TRUNCATE TABLE etf_master;
SET FOREIGN_KEY_CHECKS = 1;

-- ===============================================
-- 1. Import ETF Master (50 rows)
-- ===============================================
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('AGG', 'iShares Core U.S. Aggregate Bond ETF', 'Bond', 'US', 'Aggregate Bond', 0.03, '2003-09-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('BND', 'Vanguard Total Bond Market ETF', 'Bond', 'US', 'Aggregate Bond', 0.03, '2007-04-03');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('BNDX', 'Vanguard Total International Bond ETF', 'Bond', 'International', 'International Bond', 0.07, '2013-05-31');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('DBC', 'Invesco DB Commodity Index Tracking Fund', 'Commodity', 'Global', 'Broad Commodity', 0.85, '2006-02-03');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('DIA', 'SPDR Dow Jones Industrial Average ETF', 'Equity', 'US', 'Broad Market', 0.16, '1998-01-14');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('EEM', 'iShares MSCI Emerging Markets ETF', 'Equity', 'International', 'Emerging Markets', 0.68, '2003-04-07');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('EFA', 'iShares MSCI EAFE ETF', 'Equity', 'International', 'Developed Markets', 0.32, '2001-08-14');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('GLD', 'SPDR Gold Shares', 'Commodity', 'Global', 'Gold', 0.4, '2004-11-18');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('HYG', 'iShares iBoxx $ High Yield Corporate Bond ETF', 'Bond', 'US', 'High Yield', 0.49, '2007-04-04');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('IEF', 'iShares 7-10 Year Treasury Bond ETF', 'Bond', 'US', 'Intermediate Treasury', 0.15, '2002-07-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('IEMG', 'iShares Core MSCI Emerging Markets ETF', 'Equity', 'International', 'Emerging Markets', 0.09, '2012-10-18');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('IVV', 'iShares Core S&P 500 ETF', 'Equity', 'US', 'Broad Market', 0.03, '2000-05-15');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('IWM', 'iShares Russell 2000 ETF', 'Equity', 'US', 'Small Cap', 0.19, '2000-05-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('IXUS', 'iShares Core MSCI Total International Stock ETF', 'Equity', 'International', 'Total International', 0.07, '2012-10-18');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('IYR', 'iShares U.S. Real Estate ETF', 'REIT', 'US', 'Real Estate', 0.41, '2000-06-12');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('LQD', 'iShares iBoxx $ Investment Grade Corporate Bond ETF', 'Bond', 'US', 'Corporate Bond', 0.14, '2002-07-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('MUB', 'iShares National Muni Bond ETF', 'Bond', 'US', 'Municipal Bond', 0.05, '2007-09-07');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('QQQ', 'Invesco QQQ Trust', 'Equity', 'US', 'Technology', 0.2, '1999-03-10');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('SHY', 'iShares 1-3 Year Treasury Bond ETF', 'Bond', 'US', 'Short-Term Treasury', 0.15, '2002-07-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('SLV', 'iShares Silver Trust', 'Commodity', 'Global', 'Silver', 0.5, '2006-04-28');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('SPY', 'SPDR S&P 500 ETF Trust', 'Equity', 'US', 'Broad Market', 0.0945, '1993-01-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('TIP', 'iShares TIPS Bond ETF', 'Bond', 'US', 'Inflation-Protected', 0.19, '2003-12-04');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('TLT', 'iShares 20+ Year Treasury Bond ETF', 'Bond', 'US', 'Long-Term Treasury', 0.15, '2002-07-22');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('UNG', 'United States Natural Gas Fund', 'Commodity', 'Global', 'Natural Gas', 1.06, '2007-04-18');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('USO', 'United States Oil Fund', 'Commodity', 'Global', 'Oil', 0.79, '2006-04-10');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VAW', 'Vanguard Materials ETF', 'Equity', 'US', 'Materials', 0.1, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VDC', 'Vanguard Consumer Staples ETF', 'Equity', 'US', 'Consumer Staples', 0.1, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VDE', 'Vanguard Energy ETF', 'Equity', 'US', 'Energy', 0.1, '2004-09-23');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VEA', 'Vanguard FTSE Developed Markets ETF', 'Equity', 'International', 'Developed Markets', 0.05, '2007-07-20');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VFH', 'Vanguard Financials ETF', 'Equity', 'US', 'Financials', 0.1, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VGT', 'Vanguard Information Technology ETF', 'Equity', 'US', 'Technology', 0.1, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VHT', 'Vanguard Health Care ETF', 'Equity', 'US', 'Healthcare', 0.1, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VIS', 'Vanguard Industrials ETF', 'Equity', 'US', 'Industrials', 0.1, '2004-09-23');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VNQ', 'Vanguard Real Estate ETF', 'REIT', 'US', 'Real Estate', 0.12, '2004-09-23');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VNQI', 'Vanguard Global ex-U.S. Real Estate ETF', 'REIT', 'International', 'Real Estate', 0.12, '2010-11-01');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VOO', 'Vanguard S&P 500 ETF', 'Equity', 'US', 'Broad Market', 0.03, '2010-09-07');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VTI', 'Vanguard Total Stock Market ETF', 'Equity', 'US', 'Broad Market', 0.03, '2001-05-24');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VTV', 'Vanguard Value ETF', 'Equity', 'US', 'Value', 0.04, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VUG', 'Vanguard Growth ETF', 'Equity', 'US', 'Growth', 0.04, '2004-01-26');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('VWO', 'Vanguard FTSE Emerging Markets ETF', 'Equity', 'International', 'Emerging Markets', 0.08, '2005-03-04');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLB', 'Materials Select Sector SPDR Fund', 'Equity', 'US', 'Materials', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLE', 'Energy Select Sector SPDR Fund', 'Equity', 'US', 'Energy', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLF', 'Financial Select Sector SPDR Fund', 'Equity', 'US', 'Financials', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLI', 'Industrial Select Sector SPDR Fund', 'Equity', 'US', 'Industrials', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLK', 'Technology Select Sector SPDR Fund', 'Equity', 'US', 'Technology', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLP', 'Consumer Staples Select Sector SPDR Fund', 'Equity', 'US', 'Consumer Staples', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLRE', 'Real Estate Select Sector SPDR Fund', 'REIT', 'US', 'Real Estate', 0.1, '2015-10-07');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLU', 'Utilities Select Sector SPDR Fund', 'Equity', 'US', 'Utilities', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLV', 'Health Care Select Sector SPDR Fund', 'Equity', 'US', 'Healthcare', 0.1, '1998-12-16');
INSERT INTO etf_master (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
VALUES ('XLY', 'Consumer Discretionary Select Sector SPDR Fund', 'Equity', 'US', 'Consumer Discretionary', 0.1, '1998-12-16');

-- เสร็จ: 50 ETFs

-- ===============================================
-- 2. Import Benchmark Portfolios (35 rows)
-- ===============================================
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('100% Bond Portfolio', 'All bonds - capital preservation', 'Conservative', 4.0, '100% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('100% Stock Portfolio', 'All equity - maximum growth', 'Aggressive', 12.0, '100% SPY');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('50/50 Portfolio', 'Balanced approach', 'Moderate', 7.5, '50% SPY / 50% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('70/30 Portfolio', 'Moderate growth strategy', 'Moderate', 8.5, '70% SPY / 30% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('90/10 Portfolio', 'Aggressive growth', 'Aggressive', 11.0, '90% SPY / 10% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Aggressive 80/20', '80% Stocks 20% Bonds - Growth focused', 'Aggressive', 10.0, '80% SPY / 20% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('All Weather Portfolio', 'Ray Dalio''s diversified strategy', 'Moderate', 8.5, '30% SPY / 40% TLT / 15% IEF / 7.5% GLD / 7.5% DBC');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Balanced Growth', 'Diversified moderate portfolio', 'Moderate', 8.5, '35% SPY / 25% VEA / 20% AGG / 10% VNQ / 10% GLD');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Barbell Strategy', 'Short and long bonds', 'Conservative', 5.5, '40% SPY / 30% SHY / 30% TLT');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Bogleheads Three-Fund', 'Simple total market approach', 'Moderate', 9.0, '40% VTI / 20% VXUS / 40% BND');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Bond Ladder', 'Multiple bond maturities', 'Conservative', 4.5, '40% SHY / 30% IEF / 30% TLT');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Commodity Enhanced', 'Commodity allocation', 'Moderate', 8.0, '50% SPY / 30% AGG / 20% DBC');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Conservative 40/60', '40% Stocks 60% Bonds - Income focused', 'Conservative', 6.0, '40% SPY / 60% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Conservative Income', 'High quality bonds', 'Conservative', 5.0, '20% SPY / 60% AGG / 20% TIP');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Core Four', 'Classic four-fund', 'Moderate', 8.5, '42% VTI / 18% VXUS / 28% BND / 12% BNDX');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Core-Satellite', 'Index core with satellite positions', 'Moderate', 9.5, '60% VTI / 20% QQQ / 10% VWO / 10% GLD');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Dividend Growth Portfolio', 'Income focused equities', 'Moderate', 8.0, '50% VTV / 30% VNQ / 20% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Emerging Markets Tilt', 'EM exposure', 'Aggressive', 10.0, '40% SPY / 30% VWO / 20% EEM / 10% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Global Diversified', 'International exposure', 'Moderate', 9.0, '40% SPY / 30% VEA / 20% VWO / 10% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Golden Butterfly', 'Modified permanent portfolio', 'Moderate', 7.5, '20% SPY / 20% SCV / 20% TLT / 20% SHY / 20% GLD');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Inflation Protected', 'TIPS and commodities', 'Conservative', 6.0, '40% TIP / 30% GLD / 30% DBC');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('International Heavy', 'Global diversification', 'Moderate', 8.5, '30% SPY / 40% VEA / 20% VWO / 10% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Ivy Portfolio', 'Tactical asset allocation', 'Moderate', 9.5, '20% SPY / 20% EFA / 20% IEF / 20% DBC / 20% VNQ');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Lazy Three-Fund', 'Simplified Bogleheads', 'Moderate', 8.5, '60% VTI / 30% BND / 10% VEA');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('No-Brainer Portfolio', 'Four equal parts', 'Moderate', 8.0, '25% SPY / 25% VEA / 25% VNQ / 25% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Permanent Portfolio', 'Harry Browne''s four-quadrant approach', 'Conservative', 7.0, '25% SPY / 25% TLT / 25% GLD / 25% Cash');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('REIT Enhanced', 'Real estate allocation', 'Moderate', 9.0, '50% SPY / 30% VNQ / 20% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Risk Parity', 'Equal risk contribution', 'Moderate', 8.0, '25% SPY / 25% TLT / 25% GLD / 25% DBC');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Sector Rotation', 'Equal weight sectors', 'Aggressive', 11.0, '11% XLK / 11% XLF / 11% XLV / 11% XLE / 11% XLI / 11% XLP / 11% XLY / 11% XLU / 12% XLB');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Simple Ivy', 'Simplified tactical allocation', 'Moderate', 9.0, '33% SPY / 33% EFA / 34% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Small Cap Tilt', 'Small cap emphasis', 'Aggressive', 10.5, '40% IWM / 40% SPY / 20% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Tech Heavy Portfolio', 'Technology sector focused', 'Aggressive', 14.0, '60% QQQ / 20% XLK / 20% VGT');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Traditional 60/40', '60% Stocks 40% Bonds - Classic balanced portfolio', 'Moderate', 8.0, '60% SPY / 40% AGG');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Two-Fund Portfolio', 'Minimal complexity', 'Moderate', 8.0, '60% VTI / 40% BND');
INSERT INTO benchmark_portfolios (benchmark_name, description, risk_level, target_return, asset_allocation)
VALUES ('Value Tilt', 'Value stock emphasis', 'Moderate', 9.0, '60% VTV / 30% VEA / 10% AGG');

-- เสร็จ: 35 benchmarks

-- ===============================================
-- 3. Import Benchmark Holdings (116 rows)
-- ===============================================
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Traditional 60/40' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Traditional 60/40' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.8
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Aggressive 80/20' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Aggressive 80/20' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Conservative 40/60' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Conservative 40/60' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather Portfolio' AND e.ticker_symbol = 'TLT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.15
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather Portfolio' AND e.ticker_symbol = 'IEF';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.075
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather Portfolio' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.075
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'All Weather Portfolio' AND e.ticker_symbol = 'DBC';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Permanent Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Permanent Portfolio' AND e.ticker_symbol = 'TLT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Permanent Portfolio' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Permanent Portfolio' AND e.ticker_symbol = 'SHY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Golden Butterfly' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Golden Butterfly' AND e.ticker_symbol = 'VTV';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Golden Butterfly' AND e.ticker_symbol = 'TLT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Golden Butterfly' AND e.ticker_symbol = 'SHY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Golden Butterfly' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Bogleheads Three-Fund' AND e.ticker_symbol = 'VTI';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Bogleheads Three-Fund' AND e.ticker_symbol = 'VXUS';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Bogleheads Three-Fund' AND e.ticker_symbol = 'BND';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Ivy Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Ivy Portfolio' AND e.ticker_symbol = 'EFA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Ivy Portfolio' AND e.ticker_symbol = 'IEF';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Ivy Portfolio' AND e.ticker_symbol = 'DBC';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Ivy Portfolio' AND e.ticker_symbol = 'VNQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 1.0
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '100% Stock Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 1.0
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '100% Bond Portfolio' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.7
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '70/30 Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '70/30 Portfolio' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.5
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '50/50 Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.5
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '50/50 Portfolio' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.9
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '90/10 Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = '90/10 Portfolio' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Tech Heavy Portfolio' AND e.ticker_symbol = 'QQQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Tech Heavy Portfolio' AND e.ticker_symbol = 'XLK';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Tech Heavy Portfolio' AND e.ticker_symbol = 'VGT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.5
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Dividend Growth Portfolio' AND e.ticker_symbol = 'VTV';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Dividend Growth Portfolio' AND e.ticker_symbol = 'VNQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Dividend Growth Portfolio' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Global Diversified' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Global Diversified' AND e.ticker_symbol = 'VEA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Global Diversified' AND e.ticker_symbol = 'VWO';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Global Diversified' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Bond Ladder' AND e.ticker_symbol = 'SHY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Bond Ladder' AND e.ticker_symbol = 'IEF';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Bond Ladder' AND e.ticker_symbol = 'TLT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Inflation Protected' AND e.ticker_symbol = 'TIP';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Inflation Protected' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Inflation Protected' AND e.ticker_symbol = 'DBC';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Risk Parity' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Risk Parity' AND e.ticker_symbol = 'TLT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Risk Parity' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Risk Parity' AND e.ticker_symbol = 'DBC';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core-Satellite' AND e.ticker_symbol = 'VTI';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core-Satellite' AND e.ticker_symbol = 'QQQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core-Satellite' AND e.ticker_symbol = 'VWO';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core-Satellite' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Lazy Three-Fund' AND e.ticker_symbol = 'VTI';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Lazy Three-Fund' AND e.ticker_symbol = 'BND';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Lazy Three-Fund' AND e.ticker_symbol = 'VEA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'No-Brainer Portfolio' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'No-Brainer Portfolio' AND e.ticker_symbol = 'VEA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'No-Brainer Portfolio' AND e.ticker_symbol = 'VNQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'No-Brainer Portfolio' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.33
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Simple Ivy' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.33
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Simple Ivy' AND e.ticker_symbol = 'EFA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.34
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Simple Ivy' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Two-Fund Portfolio' AND e.ticker_symbol = 'VTI';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Two-Fund Portfolio' AND e.ticker_symbol = 'BND';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLK';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLF';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLV';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLE';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLI';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLP';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.11
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLU';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.12
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Sector Rotation' AND e.ticker_symbol = 'XLB';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Value Tilt' AND e.ticker_symbol = 'VTV';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Value Tilt' AND e.ticker_symbol = 'VEA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Value Tilt' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Small Cap Tilt' AND e.ticker_symbol = 'IWM';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Small Cap Tilt' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Small Cap Tilt' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'International Heavy' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'International Heavy' AND e.ticker_symbol = 'VEA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'International Heavy' AND e.ticker_symbol = 'VWO';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'International Heavy' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.5
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Commodity Enhanced' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Commodity Enhanced' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Commodity Enhanced' AND e.ticker_symbol = 'DBC';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.5
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'REIT Enhanced' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'REIT Enhanced' AND e.ticker_symbol = 'VNQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'REIT Enhanced' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.35
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Balanced Growth' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.25
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Balanced Growth' AND e.ticker_symbol = 'VEA';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Balanced Growth' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Balanced Growth' AND e.ticker_symbol = 'VNQ';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Balanced Growth' AND e.ticker_symbol = 'GLD';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Conservative Income' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.6
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Conservative Income' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Conservative Income' AND e.ticker_symbol = 'TIP';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Emerging Markets Tilt' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Emerging Markets Tilt' AND e.ticker_symbol = 'VWO';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.2
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Emerging Markets Tilt' AND e.ticker_symbol = 'EEM';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.1
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Emerging Markets Tilt' AND e.ticker_symbol = 'AGG';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.4
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Barbell Strategy' AND e.ticker_symbol = 'SPY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Barbell Strategy' AND e.ticker_symbol = 'SHY';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.3
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Barbell Strategy' AND e.ticker_symbol = 'TLT';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.42
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core Four' AND e.ticker_symbol = 'VTI';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.18
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core Four' AND e.ticker_symbol = 'VXUS';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.28
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core Four' AND e.ticker_symbol = 'BND';
INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
SELECT b.benchmark_id, e.etf_id, 0.12
FROM benchmark_portfolios b, etf_master e
WHERE b.benchmark_name = 'Core Four' AND e.ticker_symbol = 'BNDX';

-- เสร็จ: 116 holdings

-- ===============================================
-- 4. Price History จะไม่รวมในไฟล์นี้
-- เพราะมี 208,700 rows (ไฟล์จะใหญ่เกินไป)
-- ให้ import ด้วย Table Data Import Wizard แทน
-- หรือใช้ simple_import.py
-- ===============================================

-- ===============================================
-- ตรวจสอบผลลัพธ์
-- ===============================================
SELECT 'etf_master' AS table_name, COUNT(*) AS row_count FROM etf_master
UNION ALL
SELECT 'benchmark_portfolios', COUNT(*) FROM benchmark_portfolios
UNION ALL
SELECT 'benchmark_holdings', COUNT(*) FROM benchmark_holdings
UNION ALL
SELECT 'price_history', COUNT(*) FROM price_history;

-- ควรได้:
-- etf_master           : 50
-- benchmark_portfolios : 35
-- benchmark_holdings   : 114-116
-- price_history        : 0 (ยังไม่ได้ import)

-- ===============================================
-- เสร็จแล้ว!
-- ===============================================
