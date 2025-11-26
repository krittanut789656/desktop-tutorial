# ETF Portfolio Backtester - Installation Guide

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## 🚀 Quick Start Installation

### Step 1: Clone or Download the Project

```bash
cd /path/to/your/projects
git clone <repository-url>
cd desktop-tutorial
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas numpy mysql-connector-python matplotlib seaborn jupyter ipython
```

### Step 3: Set Up MySQL Database

1. **Start MySQL Server**
   ```bash
   # On Linux
   sudo systemctl start mysql

   # On macOS
   brew services start mysql

   # On Windows
   # Start MySQL from Services or MySQL Workbench
   ```

2. **Create Database and Tables**
   ```bash
   mysql -u root -p < database_schema.sql
   ```

   Or manually:
   ```sql
   -- Login to MySQL
   mysql -u root -p

   -- Create database
   CREATE DATABASE etf_backtester_db;
   USE etf_backtester_db;

   -- Run the schema file
   source database_schema.sql;
   ```

3. **Verify Database Setup**
   ```sql
   USE etf_backtester_db;
   SHOW TABLES;
   -- Should show: ETF_Master, Price_Data, Strategy_Log
   ```

### Step 4: Configure Database Connection

Edit `etf_backtester_integrated.py` line ~445:

```python
success = system.initialize_system(
    host='127.0.0.1',      # Your MySQL host
    port=3306,             # Your MySQL port
    user='root',           # Your MySQL username
    password='YOUR_PASSWORD_HERE',  # ← Change this!
    database='etf_backtester_db'
)
```

### Step 5: Run the System

**Option A: Python Script**
```bash
python etf_backtester_integrated.py
```

**Option B: Jupyter Notebook**
```bash
jupyter notebook
# Open the notebook and run all cells
```

### Step 6: Load Sample Data

1. Run the system
2. Select menu option `5.1 - Load Sample Data`
3. Confirm with `yes`

This will:
- Load 10 sample ETFs
- Generate 1 year of price data
- Prepare the system for backtesting

## 📁 Project Structure

```
desktop-tutorial/
├── modules/
│   ├── __init__.py
│   ├── db_connector.py          # Database connection pooling
│   ├── backtest_engine.py       # Momentum backtesting logic
│   ├── analytics.py             # Portfolio analytics
│   ├── crud_operations.py       # CRUD operations (includes UPDATE)
│   └── data_loader.py           # Data loading utilities
├── etf_backtester_integrated.py # Main integrated system
├── database_schema.sql          # MySQL database schema
├── requirements.txt             # Python dependencies
├── INSTALLATION.md              # This file
├── README_UPDATE_FEATURE.md     # Documentation for menu 3.4
└── README.md                    # Project overview
```

## 🔧 Troubleshooting

### Issue: Cannot connect to MySQL

**Solution:**
1. Check if MySQL is running:
   ```bash
   # Linux
   sudo systemctl status mysql

   # macOS
   brew services list

   # Windows
   # Check Services panel
   ```

2. Verify credentials:
   ```bash
   mysql -u root -p
   # If this fails, reset your MySQL password
   ```

3. Check port availability:
   ```bash
   netstat -an | grep 3306
   ```

### Issue: Module import errors

**Solution:**
```bash
# Ensure you're in the correct directory
cd /path/to/desktop-tutorial

# Verify modules directory exists
ls -la modules/

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: Database tables don't exist

**Solution:**
```bash
# Re-run the schema
mysql -u root -p etf_backtester_db < database_schema.sql

# Or manually in MySQL
mysql -u root -p
USE etf_backtester_db;
source database_schema.sql;
```

### Issue: Permission denied on database operations

**Solution:**
```sql
-- Grant all privileges
GRANT ALL PRIVILEGES ON etf_backtester_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Issue: No data available

**Solution:**
1. Load sample data via menu `5.1`
2. Or run data loader programmatically:
   ```python
   system.data_loader.initialize_database()
   ```

## 🧪 Testing the Installation

Run these commands to verify everything works:

```python
# Test 1: Import modules
from modules.db_connector import DatabaseConnector, DatabaseConfig
from modules.crud_operations import CRUDOperations
print("✓ Modules imported successfully")

# Test 2: Database connection
config = DatabaseConfig()
config.password = 'YOUR_PASSWORD'
db = DatabaseConnector(config)
print("✓ Database connected")

# Test 3: Check tables
count = db.get_table_count('ETF_Master')
print(f"✓ ETF_Master has {count} records")

# Test 4: CRUD operations
crud = CRUDOperations(db)
crud.read_etf_info()
print("✓ CRUD operations working")
```

## 📚 Next Steps

After installation:

1. ✅ Load sample data (Menu 5.1)
2. ✅ Run a standard backtest (Menu 1.1)
3. ✅ View ETF information (Menu 3.3)
4. ✅ Try the new update feature (Menu 3.4)
5. ✅ Explore analytics (Menu 2.1)
6. ✅ Generate visualizations (Menu 4.1-4.3)

## 🆘 Getting Help

If you encounter issues:

1. Check the error message carefully
2. Verify all prerequisites are installed
3. Review the troubleshooting section
4. Check database connection and permissions
5. Ensure all files are in the correct directory

## 🔄 Updating the System

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🗑️ Uninstallation

To completely remove the system:

```bash
# Remove Python packages
pip uninstall pandas numpy mysql-connector-python matplotlib seaborn jupyter -y

# Drop database
mysql -u root -p -e "DROP DATABASE etf_backtester_db;"

# Remove project files
cd ..
rm -rf desktop-tutorial
```

## 📝 System Requirements

**Minimum:**
- Python 3.8+
- MySQL 8.0+
- 2GB RAM
- 1GB free disk space

**Recommended:**
- Python 3.10+
- MySQL 8.0+
- 4GB+ RAM
- 5GB+ free disk space
- SSD for better database performance

---

**Installation Support**: For issues, please check the troubleshooting section or create an issue in the repository.
