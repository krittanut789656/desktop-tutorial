# วิธีการ Verify Data บน MySQL - คู่มือฉบับสมบูรณ์

## 🎯 Overview

เอกสารนี้รวมคำสั่ง SQL สำหรับตรวจสอบความถูกต้องและครบถ้วนของข้อมูลใน ETF Backtester Database

---

## 🚀 เริ่มต้น: เข้าสู่ MySQL

```bash
mysql -u root -p
```

พิมพ์รหัสผ่านแล้วรัน:

```sql
USE etf_backtester_db;
```

---

## ✅ ขั้นตอนที่ 1: ตรวจสอบตารางทั้งหมด

### 1.1 ดูรายชื่อตารางทั้งหมด

```sql
SHOW TABLES;
```

**ผลลัพธ์ที่ต้องการ:**
```
+-------------------------------+
| Tables_in_etf_backtester_db   |
+-------------------------------+
| ETF_Master                     |
| Price_Data                     |
| Strategy_Log                   |
+-------------------------------+
3 rows in set
```

✅ **ต้องมี 3 ตาราง**

---

### 1.2 ตรวจสอบจำนวนข้อมูลในแต่ละตาราง

```sql
-- นับจำนวน records ทั้ง 3 ตาราง
SELECT
    'ETF_Master' as Table_Name,
    COUNT(*) as Row_Count
FROM ETF_Master

UNION ALL

SELECT
    'Price_Data' as Table_Name,
    COUNT(*) as Row_Count
FROM Price_Data

UNION ALL

SELECT
    'Strategy_Log' as Table_Name,
    COUNT(*) as Row_Count
FROM Strategy_Log;
```

**ผลลัพธ์ที่ต้องการ:**
```
+-------------+-----------+
| Table_Name  | Row_Count |
+-------------+-----------+
| ETF_Master  |        50 |
| Price_Data  |    25,933 |
| Strategy_Log|         X | (ขึ้นอยู่กับการรัน backtest)
+-------------+-----------+
```

✅ **ETF_Master ต้องมี 50 rows**
✅ **Price_Data ต้องมี ~25,000-26,000 rows**

---

## ✅ ขั้นตอนที่ 2: ตรวจสอบ ETF_Master Table

### 2.1 ตรวจสอบจำนวน ETF ตาม Asset Type

```sql
SELECT
    Asset_Type,
    COUNT(*) as จำนวน_ETF,
    GROUP_CONCAT(Ticker_Symbol ORDER BY Ticker_Symbol SEPARATOR ', ') as ETF_List
FROM ETF_Master
GROUP BY Asset_Type
ORDER BY Asset_Type;
```

**ผลลัพธ์ที่ต้องการ:**
```
+------------+--------------+----------------------------------+
| Asset_Type | จำนวน_ETF   | ETF_List                         |
+------------+--------------+----------------------------------+
| Bond       |           15 | AGG, BND, BNDX, EMB, GOVT, ...  |
| Commodity  |            5 | DBA, DBC, GLD, SLV, USO         |
| Equity     |           25 | ARKF, ARKG, ARKK, ARKW, DIA,... |
| Mixed      |            5 | AOK, AOM, AOR, GAL, INKM        |
+------------+--------------+----------------------------------+
```

✅ **Bond: 15 ETFs**
✅ **Commodity: 5 ETFs**
✅ **Equity: 25 ETFs**
✅ **Mixed: 5 ETFs**

---

### 2.2 ตรวจสอบ Duplicate Ticker Symbols

```sql
SELECT
    Ticker_Symbol,
    COUNT(*) as จำนวน
FROM ETF_Master
GROUP BY Ticker_Symbol
HAVING COUNT(*) > 1;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

✅ **ต้องไม่มี Duplicate**

---

### 2.3 ตรวจสอบ NULL values

```sql
SELECT
    SUM(CASE WHEN ETF_ID IS NULL THEN 1 ELSE 0 END) as Null_ETF_ID,
    SUM(CASE WHEN Ticker_Symbol IS NULL THEN 1 ELSE 0 END) as Null_Ticker,
    SUM(CASE WHEN ETF_Name IS NULL THEN 1 ELSE 0 END) as Null_Name,
    SUM(CASE WHEN Asset_Type IS NULL THEN 1 ELSE 0 END) as Null_Asset_Type,
    COUNT(*) as Total_Records
FROM ETF_Master;
```

**ผลลัพธ์ที่ต้องการ:**
```
+--------------+-------------+-----------+-----------------+---------------+
| Null_ETF_ID  | Null_Ticker | Null_Name | Null_Asset_Type | Total_Records |
+--------------+-------------+-----------+-----------------+---------------+
|            0 |           0 |         0 |               0 |            50 |
+--------------+-------------+-----------+-----------------+---------------+
```

✅ **ไม่มี NULL ในคอลัมน์หลัก**

---

### 2.4 แสดง ETF ทั้งหมด 50 ตัว

```sql
SELECT
    ETF_ID,
    Ticker_Symbol,
    ETF_Name,
    Asset_Type,
    Expense_Ratio
FROM ETF_Master
ORDER BY Asset_Type, Ticker_Symbol;
```

✅ **ตรวจสอบว่ามีครบ 50 ETFs และเป็น Real ETFs**

---

## ✅ ขั้นตอนที่ 3: ตรวจสอบ Price_Data Table

### 3.1 ตรวจสอบช่วงวันที่และความครบถ้วน

```sql
SELECT
    MIN(Price_Date) as วันแรก,
    MAX(Price_Date) as วันล่าสุด,
    DATEDIFF(MAX(Price_Date), MIN(Price_Date)) as จำนวนวัน,
    ROUND(DATEDIFF(MAX(Price_Date), MIN(Price_Date)) / 365.25, 1) as จำนวนปี,
    COUNT(DISTINCT Price_Date) as จำนวนสัปดาห์ที่ไม่ซ้ำ,
    COUNT(DISTINCT ETF_ID) as จำนวน_ETF,
    COUNT(*) as จำนวน_Records_ทั้งหมด
FROM Price_Data;
```

**ผลลัพธ์ที่ต้องการ:**
```
+------------+--------------+--------------+--------------+-------------------------+-------------+-----------------------------+
| วันแรก     | วันล่าสุด    | จำนวนวัน     | จำนวนปี      | จำนวนสัปดาห์ที่ไม่ซ้ำ   | จำนวน_ETF   | จำนวน_Records_ทั้งหมด      |
+------------+--------------+--------------+--------------+-------------------------+-------------+-----------------------------+
| 2015-11-23 | 2025-11-18   |        3652  |         10.0 |                     521 |          50 |                      25,933 |
+------------+--------------+--------------+--------------+-------------------------+-------------+-----------------------------+
```

✅ **ข้อมูลครอบคลุม ~10 ปี**
✅ **มี ~520 สัปดาห์**
✅ **มี 50 ETFs**

---

### 3.2 ตรวจสอบจำนวน Records ของแต่ละ ETF

```sql
SELECT
    em.ETF_ID,
    em.Ticker_Symbol,
    em.ETF_Name,
    em.Asset_Type,
    COUNT(pd.Price_ID) as จำนวนราคา,
    MIN(pd.Price_Date) as วันแรก,
    MAX(pd.Price_Date) as วันล่าสุด,
    ROUND(DATEDIFF(MAX(pd.Price_Date), MIN(pd.Price_Date)) / 365.25, 1) as ปี
FROM ETF_Master em
LEFT JOIN Price_Data pd ON em.ETF_ID = pd.ETF_ID
GROUP BY em.ETF_ID, em.Ticker_Symbol, em.ETF_Name, em.Asset_Type
ORDER BY จำนวนราคา DESC, em.Ticker_Symbol;
```

**ผลลัพธ์ที่ต้องการ:**
```
+--------+---------------+-----------------------------+------------+--------------+------------+--------------+------+
| ETF_ID | Ticker_Symbol | ETF_Name                    | Asset_Type | จำนวนราคา    | วันแรก     | วันล่าสุด    | ปี   |
+--------+---------------+-----------------------------+------------+--------------+------------+--------------+------+
|      1 | SPY           | SPDR S&P 500 ETF Trust      | Equity     |          521 | 2015-11-23 | 2025-11-18   | 10.0 |
|      2 | QQQ           | Invesco QQQ Trust           | Equity     |          521 | 2015-11-23 | 2025-11-18   | 10.0 |
|      3 | IWM           | iShares Russell 2000 ETF    | Equity     |          521 | 2015-11-23 | 2025-11-18   | 10.0 |
...
+--------+---------------+-----------------------------+------------+--------------+------------+--------------+------+
```

✅ **แต่ละ ETF ควรมี ~500-521 records**
✅ **ไม่มี ETF ไหนมี 0 records**

---

### 3.3 ตรวจสอบ ETF ที่ข้อมูลน้อยผิดปกติ

```sql
SELECT
    em.ETF_ID,
    em.Ticker_Symbol,
    em.ETF_Name,
    COUNT(pd.Price_ID) as จำนวนราคา
FROM ETF_Master em
LEFT JOIN Price_Data pd ON em.ETF_ID = pd.ETF_ID
GROUP BY em.ETF_ID, em.Ticker_Symbol, em.ETF_Name
HAVING COUNT(pd.Price_ID) < 400  -- ETF ที่มีข้อมูลน้อยกว่า 400 records
ORDER BY จำนวนราคา ASC;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

✅ **ทุก ETF ควรมีข้อมูลครบ (>400 records)**

---

### 3.4 ตรวจสอบ Duplicate Records

```sql
SELECT
    ETF_ID,
    Price_Date,
    COUNT(*) as จำนวน
FROM Price_Data
GROUP BY ETF_ID, Price_Date
HAVING COUNT(*) > 1;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

✅ **ไม่มี Duplicate (ETF_ID, Price_Date)**

---

### 3.5 ตรวจสอบ NULL values ในราคา

```sql
SELECT
    SUM(CASE WHEN Close_Price IS NULL THEN 1 ELSE 0 END) as Null_Close,
    SUM(CASE WHEN Open_Price IS NULL THEN 1 ELSE 0 END) as Null_Open,
    SUM(CASE WHEN High_Price IS NULL THEN 1 ELSE 0 END) as Null_High,
    SUM(CASE WHEN Low_Price IS NULL THEN 1 ELSE 0 END) as Null_Low,
    SUM(CASE WHEN Volume IS NULL OR Volume = 0 THEN 1 ELSE 0 END) as Zero_Volume,
    COUNT(*) as Total_Records
FROM Price_Data;
```

**ผลลัพธ์ที่ต้องการ:**
```
+------------+-----------+-----------+----------+-------------+---------------+
| Null_Close | Null_Open | Null_High | Null_Low | Zero_Volume | Total_Records |
+------------+-----------+-----------+----------+-------------+---------------+
|          0 |         0 |         0 |        0 |           0 |        25,933 |
+------------+-----------+-----------+----------+-------------+---------------+
```

✅ **ไม่มี NULL ในราคาหลัก**

---

### 3.6 ตรวจสอบความสมเหตุสมผลของราคา (OHLC Logic)

```sql
-- ตรวจสอบว่า High >= Low
SELECT
    COUNT(*) as Records_With_Invalid_High_Low
FROM Price_Data
WHERE High_Price < Low_Price;
```

**ผลลัพธ์ที่ต้องการ:**
```
+--------------------------------+
| Records_With_Invalid_High_Low  |
+--------------------------------+
|                              0 |
+--------------------------------+
```

✅ **High ต้อง >= Low เสมอ**

---

```sql
-- ตรวจสอบว่า Close อยู่ระหว่าง Low-High
SELECT
    COUNT(*) as Records_With_Close_Out_Of_Range
FROM Price_Data
WHERE Close_Price < Low_Price
   OR Close_Price > High_Price;
```

**ผลลัพธ์ที่ต้องการ:**
```
+-----------------------------------+
| Records_With_Close_Out_Of_Range   |
+-----------------------------------+
|                                 0 |
+-----------------------------------+
```

✅ **Close ต้องอยู่ระหว่าง Low-High**

---

### 3.7 ดูข้อมูลตัวอย่าง - SPY (S&P 500 ETF)

```sql
SELECT
    pd.Price_Date,
    pd.Open_Price,
    pd.High_Price,
    pd.Low_Price,
    pd.Close_Price,
    pd.Volume,
    em.Ticker_Symbol
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE em.Ticker_Symbol = 'SPY'
ORDER BY pd.Price_Date DESC
LIMIT 10;
```

**ผลลัพธ์ที่ต้องการ:**
```
+------------+------------+------------+-----------+-------------+-----------+---------------+
| Price_Date | Open_Price | High_Price | Low_Price | Close_Price | Volume    | Ticker_Symbol |
+------------+------------+------------+-----------+-------------+-----------+---------------+
| 2025-11-18 |    594.21  |    598.45  |   593.12  |      597.34 |  45678900 | SPY           |
| 2025-11-11 |    589.56  |    595.23  |   588.11  |      594.45 |  52341200 | SPY           |
...
+------------+------------+------------+-----------+-------------+-----------+---------------+
```

✅ **ราคาดูสมเหตุสมผล (SPY ราคาประมาณ 400-600)**

---

### 3.8 ตรวจสอบราคาผิดปกติ (Outliers)

```sql
-- หาราคาที่ต่ำผิดปกติ (< $1)
SELECT
    em.Ticker_Symbol,
    em.ETF_Name,
    pd.Price_Date,
    pd.Close_Price
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE pd.Close_Price < 1.0
ORDER BY pd.Close_Price ASC
LIMIT 10;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

หรือมี USO (oil ETF) ที่อาจมีราคาต่ำในช่วงปี 2020 (ซึ่งเป็นเรื่องปกติ)

---

```sql
-- หาราคาที่สูงผิดปกติ (> $10,000)
SELECT
    em.Ticker_Symbol,
    em.ETF_Name,
    pd.Price_Date,
    pd.Close_Price
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE pd.Close_Price > 10000
ORDER BY pd.Close_Price DESC
LIMIT 10;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

✅ **ไม่มีราคาผิดปกติมาก**

---

## ✅ ขั้นตอนที่ 4: ตรวจสอบ Foreign Key Constraints

### 4.1 ตรวจสอบ Price_Data → ETF_Master

```sql
-- หา Price records ที่ไม่มี ETF_ID ใน ETF_Master
SELECT
    pd.ETF_ID,
    COUNT(*) as จำนวน_Records
FROM Price_Data pd
LEFT JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE em.ETF_ID IS NULL
GROUP BY pd.ETF_ID;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

✅ **ทุก Price record มี ETF_ID ที่ถูกต้อง**

---

### 4.2 ตรวจสอบ Strategy_Log → ETF_Master

```sql
-- หา Strategy_Log records ที่ไม่มี ETF_ID ใน ETF_Master
SELECT
    sl.ETF_ID,
    COUNT(*) as จำนวน_Records
FROM Strategy_Log sl
LEFT JOIN ETF_Master em ON sl.ETF_ID = em.ETF_ID
WHERE em.ETF_ID IS NULL
GROUP BY sl.ETF_ID;
```

**ผลลัพธ์ที่ต้องการ:**
```
Empty set (0.00 sec)
```

✅ **ทุก Strategy_Log record มี ETF_ID ที่ถูกต้อง**

---

## ✅ ขั้นตอนที่ 5: ตรวจสอบ Strategy_Log (ถ้ามี)

### 5.1 ตรวจสอบจำนวน Backtest Runs

```sql
SELECT
    COUNT(DISTINCT Backtest_Run_ID) as จำนวน_Backtest_Runs,
    COUNT(*) as จำนวน_Records_ทั้งหมด,
    MIN(Selection_Date) as วันแรก,
    MAX(Selection_Date) as วันล่าสุด
FROM Strategy_Log;
```

---

### 5.2 ดู Backtest Runs ล่าสุด

```sql
SELECT
    sl.Backtest_Run_ID,
    sl.Selection_Date,
    sl.Lookback_Period_Days,
    COUNT(*) as จำนวน_ETF_ที่เลือก,
    AVG(sl.Holding_Return) as ผลตอบแทนเฉลี่ย
FROM Strategy_Log sl
GROUP BY sl.Backtest_Run_ID, sl.Selection_Date, sl.Lookback_Period_Days
ORDER BY sl.Selection_Date DESC
LIMIT 5;
```

---

### 5.3 ดู Top ETFs จาก Backtest ล่าสุด

```sql
SELECT
    sl.Portfolio_Rank,
    em.Ticker_Symbol,
    em.ETF_Name,
    em.Asset_Type,
    sl.Momentum_Score,
    sl.Entry_Price,
    sl.Exit_Price,
    sl.Holding_Return
FROM Strategy_Log sl
JOIN ETF_Master em ON sl.ETF_ID = em.ETF_ID
WHERE sl.Backtest_Run_ID = (
    SELECT Backtest_Run_ID
    FROM Strategy_Log
    ORDER BY Selection_Date DESC
    LIMIT 1
)
ORDER BY sl.Portfolio_Rank;
```

✅ **ดู ETFs ที่ถูกเลือกในรอบล่าสุด**

---

## ✅ ขั้นตอนที่ 6: ตรวจสอบ Data Quality - สถิติรวม

### 6.1 สรุปภาพรวมฐานข้อมูล

```sql
SELECT
    'Database Overview' as Description,
    (SELECT COUNT(*) FROM ETF_Master) as Total_ETFs,
    (SELECT COUNT(*) FROM Price_Data) as Total_Price_Records,
    (SELECT COUNT(*) FROM Strategy_Log) as Total_Strategy_Records,
    (SELECT MIN(Price_Date) FROM Price_Data) as Data_Start_Date,
    (SELECT MAX(Price_Date) FROM Price_Data) as Data_End_Date,
    ROUND((SELECT COUNT(*) FROM Price_Data) / (SELECT COUNT(*) FROM ETF_Master), 0) as Avg_Records_Per_ETF;
```

**ผลลัพธ์ตัวอย่าง:**
```
+-------------------+------------+---------------------+-------------------------+-----------------+---------------+----------------------+
| Description       | Total_ETFs | Total_Price_Records | Total_Strategy_Records  | Data_Start_Date | Data_End_Date | Avg_Records_Per_ETF  |
+-------------------+------------+---------------------+-------------------------+-----------------+---------------+----------------------+
| Database Overview |         50 |              25,933 |                       X | 2015-11-23      | 2025-11-18    |                  519 |
+-------------------+------------+---------------------+-------------------------+-----------------+---------------+----------------------+
```

✅ **ภาพรวมครบถ้วน**

---

### 6.2 สรุปราคาตาม Asset Type

```sql
SELECT
    em.Asset_Type,
    COUNT(DISTINCT em.ETF_ID) as จำนวน_ETF,
    COUNT(pd.Price_ID) as จำนวนราคา,
    MIN(pd.Close_Price) as ราคาต่ำสุด,
    MAX(pd.Close_Price) as ราคาสูงสุด,
    ROUND(AVG(pd.Close_Price), 2) as ราคาเฉลี่ย,
    SUM(pd.Volume) as Volume_รวม
FROM ETF_Master em
JOIN Price_Data pd ON em.ETF_ID = pd.ETF_ID
GROUP BY em.Asset_Type
ORDER BY em.Asset_Type;
```

---

### 6.3 ตรวจสอบความสมบูรณ์ของข้อมูลรายเดือน

```sql
SELECT
    DATE_FORMAT(Price_Date, '%Y-%m') as เดือน,
    COUNT(DISTINCT ETF_ID) as จำนวน_ETF_ที่มีข้อมูล,
    COUNT(*) as จำนวน_Records
FROM Price_Data
GROUP BY DATE_FORMAT(Price_Date, '%Y-%m')
ORDER BY เดือน DESC
LIMIT 12;
```

✅ **แต่ละเดือนควรมี 50 ETFs**

---

## ✅ ขั้นตอนที่ 7: เปรียบเทียบกับข้อมูลจริง

### 7.1 เปรียบเทียบราคา SPY ล่าสุดกับ Yahoo Finance

```sql
SELECT
    em.Ticker_Symbol,
    pd.Price_Date,
    pd.Close_Price,
    'ไปเช็คที่ https://finance.yahoo.com/quote/SPY' as ตรวจสอบที่
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE em.Ticker_Symbol = 'SPY'
ORDER BY pd.Price_Date DESC
LIMIT 1;
```

✅ **นำราคาไปเทียบกับ Yahoo Finance เพื่อยืนยันว่าเป็นข้อมูลจริง**

---

### 7.2 แสดงราคา ETF หลายตัวในวันเดียวกัน

```sql
SELECT
    em.Ticker_Symbol,
    em.ETF_Name,
    em.Asset_Type,
    pd.Close_Price,
    pd.Volume
FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
WHERE pd.Price_Date = (SELECT MAX(Price_Date) FROM Price_Data)
ORDER BY em.Asset_Type, em.Ticker_Symbol;
```

✅ **ดูราคาล่าสุดของทุก ETF พร้อมกัน**

---

## 📊 สรุป Checklist การ Verify

พิมพ์คำสั่งนี้เพื่อสรุปทั้งหมด:

```sql
-- ===== COMPLETE VERIFICATION SUMMARY =====
SELECT '1. ETF_Master Count' as Check_Item,
       CASE WHEN COUNT(*) = 50 THEN '✅ PASS' ELSE '❌ FAIL' END as Status,
       COUNT(*) as Value
FROM ETF_Master

UNION ALL

SELECT '2. Price_Data Count',
       CASE WHEN COUNT(*) > 25000 THEN '✅ PASS' ELSE '❌ FAIL' END,
       COUNT(*)
FROM Price_Data

UNION ALL

SELECT '3. Asset Types',
       CASE WHEN COUNT(DISTINCT Asset_Type) = 4 THEN '✅ PASS' ELSE '❌ FAIL' END,
       COUNT(DISTINCT Asset_Type)
FROM ETF_Master

UNION ALL

SELECT '4. No Duplicate ETF_IDs',
       CASE WHEN COUNT(*) = 0 THEN '✅ PASS' ELSE '❌ FAIL' END,
       COUNT(*)
FROM (
    SELECT ETF_ID FROM ETF_Master GROUP BY ETF_ID HAVING COUNT(*) > 1
) dup

UNION ALL

SELECT '5. No Duplicate Prices',
       CASE WHEN COUNT(*) = 0 THEN '✅ PASS' ELSE '❌ FAIL' END,
       COUNT(*)
FROM (
    SELECT ETF_ID, Price_Date FROM Price_Data GROUP BY ETF_ID, Price_Date HAVING COUNT(*) > 1
) dup2

UNION ALL

SELECT '6. All ETFs have Price Data',
       CASE WHEN COUNT(*) = 50 THEN '✅ PASS' ELSE '❌ FAIL' END,
       COUNT(*)
FROM (
    SELECT DISTINCT ETF_ID FROM Price_Data
) etfs_with_data

UNION ALL

SELECT '7. Price Data Coverage (Years)',
       CASE WHEN DATEDIFF(MAX(Price_Date), MIN(Price_Date)) > 3000 THEN '✅ PASS' ELSE '❌ FAIL' END,
       ROUND(DATEDIFF(MAX(Price_Date), MIN(Price_Date)) / 365.25, 1)
FROM Price_Data

UNION ALL

SELECT '8. Valid OHLC Logic',
       CASE WHEN COUNT(*) = 0 THEN '✅ PASS' ELSE '❌ FAIL' END,
       COUNT(*)
FROM Price_Data
WHERE High_Price < Low_Price
   OR Close_Price < Low_Price
   OR Close_Price > High_Price;
```

**ผลลัพธ์ที่ต้องการ:**
```
+-------------------------------+----------+--------+
| Check_Item                    | Status   | Value  |
+-------------------------------+----------+--------+
| 1. ETF_Master Count           | ✅ PASS  |     50 |
| 2. Price_Data Count           | ✅ PASS  | 25,933 |
| 3. Asset Types                | ✅ PASS  |      4 |
| 4. No Duplicate ETF_IDs       | ✅ PASS  |      0 |
| 5. No Duplicate Prices        | ✅ PASS  |      0 |
| 6. All ETFs have Price Data   | ✅ PASS  |     50 |
| 7. Price Data Coverage (Years)| ✅ PASS  |   10.0 |
| 8. Valid OHLC Logic           | ✅ PASS  |      0 |
+-------------------------------+----------+--------+
```

---

## 🎯 การนำเสนอผลการ Verify ต่ออาจารย์

เมื่อ Demo ให้อาจารย์ สามารถรันคำสั่งเหล่านี้เพื่อแสดงว่า:

1. **ข้อมูลครบถ้วน** - มี 50 ETFs จริง, 25,933 price records
2. **ข้อมูลถูกต้อง** - ไม่มี duplicates, NULL values, หรือราคาผิดปกติ
3. **ข้อมูลเป็น Real Data** - เปรียบเทียบราคา SPY กับ Yahoo Finance ตรงกัน
4. **Database Design ถูกต้อง** - มี Primary Keys, Foreign Keys, Constraints
5. **ข้อมูลครอบคลุม 10 ปี** - จาก 2015 ถึง 2025

---

## 💾 Export ผลการ Verify

หากต้องการ Export ผลการตรวจสอบ:

```sql
-- Export เป็น CSV (จาก MySQL command line)
SELECT * FROM ETF_Master
INTO OUTFILE '/tmp/etf_master_verify.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

หรือใช้:

```bash
mysql -u root -p etf_backtester_db -e "SELECT * FROM ETF_Master" > etf_verify.txt
```

---

## 🚀 คำสั่งด่วน - Copy & Paste

คัดลอกทั้งหมดรันเลย:

```sql
USE etf_backtester_db;

-- Quick Verify
SELECT 'ETF_Master' as Table_Name, COUNT(*) as Records FROM ETF_Master
UNION ALL
SELECT 'Price_Data', COUNT(*) FROM Price_Data
UNION ALL
SELECT 'Strategy_Log', COUNT(*) FROM Strategy_Log;

-- Asset Type Distribution
SELECT Asset_Type, COUNT(*) as Count FROM ETF_Master GROUP BY Asset_Type;

-- Date Range
SELECT MIN(Price_Date) as Start, MAX(Price_Date) as End, COUNT(*) as Records FROM Price_Data;

-- Sample Data
SELECT pd.*, em.Ticker_Symbol FROM Price_Data pd
JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
ORDER BY pd.Price_Date DESC LIMIT 10;
```

---

**ข้อมูลทั้งหมดเป็น 100% REAL จาก Yahoo Finance!** 📊✅
