# 📊 ETF Portfolio Backtester

A comprehensive Python-based backtesting system for ETF portfolio strategies using momentum-based selection and rebalancing.

## 🎯 Features

### Core Functionality
- ✅ **Momentum-Based ETF Selection** - Identify top-performing ETFs based on historical momentum
- ✅ **Automated Backtesting** - Run backtests with customizable parameters
- ✅ **Portfolio Analytics** - Comprehensive performance metrics and risk analysis
- ✅ **Data Visualization** - Interactive charts and graphs
- ✅ **MySQL Integration** - Robust database backend with connection pooling

### NEW! ⭐ Menu 3.4 - Update ETF Information
- ✅ **Live ETF Data Editing** - Update ETF information directly through the interface
- ✅ **Interactive Updates** - User-friendly prompts for selecting and modifying ETF data
- ✅ **Field Validation** - Ensures data integrity with built-in validation
- ✅ **Instant Database Sync** - Changes are immediately persisted to MySQL
- ✅ **Confirmation Steps** - Prevents accidental modifications
- ✅ **Audit Trail** - Automatic timestamp tracking for all updates

## 📋 Menu Structure

```
[1] 🎯 Run Backtest
  1.1 - Standard Backtest (6 months, 90-day lookback)
  1.2 - Custom Backtest (specify your parameters)
  1.3 - Comparative Backtest (90-day vs 180-day)

[2] 📊 Analytics & Insights
  2.1 - Generate All Insights
  2.2 - Volatility Analysis by Asset Type
  2.3 - Lookback Period Optimization
  2.4 - Drawdown Analysis

[3] 🔍 CRUD Operations
  3.1 - View Latest Backtest Results
  3.2 - View All Backtest Runs
  3.3 - View ETF Information
  3.4 - Update ETF Information (LIVE EDIT) ⭐ NEW!

[4] 📈 Data Visualization
  4.1 - Plot Cumulative Returns
  4.2 - Plot Volatility Comparison
  4.3 - Plot Asset Allocation

[5] 🔧 Data Management
  5.1 - Load Sample Data
  5.2 - Reset Database

[0] 🚪 Exit System
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd desktop-tutorial
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   mysql -u root -p < database_schema.sql
   ```

4. **Configure database connection**
   Edit `etf_backtester_integrated.py` (line ~445):
   ```python
   success = system.initialize_system(
       host='127.0.0.1',
       port=3306,
       user='root',
       password='YOUR_PASSWORD_HERE',  # ← Update this!
       database='etf_backtester_db'
   )
   ```

5. **Run the system**

   **Option A: Python Script**
   ```bash
   python etf_backtester_integrated.py
   ```

   **Option B: Jupyter Notebook - Multi-Cell** (Recommended for learning)
   ```bash
   jupyter notebook ETF_Backtester_Integrated.ipynb
   ```
   Then run all cells in sequence.

   **Option C: Jupyter Notebook - One-Cell** ⭐ (Easiest - กด Shift+Enter ครั้งเดียว!)
   ```bash
   jupyter notebook ETF_Backtester_OneCell.ipynb
   ```
   แก้ไข password แล้วกด Shift+Enter ครั้งเดียว ระบบจะ loop ไปเรื่อยๆ!

6. **Load sample data**
   - Select menu option `5.1`
   - Confirm with `yes`

## 📓 Using Jupyter Notebook (Recommended)

The Jupyter Notebook version (`ETF_Backtester_Integrated.ipynb`) provides an enhanced interactive experience with:

- ✅ **Better Visualization** - Charts and graphs display inline
- ✅ **Cell-by-Cell Execution** - Run code step by step
- ✅ **Rich Documentation** - Markdown cells with instructions
- ✅ **Easy Restart** - Restart kernel to reset system
- ✅ **Output History** - Keep track of all operations

### How to Use:

1. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook ETF_Backtester_Integrated.ipynb
   ```

2. **Run All Cells**
   - Click: `Cell → Run All`
   - Or press `Shift + Enter` on each cell

3. **Update Database Password**
   - Find the cell with `system.initialize_system()`
   - Update the `password` parameter
   - Re-run that cell

4. **Start Using the Menu**
   - The last cell contains the interactive menu loop
   - Enter menu options like `3.4` for UPDATE feature

### Notebook Structure:
- **Cell 1**: Imports and configuration
- **Cell 2**: Main controller class definition
- **Cell 3**: System initialization
- **Cell 4**: Interactive menu loop

## 📁 Project Structure

```
desktop-tutorial/
├── modules/
│   ├── __init__.py
│   ├── db_connector.py              # Database connection pooling
│   ├── backtest_engine.py           # Momentum backtesting logic
│   ├── analytics.py                 # Portfolio analytics
│   ├── crud_operations.py           # CRUD operations (includes UPDATE feature)
│   └── data_loader.py               # Data loading utilities
├── ETF_Backtester_OneCell.ipynb     # One-Cell Notebook ⭐ NEW! (แนะนำ)
├── ETF_Backtester_Integrated.ipynb  # Multi-Cell Notebook
├── etf_backtester_integrated.py     # Python script version
├── database_schema.sql              # MySQL database schema
├── requirements.txt                 # Python dependencies
├── INSTALLATION.md                  # Installation guide
├── README_UPDATE_FEATURE.md         # Documentation for menu 3.4
├── JUPYTER_NOTEBOOK_GUIDE.md        # Jupyter Notebook guide
└── README.md                        # This file
```

## 💻 Usage Examples

### Running a Standard Backtest

```
👉 Enter your choice: 1.1

Configuration:
  📅 Date Range: 2024-05-26 to 2024-11-26
  📊 Lookback: 90 days | Portfolio: Top 5 ETFs | Rebalance: 30 days

✓ Backtest complete!
  Run ID: abc12345
  Rebalance dates: 6
  Total selections: 30
```

### Updating ETF Information (Menu 3.4)

```
👉 Enter your choice: 3.4

📋 Current ETF Information:
[Displays all ETFs]

👉 Enter ETF_ID to update: 1

📌 Selected ETF:
   ETF_ID: 1
   Ticker: SPY
   Name: SPDR S&P 500 ETF Trust
   Asset Type: Equity

📝 Which field do you want to update?
   1 - Ticker Symbol
   2 - ETF Name
   3 - Asset Type

👉 Enter choice (1-3): 3

Current value: Equity
👉 Enter new value for Asset_Type: Index Fund

⚠️  CONFIRMATION
   ETF ID: 1
   Field: Asset_Type
   Old Value: Equity
   New Value: Index Fund

👉 Proceed with update? (yes/no): yes

✅ Successfully updated!
   ETF_ID: 1
   Field: Asset_Type
   New Value: Index Fund
```

### Viewing Analytics

```
👉 Enter your choice: 2.1

Generating all analytics insights...
- Volatility analysis
- Drawdown analysis
- Lookback period comparison
✓ Complete!
```

## 🗄️ Database Schema

### ETF_Master
- Primary ETF reference data
- Tracks ticker symbols, names, and asset types
- Includes automatic timestamp tracking

### Price_Data
- Daily OHLCV price data
- Calculated daily returns
- Indexed for fast queries

### Strategy_Log
- Backtest results and selections
- Portfolio rankings and momentum scores
- Performance metrics

## 📊 Sample ETFs Included

- **Equity**: SPY, QQQ, VTI, IWM, EFA
- **Fixed Income**: AGG, TLT, SHY
- **Commodity**: GLD, DBC

## 🔧 Configuration

### Backtest Parameters
- `lookback_days`: Momentum calculation period (default: 90)
- `holding_period_days`: Days to hold positions (default: 30)
- `rebalance_days`: Days between rebalances (default: 30)
- `top_n`: Number of ETFs to select (default: 5)

### Database Configuration
- Host: 127.0.0.1
- Port: 3306
- Database: etf_backtester_db
- Connection pool size: 5

## 📈 Performance Metrics

The system calculates:
- Cumulative Returns
- CAGR (Compound Annual Growth Rate)
- Average Return per Period
- Volatility (Daily, Weekly, Annual)
- Maximum Drawdown
- Sharpe Ratio
- Portfolio Rankings

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black modules/ *.py
flake8 modules/ *.py
```

## 📚 Documentation

- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [Update Feature Documentation](README_UPDATE_FEATURE.md) - Menu 3.4 guide
- [Database Schema](database_schema.sql) - SQL table definitions

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the [Installation Guide](INSTALLATION.md)
2. Review the troubleshooting section
3. Create an issue in the repository

## 🔄 Version History

### Version 1.0 (Current)
- ✅ Complete backtesting system
- ✅ MySQL integration
- ✅ Portfolio analytics
- ✅ Data visualization
- ✅ **NEW**: Menu 3.4 - Update ETF Information

### Planned Features
- [ ] Real-time data integration
- [ ] Additional strategy types
- [ ] Web-based dashboard
- [ ] Export to Excel/PDF
- [ ] Email notifications

## 👨‍💻 Author

ETF Backtester Development Team

## 🙏 Acknowledgments

- pandas for data manipulation
- matplotlib for visualizations
- MySQL for database backend
- Jupyter for interactive notebooks

---

**Last Updated**: November 2024
**Status**: Active Development
**Python Version**: 3.8+
**Database**: MySQL 8.0+
