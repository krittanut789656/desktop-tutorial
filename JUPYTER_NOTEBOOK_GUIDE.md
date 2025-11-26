# 📓 Jupyter Notebook Quick Start Guide

## ETF Portfolio Backtester - Notebook Version

### ✨ Why Use the Jupyter Notebook?

The Jupyter Notebook version (`ETF_Backtester_Integrated.ipynb`) is the **recommended way** to use the ETF Portfolio Backtester because it provides:

- ✅ **Better Visualization** - All charts and graphs display inline
- ✅ **Interactive Experience** - Run code step by step
- ✅ **Rich Documentation** - Markdown cells explain each section
- ✅ **Easy Debugging** - See outputs immediately
- ✅ **State Management** - Restart kernel to reset everything
- ✅ **Full Features** - Including Menu 3.4 for updating ETF information!

---

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Jupyter (if not already installed)

```bash
pip install jupyter
```

### Step 2: Launch the Notebook

```bash
cd /path/to/desktop-tutorial
jupyter notebook ETF_Backtester_Integrated.ipynb
```

This will open your web browser with the notebook.

### Step 3: Update Your Database Password

Find this cell (Cell 3):

```python
success = system.initialize_system(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='krittanut123456',  # ← Change this to your MySQL password!
    database='etf_backtester_db'
)
```

Update the `password` parameter with your MySQL password.

### Step 4: Run All Cells

**Option A - Run All at Once:**
- Click: `Cell → Run All`
- Wait for all cells to execute

**Option B - Run Step by Step:**
- Click on first cell
- Press `Shift + Enter` to run and move to next cell
- Repeat for all cells

### Step 5: Use the Interactive Menu

After all cells run, you'll see the interactive menu in the last cell's output:

```
================================================================================
ETF PORTFOLIO BACKTESTER - MAIN MENU
================================================================================

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
================================================================================

👉 Enter your choice:
```

Type your choice (e.g., `3.4`) and press Enter!

---

## 📊 Notebook Structure

The notebook is organized into clear sections:

### Cell 1: Title and Introduction (Markdown)
- Overview of the system
- Feature list
- Instructions

### Cell 2: Imports and Configuration (Code)
- Import all required modules
- Configure pandas and matplotlib
- Set up visualization style

### Cell 3: Main Controller Class (Code)
- Complete ETFBacktesterSystem class
- All menu operations (1.1 through 5.2)
- Including Menu 3.4 - Update ETF Information!

### Cell 4: System Initialization (Code)
- Create system instance
- Connect to database
- Check data status
- **⚠️ Update your password here!**

### Cell 5: Interactive Menu Loop (Code)
- Display menu and handle user input
- Route to appropriate operations
- Run continuously until exit

### Cell 6: Quick Reference Guide (Markdown)
- Usage tips
- Menu 3.4 examples
- Documentation links

---

## 🎯 First Time Setup

### 1. Load Sample Data

Before running any backtests, you need data:

```
👉 Enter your choice: 5.1
⚠️  Load sample data? This will add ETFs and price data. (yes/no): yes
```

This will:
- Load 10 sample ETFs
- Generate 1 year of price data
- Prepare the system for use

### 2. View ETF Information

Check what data was loaded:

```
👉 Enter your choice: 3.3
```

You'll see a table of all ETFs with:
- ETF_ID
- Ticker Symbol
- ETF Name
- Asset Type
- Timestamps

### 3. Try Menu 3.4 - Update ETF Information!

This is the **NEW feature**:

```
👉 Enter your choice: 3.4

📋 Current ETF Information:
[Table of all ETFs displayed]

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

👉 Enter choice (1-3): 2

Current value: SPDR S&P 500 ETF Trust
👉 Enter new value for ETF_Name: SPDR S&P 500 ETF (Updated Version)

⚠️  CONFIRMATION
   ETF ID: 1
   Field: ETF_Name
   Old Value: SPDR S&P 500 ETF Trust
   New Value: SPDR S&P 500 ETF (Updated Version)

👉 Proceed with update? (yes/no): yes

✅ Successfully updated!
   ETF_ID: 1
   Field: ETF_Name
   New Value: SPDR S&P 500 ETF (Updated Version)

📊 Updated ETF Information:
[Table showing updated record]

✅ Update completed successfully!
   Last Updated: 2024-11-26 12:34:56
```

---

## 💡 Tips and Tricks

### Restarting the System

If you need to restart:

1. Click: `Kernel → Restart & Clear Output`
2. Run all cells again
3. The system will reinitialize fresh

### Viewing Inline Charts

Charts automatically display in the notebook:

```
👉 Enter your choice: 4.1  # Plot Cumulative Returns
```

The chart appears right in the notebook!

### Stopping the Menu Loop

To exit the menu and stop execution:

```
👉 Enter your choice: 0
```

Or press the ⏹️ Stop button in Jupyter toolbar.

### Running Individual Operations

You can create new cells below and call operations directly:

```python
# Create a new cell and run specific operations
system.view_etf_info()
system.run_standard_backtest()
system.update_etf_info()
```

### Saving Your Work

The notebook automatically saves, but you can also:
- Click: `File → Save and Checkpoint`
- Or press: `Ctrl + S` (Windows/Linux) or `Cmd + S` (Mac)

---

## 🐛 Troubleshooting

### "Module not found" Error

Make sure you're in the correct directory:

```bash
cd /path/to/desktop-tutorial
jupyter notebook
```

All modules must be in the `modules/` folder.

### Database Connection Failed

Check:
1. MySQL is running: `sudo systemctl status mysql`
2. Password is correct in Cell 4
3. Database exists: `mysql -u root -p -e "SHOW DATABASES;"`

Re-run Cell 4 after fixing.

### Kernel Died or Crashed

1. Click: `Kernel → Restart`
2. Run all cells again
3. Check for error messages in the output

### Menu Not Responding

If the menu stops responding:
1. Click the ⏹️ Stop button
2. Scroll to Cell 5 (menu loop)
3. Click on the cell and press `Shift + Enter` to restart it

### Charts Not Displaying

Make sure the first cell has `%matplotlib inline`:

```python
%matplotlib inline
plt.style.use('seaborn-v0_8-darkgrid')
```

If charts still don't show, restart the kernel.

---

## 📚 Additional Resources

- **Main README**: [README.md](README.md) - Complete project documentation
- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md) - Detailed setup
- **Update Feature**: [README_UPDATE_FEATURE.md](README_UPDATE_FEATURE.md) - Menu 3.4 guide
- **Database Schema**: [database_schema.sql](database_schema.sql) - SQL structure

---

## 🎓 Learning Path

### Beginner:
1. ✅ Load sample data (Menu 5.1)
2. ✅ View ETF info (Menu 3.3)
3. ✅ Run standard backtest (Menu 1.1)
4. ✅ View results (Menu 3.1)

### Intermediate:
1. ✅ Try custom backtest (Menu 1.2)
2. ✅ Update ETF info (Menu 3.4) ⭐
3. ✅ Generate analytics (Menu 2.1)
4. ✅ Plot visualizations (Menu 4.1-4.3)

### Advanced:
1. ✅ Comparative backtest (Menu 1.3)
2. ✅ Optimize lookback periods (Menu 2.3)
3. ✅ Analyze drawdowns (Menu 2.4)
4. ✅ Create custom analysis cells

---

## 🎉 You're Ready!

The Jupyter Notebook version gives you the best interactive experience for the ETF Portfolio Backtester. Enjoy exploring the system and trying out Menu 3.4 to update ETF information!

**Happy Backtesting! 📊🚀**

---

**Version**: 1.0
**Last Updated**: November 2024
**Format**: Jupyter Notebook (.ipynb)
