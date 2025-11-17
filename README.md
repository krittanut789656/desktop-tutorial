# ETF Portfolio Backtesting System

**Comprehensive MySQL-based portfolio backtesting and analytics platform for ETF investors**

A complete end-to-end system for managing ETF portfolios, running backtests with multiple strategies, and generating actionable investment insights using advanced analytics.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
[Modules](#modules)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The ETF Portfolio Backtesting System is a professional-grade application designed for:

- **Portfolio Managers** - Test and optimize portfolio strategies
- **Quantitative Analysts** - Analyze risk-adjusted performance metrics
- **Individual Investors** - Make data-driven investment decisions
- **Researchers** - Study market conditions and investment strategies

### What Makes This System Unique?

✅ **SQL-Optimized** - Leverages MySQL window functions for fast analytics
✅ **Production-Ready** - Comprehensive error handling and logging
✅ **User-Friendly** - Menu-driven console interface with color-coded output
✅ **Extensible** - Modular architecture for easy customization
✅ **Well-Documented** - Complete documentation and examples
✅ **Scientifically Sound** - Based on established financial metrics

---

## 🚀 Features

### 1. Portfolio Management
- Create custom ETF portfolios with flexible weighting
- View and compare multiple portfolios
- Update portfolio allocations dynamically
- Delete portfolios with cascade safety

### 2. ETF Data Management
- 40+ pre-loaded popular ETFs (US Equity, International, Bonds, Commodities, REITs)
- Automatic price data collection using yfinance
- Historical data from 2009-2025
- Data validation and quality checks

### 3. Backtesting Engine
Three powerful strategies:
- **Buy & Hold** - Passive investment baseline
- **Periodic Rebalancing** - Maintain target weights (monthly, quarterly, semi-annual, annual)
- **Dollar Cost Averaging (DCA)** - Regular contributions over time

Features:
- Transaction cost modeling (0.1% default)
- Progress bars for long-running backtests
- Batch processing for performance
- Comprehensive result storage

### 4. Analytics & Insights

#### Insight 1: Risk-Adjusted Performance Analysis
- Sharpe, Sortino, and Calmar ratios
- Maximum drawdown calculation
- Alpha and Beta vs benchmark (SPY)
- Risk-return scatter plots
- Drawdown comparison charts

#### Insight 2: Optimal Rebalancing Frequency Analysis
- Automatic comparison of 5 rebalancing strategies
- Transaction cost vs performance trade-off
- Cost-benefit analysis
- Actionable recommendations

#### Insight 3: DCA vs Lump Sum Market Timing Analysis
- Compare investment entry strategies
- Market condition detection (bull/bear/neutral)
- Win rate analysis
- Psychological insights
- Hybrid strategy recommendations

### 5. Reports & Visualization
- Detailed text reports for all analyses
- Professional matplotlib/seaborn charts
- Publication-ready visualizations (300 DPI)
- Comprehensive logging system

### 6. Console Application
- Interactive menu-driven interface
- Color-coded output (colorama)
- Pretty-printed tables (tabulate)
- Input validation and error handling
- Session management
- Database connection pooling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MAIN APPLICATION (main.py)                  │
│              Menu-driven Console Interface                      │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   Portfolio  │      │     ETF      │     │  Backtest    │
│  Management  │      │  Management  │     │   Engine     │
│   (CRUD)     │      │              │     │              │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  MySQL Database  │
                    │  8 Normalized    │
                    │     Tables       │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │    Analytics     │
                    │    3 Insights    │
                    │  Visualizations  │
                    └──────────────────┘
```

---

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **MySQL 8.0+**
- **pip** (Python package manager)

### Step 1: Clone Repository

```bash
git clone https://github.com/krittanut789656/desktop-tutorial.git
cd desktop-tutorial
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

```bash
cd database

# Create database and tables
mysql -u root -p < 01_create_database.sql

# Insert sample ETFs
mysql -u root -p < 02_insert_sample_etfs.sql

# Insert sample portfolios (optional)
mysql -u root -p < 03_insert_sample_portfolios.sql
```

### Step 5: Configure Database Connection

```bash
# Run main.py and enter credentials when prompted
python main.py
```

### Step 6: Load ETF Price Data

```bash
cd data_collection
python data_collection.py
# This will fetch historical prices for 40+ ETFs from 2009-2025
# Takes approximately 10-15 minutes
```

---

## 🚀 Quick Start

### Launch Main Application

```bash
python main.py
```

### Quick Example Workflow

```
1. Launch application: python main.py
2. Go to menu 1.2 (View Portfolios)
3. Select a portfolio to view details
4. Go to menu 4.1 (Risk-Adjusted Performance Analysis)
5. Follow instructions to analyze portfolio
6. View generated reports in analytics/ folder
```

### Run Analytics Examples

```bash
cd analytics
python example_analytics.py

# Interactive menu:
# 1. Risk-Adjusted Performance Analysis
# 2. Optimal Rebalancing Frequency Analysis
# 3. DCA vs Lump Sum Market Timing Analysis
# 4. Run All Insights (Comprehensive)
# 5. Custom Analysis Example
```

---

## 📊 Using Jupyter Notebooks (Recommended for Beginners!)

**เรียนรู้ง่าย - ใช้งานได้ทันที!**

### 🎯 แนะนำ: `Simple_Run_All.ipynb`

Notebook ที่ง่ายที่สุด - ไม่มีปัญหา import errors!

```bash
jupyter notebook Simple_Run_All.ipynb
```

**ทำอะไรได้:**
- ✅ ดู Portfolios และ ETFs
- ✅ ดูข้อมูลราคา
- ✅ วิเคราะห์ด้วย Pandas
- ✅ สร้าง Charts
- ✅ ไม่ต้อง import external files

### 📚 Notebooks อื่นๆ:

- **`Complete_Setup_and_Run.ipynb`** - สำหรับ setup ครั้งแรก
- **`ETF_Backtesting_Notebook.ipynb`** - Advanced features
- **`jupyter_interface.py`** - Python module สำหรับ custom notebooks

### 🤔 ควรใช้ Notebook ไหน?

**อ่านคู่มือฉบับเต็ม:** [`WHICH_NOTEBOOK_TO_USE.md`](WHICH_NOTEBOOK_TO_USE.md)

**สรุปสั้นๆ:**
- 🆕 **ครั้งแรก**: ใช้ `Complete_Setup_and_Run.ipynb` (setup database)
- 📊 **ใช้งานทั่วไป**: ใช้ `Simple_Run_All.ipynb` (ง่ายที่สุด!)
- 🔬 **Advanced**: ใช้ `jupyter_interface.py` + custom notebook

---

## 📂 Project Structure

```
desktop-tutorial/
├── main.py                      # Main console application
├── config.py                    # Configuration management
├── requirements.txt             # All dependencies
├── README.md                    # This file
│
├── database/                    # Phase 1: Database Schema
│   ├── 01_create_database.sql
│   ├── 02_insert_sample_etfs.sql
│   ├── 03_insert_sample_portfolios.sql
│   └── README.md
│
├── data_collection/             # Phase 2: ETF Price Data
│   ├── data_collection.py
│   ├── config.py
│   └── README.md
│
├── crud_operations/             # Phase 3: CRUD Operations
│   ├── crud_operations.py
│   └── README.md
│
├── backtesting/                 # Phase 4: Backtesting Engine
│   ├── backtesting_engine.py
│   ├── example_backtest.py
│   └── README.md
│
└── analytics/                   # Phase 5: Analytics & Insights
    ├── analytics.py
    ├── visualizations.py
    ├── example_analytics.py
    └── README.md
```

---

## 💻 Main Application Menu

```
═══════════════════════════════════════════════════════════════
                ETF PORTFOLIO BACKTESTING SYSTEM
═══════════════════════════════════════════════════════════════

1. Portfolio Management
2. ETF Management
3. Run Backtest
4. Analytics & Insights
5. Reports & Export
6. System Settings
0. Exit
```

---

## 📖 Usage Guide

### Creating a Portfolio

1. Run `python main.py`
2. Select **1. Portfolio Management**
3. Select **1.1 Create New Portfolio**
4. Enter portfolio name and select ETFs
5. Enter weights (must sum to 100%)

### Running Analytics

```bash
cd analytics
python example_analytics.py
```

Or use directly:

```python
import analytics

# Risk-Adjusted Analysis
analytics.generate_risk_adjusted_report(
    portfolio_ids=[1, 2, 3],
    start_date='2020-01-01',
    end_date='2024-12-31',
    benchmark_symbol='SPY',
    output_file='risk_analysis.txt',
    db_config=DB_CONFIG
)
```

---

## 🔧 Modules

### Phase 1: Database Schema
8 normalized MySQL tables with foreign key constraints
[📖 Documentation](database/README.md)

### Phase 2: Data Collection
yfinance integration for 40+ ETFs (2009-2025)
[📖 Documentation](data_collection/README.md)

### Phase 3: CRUD Operations
Portfolio, ETF, and backtest management
[📖 Documentation](crud_operations/README.md)

### Phase 4: Backtesting Engine
3 strategies: Buy & Hold, Rebalancing, DCA
[📖 Documentation](backtesting/README.md)

### Phase 5: Analytics & Insights
3 comprehensive insights with visualizations
[📖 Documentation](analytics/README.md)

### Phase 6: Main Application
Menu-driven console interface
See main.py for details

---

## 🔍 Troubleshooting

### Database Connection Error
```bash
# Check MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u root -p

# Update credentials when prompted in main.py
```

### Module Import Error
```bash
# Ensure you're in project root
cd desktop-tutorial

# Reinstall dependencies
pip install -r requirements.txt
```

### No Price Data
```bash
# Run data collection
cd data_collection
python data_collection.py
```

---

## 📝 Configuration

### Environment Variables

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=etf_backtesting
```

### config.ini File

```bash
# Generate template
python config.py --create-template

# Edit config.ini with your settings
```

---

## 📈 Performance

- Portfolio creation: <0.1 seconds
- Backtest (5 years): 5-10 seconds
- Analytics (3 insights): 15-30 seconds
- Data collection (40 ETFs, 15 years): 10-15 minutes

---

## 🤝 Contributing

Contributions welcome! Fork, create feature branch, test, and submit PR.

---

## 📄 License

Educational/Personal Use

---

## 👨‍💻 Author

**ETF Portfolio Backtesting System**
Complete 6-Phase Implementation

---

## 🎯 Roadmap

- [ ] Web-based UI
- [ ] Real-time data updates
- [ ] Monte Carlo simulations
- [ ] Factor analysis
- [ ] Machine learning predictions

---

**Built with ❤️ for ETF investors and quantitative analysts**

**Happy Investing! 📊🚀**
