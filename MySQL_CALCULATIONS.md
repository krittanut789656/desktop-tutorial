# 🔍 การใช้ MySQL ในการคำนวณ - ETF Backtesting System

**สรุป: MySQL ใช้ในการคำนวณบางส่วน แต่ส่วนใหญ่คำนวณใน Python**

---

## 📊 สรุปรวม:

### ✅ MySQL ใช้สำหรับ:
1. **Storage** - เก็บข้อมูล (Primary role)
2. **Basic Aggregations** - COUNT, SUM, AVG, MIN, MAX
3. **Window Functions** - การคำนวณ Maximum Drawdown
4. **Data Retrieval** - SELECT queries

### ✅ Python ใช้สำหรับ:
1. **Complex Calculations** - Sharpe, Sortino, Calmar ratios
2. **Backtesting Logic** - Portfolio rebalancing, DCA
3. **Statistical Analysis** - Correlation, regression
4. **Visualizations** - Charts and graphs

---

## 🔬 รายละเอียดการคำนวณ:

### 1. **MySQL Window Functions** (คำนวณใน MySQL)

#### Maximum Drawdown Calculation:
```sql
-- analytics/analytics.py (บรรทัด 164-177)
WITH running_max AS (
    SELECT
        date,
        portfolio_value,
        MAX(portfolio_value) OVER (ORDER BY date) as peak_value  -- ⭐ Window Function
    FROM backtest_results
    WHERE backtest_id = ?
)
SELECT
    MIN((portfolio_value - peak_value) / peak_value) as max_drawdown
FROM running_max
```

**ทำไมใช้ MySQL:**
- ✅ Window functions (`OVER`) เหมาะสำหรับ running calculations
- ✅ Performance ดีกว่าการ loop ใน Python
- ✅ Code กระชับและอ่านง่าย

---

### 2. **MySQL Aggregations** (คำนวณใน MySQL)

#### Daily Statistics:
```sql
-- analytics/analytics.py (บรรทัด 184-192)
SELECT
    MIN(daily_return) as worst_day,      -- ⭐ Aggregation
    MAX(daily_return) as best_day,       -- ⭐ Aggregation
    AVG(daily_return) as avg_daily_return -- ⭐ Aggregation
FROM backtest_results
WHERE backtest_id = ? AND daily_return IS NOT NULL
```

**ทำไมใช้ MySQL:**
- ✅ Basic aggregations เร็วใน database
- ✅ ไม่ต้องโหลดข้อมูลทั้งหมดมา Python
- ✅ Efficient memory usage

---

#### Portfolio ETF Count:
```sql
-- main.py (บรรทัด 409)
SELECT
    p.portfolio_id,
    p.name,
    COUNT(pe.ticker) as etf_count  -- ⭐ Aggregation
FROM portfolios p
LEFT JOIN portfolio_etfs pe ON p.portfolio_id = pe.portfolio_id
GROUP BY p.portfolio_id
```

---

#### Price Records Count:
```sql
-- main.py (บรรทัด 682-683)
SELECT
    e.ticker,
    e.name,
    COUNT(dp.date) as price_records,  -- ⭐ Aggregation
    MAX(dp.date) as latest_date       -- ⭐ Aggregation
FROM etfs e
LEFT JOIN daily_prices dp ON e.ticker = dp.ticker
GROUP BY e.ticker
```

---

### 3. **Python Calculations** (คำนวณใน Python)

#### Sharpe Ratio:
```python
# analytics/analytics.py (บรรทัด 151-153)
risk_free_rate = 0.02
excess_return = cagr - risk_free_rate
sharpe_ratio = excess_return / annualized_volatility if annualized_volatility > 0 else 0
```

**ทำไมใช้ Python:**
- ✅ Formula ซับซ้อน - ต้องการ conditional logic
- ✅ ใช้ค่าจาก Python variables (cagr, annualized_volatility)

---

#### Sortino Ratio:
```python
# analytics/analytics.py (บรรทัด 156-161)
negative_returns = results_df[results_df['daily_return'] < 0]['daily_return']
if len(negative_returns) > 0:
    downside_std = np.std(negative_returns) * np.sqrt(252)
    sortino_ratio = excess_return / downside_std if downside_std > 0 else 0
else:
    sortino_ratio = float('inf')
```

**ทำไมใช้ Python:**
- ✅ ต้อง filter เฉพาะ negative returns
- ✅ ใช้ NumPy สำหรับ std calculation
- ✅ Complex conditional logic

---

#### Calmar Ratio:
```python
# analytics/analytics.py (บรรทัด 180-181)
calmar_ratio = cagr / max_drawdown if max_drawdown > 0 else 0
```

**ทำไมใช้ Python:**
- ✅ Simple calculation
- ✅ ใช้ค่าจาก Python และ MySQL รวมกัน (cagr จาก Python, max_drawdown จาก MySQL)

---

#### Alpha & Beta (vs Benchmark):
```python
# analytics/analytics.py
# Merge portfolio returns with benchmark returns
merged = pd.merge(portfolio_returns, benchmark_returns, on='date', how='inner')

# Calculate beta using covariance / variance
covariance = np.cov(merged['portfolio_return'], merged['benchmark_return'])[0][1]
benchmark_variance = np.var(merged['benchmark_return'])
beta = covariance / benchmark_variance if benchmark_variance > 0 else 0

# Calculate alpha
alpha = portfolio_cagr - (risk_free_rate + beta * (benchmark_cagr - risk_free_rate))
```

**ทำไมใช้ Python:**
- ✅ ต้องใช้ NumPy สำหรับ covariance และ variance
- ✅ Complex statistical calculations
- ✅ ต้อง merge data จาก 2 sources

---

### 4. **Backtesting Logic** (คำนวณใน Python)

#### Portfolio Rebalancing:
```python
# backtesting/backtesting_engine.py
def rebalance_portfolio(current_holdings, target_weights, current_prices):
    """Rebalance portfolio to target weights"""
    total_value = sum(shares * current_prices[ticker]
                     for ticker, shares in current_holdings.items())

    for ticker, target_weight in target_weights.items():
        target_value = total_value * target_weight
        target_shares = target_value / current_prices[ticker]
        current_shares = current_holdings.get(ticker, 0)

        if target_shares != current_shares:
            # Execute trade
            execute_trade(ticker, target_shares - current_shares, current_prices[ticker])
```

**ทำไมใช้ Python:**
- ✅ Complex business logic
- ✅ ต้องการ loops และ iterations
- ✅ Transaction handling

---

#### Dollar Cost Averaging (DCA):
```python
# backtesting/backtesting_engine.py
def execute_dca_strategy(portfolio_id, total_capital, months, start_date, end_date):
    """Execute DCA strategy - invest fixed amount each month"""
    monthly_investment = total_capital / months
    investment_dates = generate_monthly_dates(start_date, end_date, months)

    for date in investment_dates:
        prices = get_prices_on_date(date)
        for ticker, weight in portfolio_weights.items():
            investment_amount = monthly_investment * weight
            shares_to_buy = investment_amount / prices[ticker]
            buy_shares(ticker, shares_to_buy, prices[ticker], date)
```

**ทำไมใช้ Python:**
- ✅ Time-based logic (monthly investments)
- ✅ Complex iteration over dates
- ✅ Multiple database writes

---

## 📊 สรุปการแบ่งหน้าที่:

### MySQL (Database Layer):

| Operation | Example | Location |
|-----------|---------|----------|
| **Window Functions** | MAX() OVER (ORDER BY) | Maximum Drawdown |
| **Aggregations** | COUNT(), AVG(), MIN(), MAX() | Statistics |
| **JOINs** | Portfolio + ETFs | Data retrieval |
| **Filtering** | WHERE clauses | Data selection |
| **Sorting** | ORDER BY | Data ordering |

**ประมาณ: 20% ของการคำนวณ**

---

### Python (Application Layer):

| Operation | Example | Location |
|-----------|---------|----------|
| **Complex Math** | Sharpe, Sortino, Calmar | Analytics |
| **Statistical Analysis** | Correlation, Regression | Analytics |
| **Business Logic** | Rebalancing, DCA | Backtesting |
| **Data Processing** | Pandas operations | All modules |
| **Visualizations** | Charts, Graphs | Visualizations |

**ประมาณ: 80% ของการคำนวณ**

---

## 🎯 ตัวอย่างการทำงานร่วมกัน:

### Example: Risk-Adjusted Performance Analysis

#### Step 1: MySQL ดึงข้อมูล
```sql
SELECT date, portfolio_value, daily_return
FROM backtest_results
WHERE backtest_id = ?
ORDER BY date
```

#### Step 2: Python คำนวณ Volatility
```python
returns = results_df['daily_return']
daily_std = np.std(returns)
annualized_volatility = daily_std * np.sqrt(252)
```

#### Step 3: Python คำนวณ CAGR
```python
days = (end_date - start_date).days
years = days / 365.25
cagr = (final_value / initial_value) ** (1 / years) - 1
```

#### Step 4: MySQL คำนวณ Max Drawdown
```sql
WITH running_max AS (
    SELECT portfolio_value,
           MAX(portfolio_value) OVER (ORDER BY date) as peak_value
    FROM backtest_results
    WHERE backtest_id = ?
)
SELECT MIN((portfolio_value - peak_value) / peak_value) as max_drawdown
FROM running_max
```

#### Step 5: Python คำนวณ Metrics
```python
sharpe_ratio = (cagr - 0.02) / annualized_volatility
sortino_ratio = (cagr - 0.02) / downside_deviation
calmar_ratio = cagr / max_drawdown
```

---

## 💡 ทำไมไม่คำนวณทั้งหมดใน MySQL?

### ข้อจำกัดของ MySQL:

1. **Complex Statistical Functions:**
   - ไม่มี built-in functions สำหรับ Sharpe, Sortino
   - NumPy/SciPy มี functions ที่สมบูรณ์กว่า

2. **Business Logic:**
   - Backtesting ต้องการ complex state management
   - Python เหมาะกับ procedural logic มากกว่า

3. **Data Transformation:**
   - Pandas ทำ data manipulation ได้ง่ายกว่า
   - Python มี libraries เยอะสำหรับ analysis

4. **Visualization:**
   - MySQL ไม่สามารถสร้าง charts ได้
   - Python มี matplotlib, seaborn

5. **Flexibility:**
   - Python code แก้ไขง่ายกว่า complex SQL
   - Testing และ debugging ง่ายกว่า

---

## ✅ ข้อดีของแนวทางนี้:

### 1. **Best of Both Worlds:**
- MySQL: Fast data retrieval, aggregations, window functions
- Python: Complex calculations, business logic, visualizations

### 2. **Performance:**
- MySQL ทำ heavy lifting สำหรับ data operations
- Python ทำ complex calculations บน processed data
- ลดการโหลดข้อมูลไม่จำเป็น

### 3. **Maintainability:**
- Business logic อยู่ใน Python (อ่านง่าย)
- Database ทำหน้าที่ storage และ basic operations
- แยกส่วนชัดเจน

### 4. **Scalability:**
- MySQL query optimization
- Python parallel processing (ถ้าต้องการ)
- ขยายได้ทั้ง 2 ฝั่ง

---

## 📋 สรุป:

### คำตอบคำถาม: "ได้ใช้ MySQL ในการคำนวณใช่หรือไม่?"

**คำตอบ:** ✅ **ใช่ แต่บางส่วน**

### การแบ่งหน้าที่:

**MySQL (20%):**
- ✅ Window Functions (MAX OVER) → Maximum Drawdown
- ✅ Aggregations (COUNT, AVG, MIN, MAX) → Basic statistics
- ✅ JOINs → Data retrieval
- ✅ Filtering & Sorting → Data selection

**Python (80%):**
- ✅ Sharpe, Sortino, Calmar ratios
- ✅ Alpha & Beta calculations
- ✅ Backtesting logic (rebalancing, DCA)
- ✅ Statistical analysis
- ✅ Visualizations

### แนวทางนี้:
- ✅ **Hybrid Approach** - ใช้จุดแข็งของทั้ง MySQL และ Python
- ✅ **Optimal Performance** - คำนวณในที่ที่เหมาะสมที่สุด
- ✅ **Maintainable** - Code อ่านง่าย แก้ไขง่าย
- ✅ **Scalable** - ขยายได้ทั้ง 2 ฝั่ง

---

**สรุปสุดท้าย:**
ระบบใช้ **MySQL สำหรับการคำนวณที่เหมาะสม** (window functions, aggregations)
และ **Python สำหรับการคำนวณที่ซับซ้อน** (statistical analysis, business logic)

**นี่คือ best practice ในการพัฒนา data analytics system!** ✅
