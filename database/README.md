# ETF Portfolio Backtesting System

ระบบจัดการและทดสอบย้อนหลังสำหรับ Portfolio ของ ETF (Exchange-Traded Funds) โดยใช้ MySQL Database

## 📋 สารบัญ

- [ภาพรวมระบบ](#ภาพรวมระบบ)
- [โครงสร้าง Database](#โครงสร้าง-database)
- [การติดตั้งและใช้งาน](#การติดตั้งและใช้งาน)
- [ไฟล์ SQL Scripts](#ไฟล์-sql-scripts)
- [ตัวอย่างการใช้งาน](#ตัวอย่างการใช้งาน)
- [Use Cases](#use-cases)
- [คำอธิบายความแตกต่าง MySQL vs PostgreSQL](#คำอธิบายความแตกต่าง-mysql-vs-postgresql)

## 🎯 ภาพรวมระบบ

ระบบนี้ออกแบบมาเพื่อ:

1. **เก็บข้อมูล ETF** - ข้อมูลพื้นฐานของ ETF 40+ ตัวครอบคลุมหลายประเภท Asset Class
2. **จัดการ Portfolio** - สร้างและจัดการ Portfolio ที่มีการกระจายน้ำหนัก (Allocation) ของ ETF ต่างๆ
3. **ทดสอบย้อนหลัง (Backtesting)** - ทดสอบกลยุทธ์การลงทุนต่างๆ ย้อนหลัง
4. **วิเคราะห์ผลลัพธ์** - คำนวณและเก็บผลลัพธ์รายวันของการทดสอบ
5. **ติดตามการ Rebalance** - บันทึกประวัติการปรับสมดุล Portfolio

## 📊 โครงสร้าง Database

### ER Diagram

ดูรายละเอียดเพิ่มเติมได้ที่ไฟล์ `ER_Diagram.md`

### Tables (8 ตาราง)

| ตาราง | จำนวน Columns | Primary Key | Foreign Keys | คำอธิบาย |
|-------|---------------|-------------|--------------|----------|
| **users** | 6 | user_id | - | ข้อมูลผู้ใช้งานระบบ |
| **etfs** | 7 | ticker | - | ข้อมูลพื้นฐาน ETF |
| **daily_prices** | 9 | price_id | ticker → etfs | ราคารายวันของ ETF |
| **portfolios** | 6 | portfolio_id | user_id → users | Portfolio ของผู้ใช้ |
| **portfolio_allocations** | 6 | allocation_id | portfolio_id, ticker | การจัดสรรน้ำหนัก |
| **backtests** | 10 | backtest_id | portfolio_id → portfolios | การทดสอบย้อนหลัง |
| **backtest_results** | 9 | result_id | backtest_id → backtests | ผลลัพธ์รายวัน |
| **rebalance_history** | 5 | rebalance_id | backtest_id → backtests | ประวัติการปรับสมดุล |

### Views (2 Views)

1. **vw_portfolio_summary** - สรุปข้อมูล Portfolio พร้อมจำนวน ETF และน้ำหนักรวม
2. **vw_backtest_performance** - สรุปผลการทดสอบย้อนหลังพร้อม Performance Metrics

### Stored Procedures

1. **sp_validate_portfolio_weights** - ตรวจสอบน้ำหนักรวมของ Portfolio ว่าเท่ากับ 100% หรือไม่

## 🚀 การติดตั้งและใช้งาน

### ความต้องการของระบบ

- MySQL 8.0 หรือสูงกว่า
- MySQL Client (mysql command line, MySQL Workbench, หรือ DBeaver)
- สิทธิ์ในการสร้าง Database และ Tables

### ขั้นตอนการติดตั้ง

#### 1. เข้าสู่ MySQL

```bash
mysql -u root -p
```

#### 2. รัน SQL Scripts ตามลำดับ

```bash
# สร้าง Database และ Tables
mysql -u root -p < 01_create_database.sql

# Insert ข้อมูล ETF ตัวอย่าง (40 ETFs)
mysql -u root -p < 02_insert_sample_etfs.sql

# Insert Portfolio และ Backtest ตัวอย่าง
mysql -u root -p < 03_insert_sample_portfolios.sql

# ทดลองรัน Sample Queries (Optional)
mysql -u root -p etf_backtesting < 04_sample_queries.sql
```

#### 3. ตรวจสอบการติดตั้ง

```sql
USE etf_backtesting;

-- ดูจำนวน Tables
SHOW TABLES;

-- ดูจำนวน ETFs
SELECT COUNT(*) FROM etfs;

-- ดูจำนวน Portfolios
SELECT COUNT(*) FROM portfolios;
```

## 📁 ไฟล์ SQL Scripts

| ไฟล์ | ขนาด (โดยประมาณ) | คำอธิบาย |
|------|-------------------|----------|
| **01_create_database.sql** | ~15 KB | สร้าง Database, Tables, Views, Constraints, Indexes, Stored Procedures |
| **02_insert_sample_etfs.sql** | ~8 KB | Insert ข้อมูล ETF ยอดนิยม 40 ตัวครอบคลุม US Equity, International, Bonds, Commodities |
| **03_insert_sample_portfolios.sql** | ~10 KB | สร้าง Portfolio ตัวอย่าง 8 แบบพร้อม Allocations และ Sample Backtests |
| **04_sample_queries.sql** | ~12 KB | Query ตัวอย่าง 20+ แบบสำหรับวิเคราะห์ข้อมูล |
| **ER_Diagram.md** | ~8 KB | ER Diagram และเอกสารอธิบายโครงสร้าง Database |
| **README.md** | ~6 KB | เอกสารนี้ |

## 💡 ตัวอย่างการใช้งาน

### 1. สร้าง Portfolio ใหม่

```sql
-- สร้าง Portfolio
INSERT INTO portfolios (user_id, name, description)
VALUES (1, 'My Custom Portfolio', 'Portfolio สำหรับเกษียณอายุ');

SET @new_portfolio_id = LAST_INSERT_ID();

-- เพิ่ม Allocations
INSERT INTO portfolio_allocations (portfolio_id, ticker, weight) VALUES
(@new_portfolio_id, 'VOO', 50.00),
(@new_portfolio_id, 'BND', 30.00),
(@new_portfolio_id, 'VNQ', 20.00);

-- ตรวจสอบน้ำหนัก
CALL sp_validate_portfolio_weights(@new_portfolio_id);
```

### 2. สร้าง Backtest

```sql
-- สร้าง Backtest ใหม่
INSERT INTO backtests (
    portfolio_id, start_date, end_date, initial_capital,
    strategy_type, rebalance_frequency, monthly_contribution
) VALUES (
    @new_portfolio_id,
    '2015-01-01',
    '2023-12-31',
    100000.00,
    'Rebalanced',
    'Quarterly',
    500.00
);

SET @new_backtest_id = LAST_INSERT_ID();
```

### 3. ดูผลลัพธ์ Portfolio

```sql
-- ดู Allocation ของ Portfolio
SELECT
    p.name AS portfolio_name,
    e.ticker,
    e.name AS etf_name,
    pa.weight AS allocation_pct,
    e.asset_class
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
JOIN etfs e ON pa.ticker = e.ticker
WHERE p.portfolio_id = @new_portfolio_id
ORDER BY pa.weight DESC;
```

### 4. วิเคราะห์ Performance

```sql
-- ดู Performance Summary
SELECT * FROM vw_backtest_performance
WHERE portfolio_id = @new_portfolio_id;

-- คำนวณ Sharpe Ratio
SELECT
    b.backtest_id,
    p.name AS portfolio_name,
    ROUND(AVG(br.daily_return) * 252, 4) AS annualized_return,
    ROUND(STDDEV(br.daily_return) * SQRT(252), 4) AS annualized_volatility,
    ROUND((AVG(br.daily_return) * 252) / (STDDEV(br.daily_return) * SQRT(252)), 2) AS sharpe_ratio
FROM backtests b
JOIN backtest_results br ON b.backtest_id = br.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.backtest_id = @new_backtest_id
GROUP BY b.backtest_id, p.name;
```

## 🎓 Use Cases

### Use Case 1: เปรียบเทียบกลยุทธ์การลงทุน

เปรียบเทียบผลลัพธ์ระหว่าง Buy-and-Hold vs Rebalancing ด้วย Portfolio เดียวกัน

```sql
SELECT
    b.strategy_type,
    b.rebalance_frequency,
    CONCAT('$', FORMAT(
        (SELECT portfolio_value FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1), 2
    )) AS final_value,
    CONCAT(ROUND(
        (SELECT cumulative_return FROM backtest_results
         WHERE backtest_id = b.backtest_id ORDER BY date DESC LIMIT 1) * 100, 2
    ), '%') AS total_return
FROM backtests b
WHERE b.portfolio_id = 1 AND b.status = 'Completed'
ORDER BY total_return DESC;
```

### Use Case 2: หา Portfolio ที่มี Risk-Adjusted Return ดีที่สุด

```sql
-- คำนวณ Sharpe Ratio และ Sortino Ratio
SELECT
    p.name AS portfolio_name,
    b.strategy_type,
    ROUND(AVG(br.daily_return) * 252 * 100, 2) AS annualized_return_pct,
    ROUND(STDDEV(br.daily_return) * SQRT(252) * 100, 2) AS volatility_pct,
    ROUND((AVG(br.daily_return) * 252) / (STDDEV(br.daily_return) * SQRT(252)), 2) AS sharpe_ratio
FROM backtests b
JOIN backtest_results br ON b.backtest_id = br.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
WHERE b.status = 'Completed'
GROUP BY p.name, b.strategy_type
ORDER BY sharpe_ratio DESC
LIMIT 5;
```

### Use Case 3: วิเคราะห์ Maximum Drawdown

```sql
-- หา Maximum Drawdown ของแต่ละ Portfolio
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
    CONCAT(ROUND(MIN((pp.portfolio_value - pp.peak_value) / pp.peak_value * 100), 2), '%') AS max_drawdown
FROM portfolio_peaks pp
JOIN backtests b ON pp.backtest_id = b.backtest_id
JOIN portfolios p ON b.portfolio_id = p.portfolio_id
GROUP BY b.backtest_id, p.name
ORDER BY max_drawdown ASC;
```

### Use Case 4: Portfolio Diversification Analysis

```sql
-- วิเคราะห์ความหลากหลายของ Portfolio
SELECT
    p.name AS portfolio_name,
    COUNT(DISTINCT e.asset_class) AS num_asset_classes,
    COUNT(pa.ticker) AS num_holdings,
    GROUP_CONCAT(DISTINCT e.asset_class SEPARATOR ', ') AS asset_classes,
    CONCAT(ROUND(SUM(pa.weight * e.expense_ratio) / SUM(pa.weight), 4), '%') AS weighted_avg_expense
FROM portfolios p
JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
JOIN etfs e ON pa.ticker = e.ticker
GROUP BY p.portfolio_id, p.name
ORDER BY num_asset_classes DESC;
```

## 📝 คำอธิบายความแตกต่าง MySQL vs PostgreSQL

### ความแตกต่างหลักของ MySQL Script นี้

| คุณสมบัติ | MySQL | PostgreSQL | หมายเหตุ |
|-----------|-------|------------|----------|
| **Auto Increment** | `AUTO_INCREMENT` | `SERIAL` หรือ `GENERATED AS IDENTITY` | MySQL ใช้ AUTO_INCREMENT |
| **Boolean Type** | `BOOLEAN` (เป็น TINYINT(1)) | `BOOLEAN` (แยก type จริง) | MySQL แปลง BOOLEAN เป็น 0/1 |
| **Date/Time Functions** | `CURDATE()`, `CURRENT_TIMESTAMP` | `CURRENT_DATE`, `NOW()` | MySQL ใช้ชื่อย่อได้ |
| **Check Constraints** | รองรับตั้งแต่ 8.0.16+ | รองรับตั้งแต่เวอร์ชันแรก | ใน MySQL เก่าต้องใช้ Trigger |
| **JSON Type** | `JSON` + JSON functions | `JSON` / `JSONB` | MySQL มี JSON native type |
| **String Concatenation** | `CONCAT()` | `||` หรือ `CONCAT()` | MySQL ใช้ function เสมอ |
| **LIMIT Syntax** | `LIMIT 10` | `LIMIT 10` หรือ `FETCH FIRST 10 ROWS` | MySQL ใช้ LIMIT เท่านั้น |
| **Sequence** | ไม่มี (ใช้ AUTO_INCREMENT) | `CREATE SEQUENCE` | PostgreSQL มี Sequence object |
| **String Type** | `VARCHAR(255)` default | `VARCHAR(255)` หรือ `TEXT` | MySQL มี length limit ที่ชัดเจน |
| **ON UPDATE CASCADE** | รองรับ | รองรับ | ทั้งคู่รองรับ |
| **Views** | `CREATE OR REPLACE VIEW` | `CREATE OR REPLACE VIEW` | Syntax เหมือนกัน |
| **Window Functions** | รองรับตั้งแต่ 8.0+ | รองรับตั้งแต่ 8.4+ | ทั้งคู่รองรับแล้ว |
| **CTE (WITH clause)** | รองรับตั้งแต่ 8.0+ | รองรับ | PostgreSQL รองรับก่อน |
| **Storage Engine** | `ENGINE=InnoDB` | ไม่ต้องระบุ | MySQL มีหลาย Engine |
| **Character Set** | `CHARACTER SET utf8mb4` | `ENCODING 'UTF8'` | Syntax ต่างกัน |
| **Case Sensitivity** | ตาราง/ฐานข้อมูลขึ้นกับ OS | ทุกอย่างเป็น lowercase | MySQL บน Windows ไม่ case-sensitive |

### สิ่งที่ต้องแก้ไขหากต้องการใช้ PostgreSQL

1. **เปลี่ยน AUTO_INCREMENT เป็น SERIAL**
```sql
-- MySQL
user_id INT AUTO_INCREMENT

-- PostgreSQL
user_id SERIAL
```

2. **เปลี่ยน Engine และ Charset Declaration**
```sql
-- MySQL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- PostgreSQL (ไม่ต้องระบุ)
);
```

3. **เปลี่ยน CONCAT ใน GROUP_CONCAT**
```sql
-- MySQL
GROUP_CONCAT(ticker SEPARATOR ', ')

-- PostgreSQL
STRING_AGG(ticker, ', ')
```

4. **เปลี่ยน LAST_INSERT_ID()**
```sql
-- MySQL
SET @portfolio_id = LAST_INSERT_ID();

-- PostgreSQL
RETURNING portfolio_id INTO portfolio_id;
```

5. **Stored Procedure Syntax**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE sp_name() BEGIN ... END //
DELIMITER ;

-- PostgreSQL
CREATE OR REPLACE FUNCTION sp_name() RETURNS void AS $$
BEGIN ... END;
$$ LANGUAGE plpgsql;
```

## 🔒 Security Best Practices

1. **เปลี่ยน Default Password** - อย่าใช้ password ตัวอย่างในไฟล์
2. **สร้าง User แยก** - อย่าใช้ root user ใน Production
3. **ใช้ Prepared Statements** - เมื่อเขียน Application code
4. **Backup ข้อมูลสม่ำเสมอ** - ใช้ `mysqldump` หรือ MySQL Enterprise Backup
5. **จำกัด Privileges** - ให้สิทธิ์เฉพาะที่จำเป็น

```sql
-- สร้าง User สำหรับ Application
CREATE USER 'etf_app'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT SELECT, INSERT, UPDATE, DELETE ON etf_backtesting.* TO 'etf_app'@'localhost';
FLUSH PRIVILEGES;
```

## 📈 Performance Tips

1. **สร้าง Indexes สำหรับ Foreign Keys** - รวมอยู่ในไฟล์แล้ว
2. **Partition ตาราง daily_prices** - สำหรับข้อมูลหลายล้านแถว
```sql
ALTER TABLE daily_prices
PARTITION BY RANGE (YEAR(date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

3. **ใช้ Summary Tables** - สำหรับ Analytics ที่ซับซ้อน
4. **Cache Views** - หาก query ช้า
5. **Monitor Slow Queries** - เปิด slow query log

## 🛠️ การ Maintain Database

### Backup

```bash
# Full backup
mysqldump -u root -p etf_backtesting > backup_$(date +%Y%m%d).sql

# Backup เฉพาะ schema
mysqldump -u root -p --no-data etf_backtesting > schema_only.sql

# Backup เฉพาะ data
mysqldump -u root -p --no-create-info etf_backtesting > data_only.sql
```

### Restore

```bash
mysql -u root -p etf_backtesting < backup_20231231.sql
```

### ตรวจสอบขนาด Database

```sql
SELECT
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES
WHERE table_schema = 'etf_backtesting'
ORDER BY (data_length + index_length) DESC;
```

## 📞 Support และเอกสารเพิ่มเติม

- MySQL Documentation: https://dev.mysql.com/doc/
- MySQL Workbench: https://www.mysql.com/products/workbench/
- Sample Data Sources:
  - Yahoo Finance API
  - Alpha Vantage API
  - IEX Cloud API

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

---

**Version**: 1.0.0
**Last Updated**: 2024
**Database**: MySQL 8.0+
**Author**: ETF Backtesting System Team
