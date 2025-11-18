-- ===============================================
-- Import Price History (208,700 rows)
-- วิธีที่ 1: LOAD DATA INFILE (แนะนำ - เร็วที่สุด!)
-- ===============================================

USE portfolio_backtesting;

-- ===============================================
-- เตรียมข้อมูล
-- ===============================================

-- ลบข้อมูลเก่า (ถ้ามี)
TRUNCATE TABLE price_history;

-- ===============================================
-- LOAD DATA INFILE
-- ===============================================
-- ⚠️ สำคัญ: ต้องแก้ path ให้ตรงกับเครื่องคุณ!
--
-- สำหรับ Windows:
-- LOAD DATA LOCAL INFILE 'C:/Users/YourName/desktop-tutorial/data/etf_price_history.csv'
--
-- สำหรับ Mac/Linux:
-- LOAD DATA LOCAL INFILE '/Users/YourName/desktop-tutorial/data/etf_price_history.csv'
-- ===============================================

LOAD DATA LOCAL INFILE 'C:/Users/YourName/desktop-tutorial/data/etf_price_history.csv'
INTO TABLE price_history
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @ticker,
    @date,
    @open,
    @high,
    @low,
    @close,
    @adj_close,
    @volume
)
SET
    etf_id = (SELECT etf_id FROM etf_master WHERE ticker_symbol = @ticker),
    price_date = @date,
    open_price = @open,
    high_price = @high,
    low_price = @low,
    close_price = @close,
    volume = @volume;

-- ===============================================
-- ตรวจสอบผลลัพธ์
-- ===============================================

SELECT COUNT(*) AS row_count FROM price_history;
-- ควรได้: 208,700

-- ตัวอย่างข้อมูล
SELECT e.ticker_symbol, ph.price_date, ph.close_price, ph.volume
FROM price_history ph
JOIN etf_master e ON ph.etf_id = e.etf_id
ORDER BY ph.price_date DESC
LIMIT 10;

-- ===============================================
-- เสร็จแล้ว!
-- ===============================================
