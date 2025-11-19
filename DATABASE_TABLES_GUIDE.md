# 📊 Database Tables - สรุปการใช้งาน

**Portfolio Backtesting System - Database Schema Overview**

---

## 🗂️ **Tables ทั้งหมด (9 Tables)**

### **✅ Tables ที่ใช้งานแล้ว (4 Tables)**

#### **1. `etf_master`** - ข้อมูล ETF หลัก ✅
**โครงสร้าง:**
- `etf_id` (Primary Key)
- `ticker_symbol` (SPY, QQQ, AGG, etc.)
- `etf_name` (S&P 500 ETF, Nasdaq 100, etc.)
- `asset_class` (Equity, Bond, Commodity, etc.)
- `region`, `sector`
- `expense_ratio`, `inception_date`

**ใช้งานใน:**
- ✅ **main.py** → Module 1: ETF Management (CRUD)
  - View All ETFs
  - Create ETF
  - Update ETF
  - Delete ETF
  - Search ETF
- ✅ **Analytics** → ทุก Feature ต้องใช้ข้อมูล ETF
- ✅ **SQL Views** → `vw_weekly_returns`, `vw_etf_performance`
- ✅ **live_demo** → แสดงรายชื่อ ETF, Top Performers

**ตัวอย่างข้อมูล:**
| etf_id | ticker | etf_name | asset_class |
|--------|--------|----------|-------------|
| 1 | SPY | S&P 500 ETF | Equity |
| 2 | AGG | US Aggregate Bond | Bond |

---

#### **2. `price_history`** - ข้อมูลราคา (จาก Yahoo Finance) ✅
**โครงสร้าง:**
- `price_id` (Primary Key)
- `etf_id` (Foreign Key → etf_master)
- `date` (วันที่ข้อมูล)
- `open`, `high`, `low`, `close`, `adj_close`
- `volume`

**ใช้งานใน:**
- ✅ **SQL View: `vw_weekly_returns`**
  - คำนวณ weekly returns ด้วย Window Functions (LAG, OVER)
- ✅ **SQL View: `vw_etf_performance`**
  - คำนวณ annualized return, volatility, Sharpe ratio
- ✅ **Analytics**
  - Top Performers
  - Portfolio Comparison
  - Correlation Analysis

**ข้อมูล:**
- 208,700+ records (50 ETFs × 16 years)
- Import จาก CSV: `data/etf_price_history.csv`

**ตัวอย่างข้อมูล:**
| price_id | etf_id | date | adj_close |
|----------|--------|------------|-----------|
| 1 | 1 | 2009-01-05 | 90.28 |
| 2 | 1 | 2009-01-12 | 87.71 |

---

#### **3. `benchmark_portfolios`** - Portfolio Templates ✅
**โครงสร้าง:**
- `benchmark_id` (Primary Key)
- `benchmark_name` (60/40 Portfolio, All Weather, etc.)
- `description`
- `risk_level` (Conservative, Moderate, Aggressive)
- `target_return`
- `asset_allocation`

**ใช้งานใน:**
- ✅ **main.py** → Module 2: Portfolio Management (CRUD)
  - View All Portfolios
  - Create Portfolio
  - Update Portfolio
  - Delete Portfolio
- ✅ **Analytics** → Portfolio Comparison
- ✅ **SQL View: `vw_portfolio_summary`**
- ✅ **Stored Procedure: `sp_compare_portfolios`**

**ข้อมูล:**
- 35 benchmark portfolios
- Insert จาก `complete_setup.sql`

**ตัวอย่างข้อมูล:**
| benchmark_id | benchmark_name | risk_level |
|--------------|----------------|------------|
| 1 | 60/40 Portfolio | Moderate |
| 2 | All Weather Portfolio | Conservative |

---

#### **4. `benchmark_holdings`** - Holdings ของแต่ละ Portfolio ✅
**โครงสร้าง:**
- `holding_id` (Primary Key)
- `benchmark_id` (Foreign Key → benchmark_portfolios)
- `etf_id` (Foreign Key → etf_master)
- `target_weight` (น้ำหนัก 0.00-1.00)

**ใช้งานใน:**
- ✅ **Portfolio Management** → View Portfolio Detail
- ✅ **Analytics** → Portfolio Comparison
- ✅ **Stored Procedure: `sp_get_portfolio_weights`**
  - แสดงน้ำหนักของ ETF แต่ละตัวใน Portfolio
- ✅ **Stored Procedure: `sp_compare_portfolios`**
  - คำนวณ weighted average return

**ตัวอย่างข้อมูล:**
| holding_id | benchmark_id | etf_id | target_weight |
|------------|--------------|--------|---------------|
| 1 | 1 | 1 | 0.6000 | (60% SPY)
| 2 | 1 | 2 | 0.4000 | (40% AGG)

---

### **⏳ Tables ที่ยังไม่ได้ใช้ (5 Tables)**

#### **5. `backtest_scenarios`** - Scenarios สำหรับ Backtesting ⏳
**โครงสร้าง:**
- `scenario_id` (Primary Key)
- `benchmark_id` (Foreign Key)
- `created_by` (ชื่อผู้สร้าง)
- `scenario_name` (ชื่อ scenario)
- `initial_capital` (เงินลงทุนเริ่มต้น)
- `start_date`, `end_date`
- `strategy_type` (BUY_HOLD, REBALANCE, DCA)
- `rebalance_freq` (MONTHLY, QUARTERLY, etc.)
- `monthly_contribution` (เงินเพิ่มรายเดือน)

**จะใช้ทำอะไร:**
- 🔄 **Backtesting Feature** (ยังไม่ได้ implement)
- กำหนดเงื่อนไข backtesting แต่ละครั้ง
- เปรียบเทียบ strategies ต่างๆ (Buy & Hold vs Rebalance vs DCA)
- ทดสอบ portfolio ในช่วงเวลาต่างๆ

**ตัวอย่างการใช้งานในอนาคต:**
```sql
INSERT INTO backtest_scenarios
(benchmark_id, created_by, scenario_name, initial_capital,
 start_date, end_date, strategy_type, rebalance_freq)
VALUES
(1, 'Student01', 'Test 60/40 with Monthly Rebalance', 100000.00,
 '2020-01-01', '2024-12-31', 'REBALANCE', 'MONTHLY');
```

**Feature ที่จะพัฒนาต่อ:**
- สร้าง Backtest Scenario ใหม่
- รัน Backtest และเก็บผลลัพธ์
- เปรียบเทียบ Scenarios หลายๆ อัน

---

#### **6. `scenario_holdings`** - Holdings ของแต่ละ Scenario ⏳
**โครงสร้าง:**
- `holding_id` (Primary Key)
- `scenario_id` (Foreign Key → backtest_scenarios)
- `etf_id` (Foreign Key → etf_master)
- `target_weight` (น้ำหนัก)

**จะใช้ทำอะไร:**
- เก็บน้ำหนักของ ETF แต่ละตัวในแต่ละ scenario
- รองรับการ customize portfolio สำหรับ backtesting
- ทดสอบ portfolio ที่ผู้ใช้สร้างเอง (ไม่ใช่ benchmark)

**ตัวอย่างการใช้งานในอนาคต:**
```sql
-- Scenario: Custom Portfolio (70% SPY, 30% AGG)
INSERT INTO scenario_holdings
(scenario_id, etf_id, target_weight)
VALUES
(1, 1, 0.70),  -- 70% SPY
(1, 2, 0.30);  -- 30% AGG
```

---

#### **7. `backtest_results`** - ผลลัพธ์จาก Backtesting ⏳
**โครงสร้าง:**
- `result_id` (Primary Key)
- `scenario_id` (Foreign Key)
- `total_return` (ผลตอบแทนรวม)
- `annualized_return` (ผลตอบแทนต่อปี)
- `volatility` (ความผันผวน)
- `max_drawdown` (การขาดทุนสูงสุด)
- `sharpe_ratio`
- `final_value` (มูลค่าสุดท้าย)
- `vs_benchmark_alpha` (เทียบกับ benchmark)

**จะใช้ทำอะไร:**
- เก็บผลลัพธ์จากการรัน backtest
- เปรียบเทียบ scenarios หลายๆ อัน
- แสดงรายงานผลลัพธ์

**ตัวอย่างการใช้งานในอนาคต:**
```sql
-- หลังจากรัน backtest เสร็จ
INSERT INTO backtest_results
(scenario_id, total_return, annualized_return, volatility,
 max_drawdown, sharpe_ratio, final_value)
VALUES
(1, 45.50, 0.0852, 0.1420, -0.1850, 1.15, 145500.00);
```

**Feature ที่จะพัฒนาต่อ:**
- แสดงผลลัพธ์ Backtest แบบ Summary
- เปรียบเทียบหลาย Scenarios
- Export รายงาน

---

#### **8. `portfolio_snapshots`** - Snapshots ของ Portfolio ตามเวลา ⏳
**โครงสร้าง:**
- `snapshot_id` (Primary Key)
- `scenario_id` (Foreign Key)
- `etf_id` (Foreign Key)
- `snapshot_date` (วันที่บันทึก)
- `shares_held` (จำนวนหุ้น)
- `market_value` (มูลค่าตลาด)
- `portfolio_weight` (น้ำหนักจริง)
- `unrealized_gain` (กำไร/ขาดทุนที่ยังไม่ realize)

**จะใช้ทำอะไร:**
- บันทึกสถานะ portfolio ณ แต่ละจุดเวลา
- ติดตาม portfolio performance ตามเวลา
- แสดงกราฟ portfolio value over time
- ตรวจสอบว่า portfolio drift จาก target weight หรือไม่

**ตัวอย่างการใช้งานในอนาคต:**
```sql
-- บันทึก snapshot ทุกสิ้นเดือน
INSERT INTO portfolio_snapshots
(scenario_id, etf_id, snapshot_date, shares_held,
 market_value, portfolio_weight)
VALUES
(1, 1, '2024-01-31', 150.5000, 75250.00, 0.6020);  -- SPY
```

**Feature ที่จะพัฒนาต่อ:**
- แสดงกราฟ Portfolio Value Over Time
- Rebalancing Alert (เมื่อ weight เบี่ยงเบนมาก)
- Performance Tracking

---

#### **9. `transaction_log`** - บันทึก Transactions ⏳
**โครงสร้าง:**
- `transaction_id` (Primary Key)
- `scenario_id` (Foreign Key)
- `etf_id` (Foreign Key)
- `trans_date` (วันที่ทำ transaction)
- `trans_type` (BUY, SELL, REBALANCE)
- `shares` (จำนวนหุ้น)
- `price` (ราคาต่อหุ้น)
- `amount` (จำนวนเงิน)
- `reason` (เหตุผล)

**จะใช้ทำอะไร:**
- บันทึกทุก transaction ที่เกิดขึ้นใน backtest
- ติดตาม trading activity
- คำนวณ transaction costs
- ตรวจสอบ rebalancing frequency

**ตัวอย่างการใช้งานในอนาคต:**
```sql
-- บันทึกการซื้อ SPY
INSERT INTO transaction_log
(scenario_id, etf_id, trans_date, trans_type,
 shares, price, amount, reason)
VALUES
(1, 1, '2020-01-05', 'BUY', 100.0000,
 320.50, 32050.00, 'Initial Purchase');

-- บันทึกการ Rebalance
INSERT INTO transaction_log
(scenario_id, etf_id, trans_date, trans_type,
 shares, price, amount, reason)
VALUES
(1, 1, '2020-04-01', 'SELL', 10.5000,
 285.20, 2994.60, 'Monthly Rebalance - Reduce to 60%');
```

**Feature ที่จะพัฒนาต่อ:**
- Transaction History Report
- ค่าใช้จ่าย (Transaction Costs) Analysis
- Turnover Rate Calculation

---

## 📊 **สรุปการใช้งาน Tables**

### **✅ ใช้งานแล้ว (4/9 Tables = 44%)**

| Table | ใช้ใน Feature | สถานะ |
|-------|--------------|-------|
| `etf_master` | ETF CRUD, Analytics, SQL Views | ✅ ใช้งานแล้ว |
| `price_history` | Analytics, SQL Views (vw_weekly_returns) | ✅ ใช้งานแล้ว |
| `benchmark_portfolios` | Portfolio CRUD, Analytics | ✅ ใช้งานแล้ว |
| `benchmark_holdings` | Portfolio Management, Analytics | ✅ ใช้งานแล้ว |

### **⏳ ยังไม่ได้ใช้ (5/9 Tables = 56%)**

| Table | จะใช้ทำอะไร | เมื่อไหร่ |
|-------|------------|----------|
| `backtest_scenarios` | สร้าง Backtest Scenarios | 🔄 Phase 2 |
| `scenario_holdings` | กำหนด Holdings ของ Scenarios | 🔄 Phase 2 |
| `backtest_results` | เก็บผลลัพธ์ Backtesting | 🔄 Phase 2 |
| `portfolio_snapshots` | ติดตาม Portfolio Over Time | 🔄 Phase 2 |
| `transaction_log` | บันทึก Transactions | 🔄 Phase 2 |

---

## 🔄 **Phase 2 Features (ถ้ามีเวลาพัฒนาต่อ)**

### **Feature 1: Backtesting System** 🚀
**ใช้ Tables:**
- `backtest_scenarios` (กำหนด scenario)
- `scenario_holdings` (กำหนด holdings)
- `backtest_results` (เก็บผลลัพธ์)
- `portfolio_snapshots` (บันทึก snapshots)
- `transaction_log` (บันทึก transactions)

**ทำอะไรได้:**
- สร้าง Backtest Scenario ใหม่
- เลือก Strategy (Buy & Hold, Rebalance, DCA)
- รัน Backtest และดูผลลัพธ์
- เปรียบเทียบ Strategies หลายๆ อัน
- ดูกราฟ Portfolio Value Over Time
- ดู Transaction History

**ตัวอย่าง Use Case:**
```
1. สร้าง Scenario: "Test 60/40 with Monthly Rebalance"
   - Initial Capital: $100,000
   - Period: 2020-2024
   - Strategy: Rebalance Monthly

2. รัน Backtest → ได้ผลลัพธ์:
   - Total Return: 45.5%
   - Annualized Return: 8.52%
   - Sharpe Ratio: 1.15
   - Max Drawdown: -18.5%

3. เปรียบเทียบกับ Buy & Hold:
   - Buy & Hold Return: 42.3%
   - Rebalance Return: 45.5%
   - Winner: Rebalance (+3.2%)
```

---

### **Feature 2: Custom Portfolio Builder** 🎨
**ใช้ Tables:**
- `backtest_scenarios` (สร้าง custom portfolio)
- `scenario_holdings` (กำหนด weights เอง)

**ทำอะไรได้:**
- ผู้ใช้สร้าง Portfolio เองได้ (ไม่ต้องใช้ benchmark)
- กำหนดน้ำหนักของแต่ละ ETF เอง
- ทดสอบว่า Portfolio ที่สร้างจะได้ผลตอบแทนเท่าไหร่

**ตัวอย่าง:**
```
Custom Portfolio: "My Aggressive Tech Portfolio"
- 40% QQQ (Nasdaq 100)
- 30% SPY (S&P 500)
- 20% IWM (Small Cap)
- 10% VTI (Total Stock)

Backtest → ดูว่าได้ผลตอบแทนเท่าไหร่
```

---

### **Feature 3: Performance Tracking** 📈
**ใช้ Tables:**
- `portfolio_snapshots`
- `transaction_log`

**ทำอะไรได้:**
- ดูกราฟ Portfolio Value Over Time
- ดู Cumulative Return Chart
- ดู Drawdown Chart
- ดู Transaction History
- คำนวณ Transaction Costs

---

## 💡 **ทำไมต้องมี Tables เยอะ?**

### **แนวคิด Database Design:**

1. **Normalization**
   - แยก tables ตาม function ชัดเจน
   - ไม่ซ้ำซ้อน (No redundancy)
   - ง่ายต่อการ maintain

2. **Separation of Concerns**
   - `benchmark_portfolios` = Templates (ไม่เปลี่ยนแปลง)
   - `backtest_scenarios` = User-created tests (เปลี่ยนแปลงได้)
   - `backtest_results` = Results only (read-only)

3. **Scalability**
   - รองรับการพัฒนาต่อยอดในอนาคต
   - เพิ่ม feature ใหม่ได้ง่าย
   - ไม่ต้องแก้ schema มากเกินไป

4. **Data Integrity**
   - Foreign Keys รับรองความสัมพันธ์
   - Cascade Delete ลบข้อมูลที่เกี่ยวข้องอัตโนมัติ
   - Unique Keys ป้องกันข้อมูลซ้ำ

---

## 🎯 **สรุป**

### **ปัจจุบัน (Phase 1):**
- ใช้ 4 Tables: `etf_master`, `price_history`, `benchmark_portfolios`, `benchmark_holdings`
- Features: CRUD, Analytics (SQL-based), Portfolio Comparison
- **ตรงตามโจทย์อาจารย์ 100%** ✅

### **อนาคต (Phase 2):**
- ใช้ 5 Tables เพิ่ม: `backtest_scenarios`, `scenario_holdings`, `backtest_results`, `portfolio_snapshots`, `transaction_log`
- Features: Backtesting, Custom Portfolios, Performance Tracking
- **พัฒนาต่อได้ถ้ามีเวลา** 🔄

---

**Tables ที่ยังไม่ได้ใช้ = โครงสร้างพร้อมสำหรับการพัฒนาต่อ!** 🚀
