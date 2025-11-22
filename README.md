# ETF Portfolio Backtesting System

ระบบ Backtesting ที่สมบูรณ์สำหรับการทดสอบกลยุทธ์การลงทุนใน ETF (Exchange-Traded Funds) พร้อมฟีเจอร์ที่ครบครัน

## ✨ Features

- 📊 **การดึงข้อมูลอัตโนมัติ**: ดาวน์โหลดข้อมูลราคา ETF ผ่าน Yahoo Finance
- 💼 **Portfolio Management**: จัดการพอร์ตโฟลิโอและ allocation ได้อย่างยืดหยุ่น
- ⚖️ **Rebalancing**: รองรับการ rebalance แบบ daily, weekly, monthly, quarterly, yearly
- 📈 **Performance Metrics**: คำนวณ metrics มากกว่า 15 ตัว (Sharpe, Sortino, Max Drawdown, etc.)
- 📉 **Benchmark Comparison**: เปรียบเทียบผลตอบแทนกับ benchmark
- 🎨 **Rich Visualizations**: กราฟและแผนภูมิหลากหลายรูปแบบ
- 🔄 **Custom Strategies**: สร้างกลยุทธ์การลงทุนแบบ custom ได้
- 💰 **Transaction Costs**: คำนึงถึงค่าธรรมเนียมการซื้อขาย

## 📦 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd desktop-tutorial
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run examples

```bash
python main.py
```

## 🚀 Quick Start

### ตัวอย่างพื้นฐาน

```python
from etf_backtest import DataFetcher, Portfolio, Backtest, PerformanceMetrics, Visualizer
import matplotlib.pyplot as plt

# 1. ดึงข้อมูล ETF
fetcher = DataFetcher()
tickers = ['SPY', 'QQQ', 'IWM']
prices = fetcher.fetch_data(tickers, '2020-01-01', '2023-12-31')

# 2. สร้าง Portfolio
allocation = {
    'SPY': 0.40,  # 40% S&P 500
    'QQQ': 0.40,  # 40% NASDAQ
    'IWM': 0.20   # 20% Russell 2000
}

portfolio = Portfolio(
    initial_capital=100000,
    rebalance_frequency='monthly',
    transaction_cost=0.001
)
portfolio.set_allocation(allocation)

# 3. รัน Backtest
backtest = Backtest(portfolio, prices, benchmark='SPY')
results = backtest.run()

# 4. คำนวณ Performance Metrics
metrics = PerformanceMetrics(results['returns'], results['benchmark_returns'])
metrics.print_summary()

# 5. สร้างกราฟ
viz = Visualizer()
viz.plot_portfolio_value(results)
viz.plot_returns(results)
plt.show()
```

## 📖 Documentation

### Modules

#### 1. DataFetcher

จัดการการดึงและ cache ข้อมูลราคา ETF

```python
fetcher = DataFetcher(cache_dir='./data/cache')

# ดึงข้อมูล single ticker
prices = fetcher.fetch_data('SPY', '2020-01-01', '2023-12-31')

# ดึงข้อมูล multiple tickers
prices = fetcher.fetch_data(['SPY', 'QQQ', 'IWM'], '2020-01-01', '2023-12-31')

# ดูรายการ ETF ยอดนิยม
popular_etfs = DataFetcher.get_popular_etfs()
```

#### 2. Portfolio

จัดการ portfolio allocation และ rebalancing

```python
portfolio = Portfolio(
    initial_capital=100000,           # เงินทุนเริ่มต้น
    rebalance_frequency='quarterly',  # ความถี่ในการ rebalance
    transaction_cost=0.001            # ค่าธรรมเนียม 0.1%
)

# ตั้งค่า allocation
allocation = {
    'SPY': 0.60,
    'AGG': 0.30,
    'GLD': 0.10
}
portfolio.set_allocation(allocation)

# หรือใช้ equal weight
allocation = Portfolio.create_equal_weight(['SPY', 'QQQ', 'IWM'])
```

#### 3. Backtest

Engine สำหรับการทดสอบกลยุทธ์

```python
backtest = Backtest(
    portfolio=portfolio,
    data=prices,
    start_date='2020-01-01',  # Optional
    end_date='2023-12-31',    # Optional
    benchmark='SPY'           # Optional
)

results = backtest.run(verbose=True)

# ดึงผลลัพธ์
final_value = backtest.get_final_value()
total_return = backtest.get_total_return()
allocations = backtest.get_allocations_history()
```

#### 4. PerformanceMetrics

คำนวณ metrics ต่างๆ

```python
metrics = PerformanceMetrics(
    returns=results['returns'],
    benchmark_returns=results['benchmark_returns'],
    risk_free_rate=0.02
)

# คำนวณ individual metrics
sharpe = metrics.sharpe_ratio()
sortino = metrics.sortino_ratio()
max_dd = metrics.max_drawdown()
var = metrics.value_at_risk(0.95)

# ดูทุก metrics
all_metrics = metrics.get_all_metrics()
metrics.print_summary()
```

**Available Metrics:**
- Total Return
- Annualized Return
- Volatility (Standard Deviation)
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Calmar Ratio
- Value at Risk (VaR)
- Conditional VaR (CVaR)
- Win Rate
- Beta (vs benchmark)
- Alpha (Jensen's Alpha)
- Information Ratio

#### 5. Visualizer

สร้างกราฟและแผนภูมิ

```python
viz = Visualizer()

# กราฟมาตรฐาน
viz.plot_portfolio_value(results, benchmark=True)
viz.plot_returns(results, benchmark=True)
viz.plot_drawdown(results)
viz.plot_allocation(allocations)
viz.plot_rolling_metrics(results, window=252)
viz.plot_returns_distribution(results)
viz.plot_correlation_matrix(returns_data)

# Interactive dashboard (Plotly)
interactive_fig = viz.create_interactive_dashboard(results, allocations)
interactive_fig.write_html('dashboard.html')

# บันทึกกราฟ
viz.save_figure(fig, 'output.png', dpi=300)
```

## 📊 Examples

โปรเจกต์มี example files พร้อมใช้งาน:

### 1. Simple Backtest
```bash
python examples/simple_backtest.py
```

### 2. Advanced Momentum Strategy
```bash
python examples/advanced_strategy.py
```

### 3. Interactive Demo
```bash
python main.py
```

## 🎯 Use Cases

### 1. Equal-Weight Portfolio

```python
tickers = ['SPY', 'QQQ', 'IWM', 'EFA', 'AGG']
allocation = Portfolio.create_equal_weight(tickers)
```

### 2. 60/40 Portfolio (Stocks/Bonds)

```python
allocation = {
    'SPY': 0.60,  # 60% Stocks
    'AGG': 0.40   # 40% Bonds
}
```

### 3. All-Weather Portfolio

```python
allocation = {
    'SPY': 0.30,  # Stocks
    'TLT': 0.40,  # Long-term Bonds
    'IEF': 0.15,  # Intermediate Bonds
    'GLD': 0.075, # Gold
    'DBC': 0.075  # Commodities
}
```

### 4. Sector Rotation

```python
tickers = ['XLK', 'XLV', 'XLF', 'XLE', 'XLI']  # Sector ETFs
# ใช้ custom strategy function
```

### 5. Custom Strategy

```python
def my_strategy(historical_data, current_date):
    # Your strategy logic here
    # Return allocation dictionary
    return allocation

backtest = StrategyBacktest(
    portfolio,
    prices,
    strategy_func=my_strategy
)
```

## 🏗️ Project Structure

```
desktop-tutorial/
├── etf_backtest/           # Main package
│   ├── __init__.py
│   ├── data_fetcher.py     # Data fetching and caching
│   ├── portfolio.py        # Portfolio management
│   ├── backtest.py         # Backtesting engine
│   ├── metrics.py          # Performance metrics
│   └── visualize.py        # Visualization tools
├── examples/               # Example scripts
│   ├── simple_backtest.py
│   └── advanced_strategy.py
├── data/                   # Data cache directory
├── main.py                 # Interactive demo
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 📋 Popular ETFs

### US Equity
- **SPY**: S&P 500
- **QQQ**: NASDAQ 100
- **IWM**: Russell 2000
- **DIA**: Dow Jones
- **VTI**: Total US Market

### International
- **EFA**: Developed Markets
- **VEA**: Developed Markets ex-US
- **EEM**: Emerging Markets
- **VWO**: Emerging Markets

### Bonds
- **AGG**: US Aggregate Bonds
- **BND**: Total Bond Market
- **TLT**: 20+ Year Treasury
- **LQD**: Investment Grade Corporate
- **HYG**: High Yield Corporate

### Sectors
- **XLK**: Technology
- **XLV**: Healthcare
- **XLF**: Financial
- **XLE**: Energy
- **XLI**: Industrial

### Commodities & Real Estate
- **GLD**: Gold
- **SLV**: Silver
- **USO**: Oil
- **VNQ**: Real Estate

## 🔧 Advanced Features

### Custom Rebalancing Logic

```python
class MyPortfolio(Portfolio):
    def should_rebalance(self, current_date, last_rebalance):
        # Custom rebalancing logic
        return custom_condition
```

### Transaction Cost Analysis

```python
portfolio = Portfolio(
    initial_capital=100000,
    transaction_cost=0.001  # 0.1% per trade
)
```

### Risk-Free Rate Adjustment

```python
metrics = PerformanceMetrics(
    returns=results['returns'],
    risk_free_rate=0.03  # 3% annual
)
```

## 📈 Performance Tips

1. **Cache Data**: ข้อมูลจะถูก cache อัตโนมัติใน `./data/cache`
2. **Vectorization**: ใช้ pandas operations แทน loops
3. **Rebalance Frequency**: ความถี่มากเกินไปอาจเพิ่มค่าธรรมเนียม
4. **Date Range**: ทดสอบกับข้อมูลหลายปีเพื่อความน่าเชื่อถือ

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

**This software is for educational and research purposes only.**

- ผลการ backtest ในอดีตไม่ได้การันตีผลตอบแทนในอนาคต
- ไม่ควรใช้เป็นคำแนะนำการลงทุน
- ผู้ใช้ควรปรึกษาผู้เชี่ยวชาญทางการเงินก่อนตัดสินใจลงทุน
- ผู้พัฒนาไม่รับผิดชอบต่อความสูญเสียจากการใช้งานระบบนี้

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Happy Backtesting! 📊🚀**
