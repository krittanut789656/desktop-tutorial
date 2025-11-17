# ETF Portfolio Analytics Module

Advanced analytics and insights module for ETF portfolio backtesting system. This module provides **3 comprehensive analytics insights** using SQL-optimized queries and professional visualizations.

---

## 📊 Overview

The Analytics Module provides actionable insights for portfolio optimization and investment strategy selection:

1. **Risk-Adjusted Performance Analysis** - Evaluate portfolios using Sharpe, Sortino, and Calmar ratios
2. **Optimal Rebalancing Frequency Analysis** - Determine the best rebalancing strategy with cost-benefit analysis
3. **DCA vs Lump Sum Market Timing Analysis** - Compare investment strategies across market conditions

---

## 🎯 Key Features

- **SQL-Optimized Queries** - Fast performance using MySQL window functions and aggregations
- **Actionable Recommendations** - Not just statistics, but concrete next steps
- **Professional Visualizations** - Publication-ready charts with matplotlib/seaborn
- **Comprehensive Reports** - Detailed text reports with all findings
- **Benchmark Comparison** - Compare portfolios against SPY or custom benchmarks
- **Market Condition Analysis** - Bull/bear/neutral market detection using SMAs
- **Type Hints & Docstrings** - Well-documented, maintainable code
- **Comprehensive Logging** - Track all operations and debug issues

---

## 📁 Module Structure

```
analytics/
├── analytics.py              # Main analytics module (1355+ lines)
│   ├── Insight 1: Risk-Adjusted Performance
│   ├── Insight 2: Optimal Rebalancing Frequency
│   └── Insight 3: DCA vs Lump Sum
├── visualizations.py         # Visualization utilities (650+ lines)
│   ├── Risk-Return Scatter Plot
│   ├── Drawdown Charts
│   ├── Rebalancing Comparison Charts
│   └── DCA vs Lump Sum Charts
├── example_analytics.py      # Comprehensive examples
├── requirements.txt          # Python dependencies
├── .gitignore               # Ignored files (logs, outputs)
└── README.md                # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL 8.0+ database with ETF backtesting data
- Completed database setup (Phase 1)
- ETF price data loaded (Phase 2)

### Install Dependencies

```bash
cd analytics
pip install -r requirements.txt
```

**Required packages:**
- `mysql-connector-python>=8.2.0` - Database connectivity
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `matplotlib>=3.7.0` - Plotting
- `seaborn>=0.12.0` - Statistical visualizations

---

## 📖 Analytics Insights

### Insight 1: Risk-Adjusted Performance Analysis

**Purpose:** Evaluate portfolio performance using multiple risk-adjusted metrics and compare with benchmarks.

**Metrics Calculated:**
- **Sharpe Ratio** - Return per unit of total risk
- **Sortino Ratio** - Return per unit of downside risk
- **Calmar Ratio** - Return per unit of maximum drawdown
- **Maximum Drawdown** - Largest peak-to-trough decline
- **Alpha & Beta** - Excess return and systematic risk vs benchmark

**Key Functions:**

```python
# Calculate risk-adjusted metrics for a portfolio
result = analytics.calculate_risk_adjusted_metrics(
    portfolio_id=1,
    start_date='2020-01-01',
    end_date='2024-12-31',
    db_config=DB_CONFIG
)

# Compare with benchmark (SPY)
benchmark_result = analytics.compare_with_benchmark(
    portfolio_id=1,
    start_date='2020-01-01',
    end_date='2024-12-31',
    benchmark_symbol='SPY',
    db_config=DB_CONFIG
)

# Generate comprehensive report for multiple portfolios
analytics.generate_risk_adjusted_report(
    portfolio_ids=[1, 2, 3],
    start_date='2020-01-01',
    end_date='2024-12-31',
    benchmark_symbol='SPY',
    output_file='insight1_report.txt',
    db_config=DB_CONFIG
)
```

**Visualizations:**
- Risk-Return Scatter Plot (all portfolios)
- Drawdown Chart (comparison with SPY)

**Output Files:**
- `insight1_risk_adjusted_report.txt` - Detailed analysis report
- `insight1_risk_return_scatter.png` - Risk-return visualization
- `insight1_drawdown_comparison.png` - Drawdown charts

**Use Cases:**
- Select the best portfolio based on risk-adjusted returns
- Identify portfolios with superior downside protection
- Compare your portfolio against market benchmarks
- Evaluate recovery patterns during market crashes

---

### Insight 2: Optimal Rebalancing Frequency Analysis

**Purpose:** Determine the optimal rebalancing frequency by comparing 5 strategies with cost-benefit analysis.

**Strategies Tested:**
1. **Buy & Hold** - No rebalancing (baseline)
2. **Monthly Rebalancing** - Rebalance every month
3. **Quarterly Rebalancing** - Rebalance every 3 months
4. **Semi-Annual Rebalancing** - Rebalance every 6 months
5. **Annual Rebalancing** - Rebalance once per year

**Analysis Performed:**
- Performance comparison (return, volatility, Sharpe ratio)
- Transaction cost analysis
- Cost-benefit calculation
- Net return after costs
- Actionable recommendation

**Key Function:**

```python
# Automatically runs 5 backtests and compares results
result = analytics.compare_rebalancing_strategies(
    portfolio_id=1,
    start_date='2020-01-01',
    end_date='2024-12-31',
    initial_capital=100000.0,
    output_file='insight2_rebalancing_analysis.txt',
    db_config=DB_CONFIG
)

# Access results
best_strategy = result['best_strategy']
best_return = result['best_return']
best_sharpe = result['best_sharpe']
recommendation = result['recommendation']
```

**Visualizations:**
- Bar Chart: Return vs Rebalancing Frequency
- Bar Chart: Transaction Costs Analysis
- Line Chart: Portfolio Value Over Time (5 strategies)

**Output Files:**
- `insight2_rebalancing_analysis.txt` - Cost-benefit analysis report
- `insight2_rebalancing_comparison.png` - Performance comparison charts
- `insight2_portfolio_value.png` - Portfolio value evolution

**Recommendations Include:**
- Optimal rebalancing frequency
- Expected cost impact
- When to use Buy & Hold vs Active rebalancing
- Trade-off between performance gain and transaction costs

**Use Cases:**
- Optimize your rebalancing schedule
- Minimize transaction costs
- Balance performance improvement vs trading costs
- Choose strategy based on your portfolio size

---

### Insight 3: DCA vs Lump Sum Market Timing Analysis

**Purpose:** Compare Dollar Cost Averaging (DCA) vs Lump Sum investment strategies across different market conditions.

**Strategies Compared:**

**Scenario A: Lump Sum**
- Invest 100% of capital on Day 1
- Full market exposure immediately
- Higher potential returns in bull markets
- Higher risk if market drops after entry

**Scenario B: Dollar Cost Averaging (DCA)**
- Invest evenly over N months (e.g., 12 months)
- Gradual market entry
- Lower average entry price in volatile markets
- Psychological comfort, reduced timing risk

**Analysis Performed:**
- Win rate calculation (% of days DCA outperforms)
- Market condition detection (bull/bear/neutral using SMAs)
- Performance by market condition
- Psychological and behavioral insights
- Hybrid strategy recommendations

**Key Function:**

```python
# Compare DCA vs Lump Sum
result = analytics.compare_dca_vs_lumpsum(
    portfolio_id=1,
    total_capital=100000.0,
    investment_period_months=12,  # DCA over 12 months
    start_date='2020-01-01',
    end_date='2024-12-31',
    output_file='insight3_dca_vs_lumpsum.txt',
    db_config=DB_CONFIG
)

# Access results
winner = result['winner']
ls_return = result['lumpsum_annualized_return']
dca_return = result['dca_annualized_return']
dca_win_rate = result['dca_win_rate']
market_conditions = result['market_conditions']
```

**Market Condition Detection:**
- **Bull Market** - SPY 50-day SMA > 200-day SMA
- **Bear Market** - SPY 50-day SMA < 200-day SMA
- **Neutral Market** - Transition periods or sideways

**Visualizations:**
- Line Chart: Portfolio Value Comparison (DCA vs Lump Sum)
- Scatter Plot: Entry Points Visualization
- Bar Chart: Win Rate by Market Condition

**Output Files:**
- `insight3_dca_vs_lumpsum.txt` - Comprehensive comparison report
- `insight3_comparison_chart.png` - Portfolio value comparison
- `insight3_win_rate_by_condition.png` - Market condition analysis

**Recommendations Include:**
- Best strategy based on market conditions
- Hybrid approach (e.g., invest 50-70% immediately, DCA the rest)
- Psychological considerations
- When to use each strategy

**Use Cases:**
- Decide how to invest a lump sum (bonus, inheritance, etc.)
- Understand market timing impact
- Choose strategy based on risk tolerance
- Optimize entry strategy for volatile markets

---

## 💻 Usage Examples

### Quick Start

```python
import analytics

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'etf_backtesting'
}

# Insight 1: Risk-Adjusted Analysis
analytics.generate_risk_adjusted_report(
    portfolio_ids=[1, 2, 3],
    start_date='2020-01-01',
    end_date='2024-12-31',
    benchmark_symbol='SPY',
    output_file='risk_analysis.txt',
    db_config=DB_CONFIG
)

# Insight 2: Optimal Rebalancing
result = analytics.compare_rebalancing_strategies(
    portfolio_id=1,
    start_date='2020-01-01',
    end_date='2024-12-31',
    initial_capital=100000.0,
    output_file='rebalancing_analysis.txt',
    db_config=DB_CONFIG
)

# Insight 3: DCA vs Lump Sum
result = analytics.compare_dca_vs_lumpsum(
    portfolio_id=1,
    total_capital=100000.0,
    investment_period_months=12,
    start_date='2020-01-01',
    end_date='2024-12-31',
    output_file='dca_vs_lumpsum.txt',
    db_config=DB_CONFIG
)
```

### Run All Examples

```bash
# Interactive menu with all examples
python example_analytics.py

# Select from:
# 1. Risk-Adjusted Performance Analysis
# 2. Optimal Rebalancing Frequency Analysis
# 3. DCA vs Lump Sum Market Timing Analysis
# 4. Run All Insights (Comprehensive)
# 5. Custom Analysis Example
```

### Custom Analysis Workflow

```python
# Example: Find best portfolio, then optimize its rebalancing
import analytics

# Step 1: Evaluate all portfolios
portfolio_ids = [1, 2, 3, 4, 5]
best_sharpe = -999
best_portfolio = None

for pid in portfolio_ids:
    result = analytics.calculate_risk_adjusted_metrics(
        portfolio_id=pid,
        start_date='2020-01-01',
        end_date='2024-12-31',
        db_config=DB_CONFIG
    )

    if result['success'] and result['sharpe_ratio'] > best_sharpe:
        best_sharpe = result['sharpe_ratio']
        best_portfolio = pid

# Step 2: Optimize rebalancing for best portfolio
analytics.compare_rebalancing_strategies(
    portfolio_id=best_portfolio,
    start_date='2020-01-01',
    end_date='2024-12-31',
    initial_capital=100000.0,
    output_file=f'optimal_strategy_portfolio_{best_portfolio}.txt',
    db_config=DB_CONFIG
)

# Step 3: Test DCA vs Lump Sum for best portfolio
analytics.compare_dca_vs_lumpsum(
    portfolio_id=best_portfolio,
    total_capital=100000.0,
    investment_period_months=6,
    start_date='2020-01-01',
    end_date='2024-12-31',
    output_file=f'entry_strategy_portfolio_{best_portfolio}.txt',
    db_config=DB_CONFIG
)
```

---

## 📊 Visualization Examples

### Create Risk-Return Scatter Plot

```python
import visualizations

portfolio_data = [
    {'name': 'Portfolio 1', 'return': 12.5, 'volatility': 15.2, 'sharpe': 0.82},
    {'name': 'Portfolio 2', 'return': 10.1, 'volatility': 12.3, 'sharpe': 0.82},
    {'name': 'Portfolio 3', 'return': 14.2, 'volatility': 18.1, 'sharpe': 0.78}
]

benchmark_data = {
    'name': 'SPY',
    'return': 11.2,
    'volatility': 14.1,
    'sharpe': 0.79
}

visualizations.plot_risk_return_scatter(
    portfolio_data=portfolio_data,
    benchmark_data=benchmark_data,
    output_file='risk_return_plot.png',
    dpi=300
)
```

### Create Rebalancing Comparison Chart

```python
strategy_data = [
    {'strategy': 'Buy & Hold', 'return': 10.5, 'volatility': 15.2,
     'sharpe': 0.69, 'total_costs': 0},
    {'strategy': 'Quarterly', 'return': 11.2, 'volatility': 14.8,
     'sharpe': 0.76, 'total_costs': 450}
]

visualizations.plot_rebalancing_frequency_comparison(
    strategy_data=strategy_data,
    output_file='rebalancing_comparison.png'
)
```

---

## 🔧 Configuration

### Database Configuration

```python
DB_CONFIG = {
    'host': 'localhost',      # MySQL server host
    'user': 'root',           # Database user
    'password': 'password',   # Database password
    'database': 'etf_backtesting'  # Database name
}
```

### Analysis Parameters

```python
# Date range for analysis
START_DATE = '2020-01-01'
END_DATE = '2024-12-31'

# Initial capital
INITIAL_CAPITAL = 100000.0

# Transaction costs (for backtesting)
TRANSACTION_COST_PCT = 0.001  # 0.1% per trade

# DCA parameters
DCA_INVESTMENT_PERIOD = 12  # months

# Benchmark
BENCHMARK_SYMBOL = 'SPY'
```

---

## 📈 Output Files

All analytics functions generate comprehensive text reports and visualizations:

### Text Reports
- `insight1_risk_adjusted_report.txt` - Risk-adjusted metrics analysis
- `insight2_rebalancing_analysis.txt` - Rebalancing frequency comparison
- `insight3_dca_vs_lumpsum.txt` - DCA vs Lump Sum analysis
- `analytics.log` - Execution logs

### Visualizations
- `insight1_risk_return_scatter.png` - Risk-return scatter plot
- `insight1_drawdown_comparison.png` - Drawdown charts
- `insight2_rebalancing_comparison.png` - Rebalancing performance
- `insight2_portfolio_value.png` - Portfolio value evolution
- `insight3_comparison_chart.png` - DCA vs Lump Sum comparison
- `insight3_win_rate_by_condition.png` - Win rate by market condition

### Logs
- `analytics.log` - Main analytics module log
- `analytics_example.log` - Example script log

**Note:** Output files (*.txt, *.png, *.pdf, *.log) are automatically ignored by Git (see `.gitignore`)

---

## 🎨 Visualization Customization

All visualization functions support customization:

```python
# High-resolution output (publication quality)
visualizations.plot_risk_return_scatter(
    portfolio_data=data,
    output_file='chart.png',
    dpi=600  # High resolution
)

# Save in multiple formats
visualizations.save_chart_multiple_formats(
    fig=my_figure,
    base_filename='analysis',
    formats=['png', 'pdf', 'svg'],
    dpi=300
)

# Create comprehensive dashboard
visualizations.create_summary_dashboard(
    risk_return_file='insight1_risk_return_scatter.png',
    drawdown_file='insight1_drawdown_comparison.png',
    rebalancing_file='insight2_rebalancing_comparison.png',
    dca_comparison_file='insight3_comparison_chart.png',
    output_file='analytics_dashboard.png',
    dpi=200
)
```

---

## 🧪 Testing

Test the analytics module with sample data:

```python
# Test Insight 1
python -c "import analytics; print(analytics.calculate_risk_adjusted_metrics(1, '2020-01-01', '2024-12-31', {'host': 'localhost', 'user': 'root', 'password': 'password', 'database': 'etf_backtesting'}))"

# Run example script
python example_analytics.py
```

---

## 📚 API Reference

### Main Functions

#### `calculate_risk_adjusted_metrics()`
```python
def calculate_risk_adjusted_metrics(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    db_config: Dict,
    risk_free_rate: float = 0.02
) -> Dict:
    """Calculate Sharpe, Sortino, Calmar ratios and max drawdown"""
```

#### `compare_with_benchmark()`
```python
def compare_with_benchmark(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    benchmark_symbol: str,
    db_config: Dict,
    risk_free_rate: float = 0.02
) -> Dict:
    """Calculate Alpha and Beta vs benchmark"""
```

#### `compare_rebalancing_strategies()`
```python
def compare_rebalancing_strategies(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    initial_capital: float,
    output_file: str,
    db_config: Dict
) -> Dict:
    """Compare 5 rebalancing strategies with cost-benefit analysis"""
```

#### `compare_dca_vs_lumpsum()`
```python
def compare_dca_vs_lumpsum(
    portfolio_id: int,
    total_capital: float,
    investment_period_months: int,
    start_date: str,
    end_date: str,
    output_file: str,
    db_config: Dict
) -> Dict:
    """Compare DCA vs Lump Sum across market conditions"""
```

See function docstrings for detailed parameter descriptions and return values.

---

## 🔍 Troubleshooting

### Common Issues

**Issue:** `mysql.connector.errors.ProgrammingError: 1146 (42S02): Table 'etf_backtesting.etf_prices' doesn't exist`
- **Solution:** Run database setup scripts from Phase 1 and data collection from Phase 2

**Issue:** `No data returned for portfolio_id X`
- **Solution:** Check that portfolio exists and has backtests in the database

**Issue:** `ImportError: No module named 'mysql.connector'`
- **Solution:** `pip install mysql-connector-python`

**Issue:** Charts not displaying properly
- **Solution:** Ensure matplotlib backend is configured. Try: `export MPLBACKEND=Agg`

**Issue:** Low Sharpe ratios (< 0.5)
- **Explanation:** This is normal for volatile portfolios or bear market periods

---

## 💡 Best Practices

1. **Always analyze multiple time periods** - Results vary significantly across bull/bear markets
2. **Use appropriate benchmarks** - Compare international portfolios with ACWI, not SPY
3. **Consider transaction costs** - They significantly impact rebalancing analysis
4. **Review qualitative insights** - Don't just rely on numbers, read the recommendations
5. **Test multiple DCA periods** - Try 6, 12, 18, 24 months for different scenarios
6. **Back-test recent periods** - More relevant than ancient history for current markets
7. **Use risk-adjusted metrics** - Raw returns don't tell the full story
8. **Check data quality** - Ensure price data is complete (no large gaps)

---

## 🛠️ Advanced Usage

### Batch Analysis

```python
# Analyze all portfolios in the database
import mysql.connector

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("SELECT portfolio_id FROM portfolios")
portfolio_ids = [row[0] for row in cursor.fetchall()]

for pid in portfolio_ids:
    analytics.generate_risk_adjusted_report(
        portfolio_ids=[pid],
        start_date='2020-01-01',
        end_date='2024-12-31',
        output_file=f'report_portfolio_{pid}.txt',
        db_config=DB_CONFIG
    )
```

### Custom Risk-Free Rate

```python
# Use 10-year Treasury rate instead of default 2%
result = analytics.calculate_risk_adjusted_metrics(
    portfolio_id=1,
    start_date='2020-01-01',
    end_date='2024-12-31',
    risk_free_rate=0.045,  # 4.5%
    db_config=DB_CONFIG
)
```

---

## 📖 Related Modules

- **Phase 1: Database Schema** - `database/` - MySQL table definitions
- **Phase 2: Data Collection** - `data_collection/` - ETF price fetching with yfinance
- **Phase 3: CRUD Operations** - `crud_operations/` - Portfolio and ETF management
- **Phase 4: Backtesting Engine** - `backtesting/` - Strategy backtesting

---

## 📝 License

Part of the ETF Portfolio Backtesting System - Educational/Personal Use

---

## 👨‍💻 Author

**ETF Portfolio Backtesting System**
Phase 5: Data Analytics Module

---

## 🎓 Learning Resources

- **Sharpe Ratio**: [Investopedia - Sharpe Ratio](https://www.investopedia.com/terms/s/sharperatio.asp)
- **Maximum Drawdown**: [Investopedia - Maximum Drawdown](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)
- **DCA vs Lump Sum**: [Vanguard Research - DCA Study](https://investor.vanguard.com/investor-resources-education/online-trading/dollar-cost-averaging-vs-lump-sum)
- **Portfolio Rebalancing**: [Morningstar - Rebalancing Strategies](https://www.morningstar.com/articles)

---

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review log files in `analytics.log`
3. Ensure database has required data
4. Verify all dependencies are installed

---

**Happy Analyzing! 📊🚀**
