"""
ETF Portfolio Backtesting System - Jupyter Notebook Interface

สำหรับใช้งานใน Jupyter Notebook โดยเฉพาะ
ไม่ใช้ interactive menu - ใช้ functions โดยตรง

Author: ETF Portfolio Backtesting System
"""

import os
import sys
from pathlib import Path

# ตั้งค่า project directory
try:
    PROJECT_DIR = Path(__file__).parent.absolute()
except NameError:
    PROJECT_DIR = Path(os.getcwd()).absolute()

# เพิ่ม paths
sys.path.insert(0, str(PROJECT_DIR / 'crud_operations'))
sys.path.insert(0, str(PROJECT_DIR / 'backtesting'))
sys.path.insert(0, str(PROJECT_DIR / 'analytics'))

print(f"✓ Project directory: {PROJECT_DIR}")

# Import modules
try:
    from crud_operations import crud_operations
    from backtesting import backtesting_engine
    from analytics import analytics
    print("✓ All modules imported successfully!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure you are in the project root directory")
    raise

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

def setup_database_config(password=''):
    """
    ตั้งค่า database configuration

    Args:
        password: MySQL password (ถ้าไม่ใส่จะใช้จาก config.ini)

    Returns:
        Database configuration dictionary
    """
    if password:
        return {
            'host': '127.0.0.1',
            'user': 'root',
            'password': password,
            'database': 'etf_backtesting',
            'port': 3306
        }

    # ลองอ่านจาก config.ini
    config_file = PROJECT_DIR / 'config.ini'
    if config_file.exists():
        import configparser
        config = configparser.ConfigParser()
        config.read(config_file)

        if 'database' in config:
            print("✓ Loaded config from config.ini")
            return {
                'host': config.get('database', 'host', fallback='127.0.0.1'),
                'user': config.get('database', 'user', fallback='root'),
                'password': config.get('database', 'password', fallback=''),
                'database': config.get('database', 'database', fallback='etf_backtesting'),
                'port': config.getint('database', 'port', fallback=3306)
            }

    print("⚠ No config.ini found. Please provide password.")
    return None

# Default config
DB_CONFIG = setup_database_config()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def test_connection(db_config=None):
    """ทดสอบการเชื่อมต่อ MySQL"""
    if db_config is None:
        db_config = DB_CONFIG

    try:
        import mysql.connector
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        print(f"✓ Connected to MySQL {version}")
        print(f"✓ Database: {db_config['database']}")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def show_portfolios(db_config=None):
    """แสดง portfolios ทั้งหมด"""
    if db_config is None:
        db_config = DB_CONFIG

    try:
        import mysql.connector
        import pandas as pd

        conn = mysql.connector.connect(**db_config)

        query = """
        SELECT
            p.portfolio_id,
            p.name,
            p.description,
            COUNT(pe.ticker) as etf_count,
            p.created_at
        FROM portfolios p
        LEFT JOIN portfolio_etfs pe ON p.portfolio_id = pe.portfolio_id
        GROUP BY p.portfolio_id
        ORDER BY p.portfolio_id
        """

        df = pd.read_sql(query, conn)
        conn.close()

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def show_portfolio_details(portfolio_id, db_config=None):
    """แสดงรายละเอียด portfolio"""
    if db_config is None:
        db_config = DB_CONFIG

    result = crud_operations.read_portfolio(portfolio_id, db_config=db_config)

    if result['success']:
        portfolio = result['portfolio']

        print(f"\n{'='*60}")
        print(f"Portfolio: {portfolio['name']}")
        print(f"{'='*60}")
        print(f"ID: {portfolio['portfolio_id']}")
        print(f"Description: {portfolio['description']}")
        print(f"Created: {portfolio['created_at']}")

        print(f"\nHoldings:")
        print(f"{'-'*60}")
        for etf in portfolio['etfs']:
            print(f"{etf['ticker']:<6} {etf['name']:<40} {etf['weight']:>6.2f}%")
        print(f"{'-'*60}")

        return portfolio
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
        return None

def show_etfs(db_config=None):
    """แสดง ETFs ทั้งหมด"""
    if db_config is None:
        db_config = DB_CONFIG

    try:
        import mysql.connector
        import pandas as pd

        conn = mysql.connector.connect(**db_config)

        query = """
        SELECT
            ticker,
            name,
            category,
            expense_ratio,
            COUNT(dp.date) as price_records,
            MAX(dp.date) as latest_date
        FROM etfs e
        LEFT JOIN daily_prices dp ON e.ticker = dp.ticker
        GROUP BY ticker
        ORDER BY category, ticker
        """

        df = pd.read_sql(query, conn)
        conn.close()

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def show_backtest_history(limit=20, db_config=None):
    """แสดงประวัติ backtests"""
    if db_config is None:
        db_config = DB_CONFIG

    try:
        import mysql.connector
        import pandas as pd

        conn = mysql.connector.connect(**db_config)

        query = f"""
        SELECT
            b.backtest_id,
            p.name as portfolio_name,
            b.strategy_type,
            b.start_date,
            b.end_date,
            b.initial_capital,
            b.final_value,
            b.total_return,
            b.created_at
        FROM backtests b
        JOIN portfolios p ON b.portfolio_id = p.portfolio_id
        ORDER BY b.created_at DESC
        LIMIT {limit}
        """

        df = pd.read_sql(query, conn)
        conn.close()

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

# =============================================================================
# ANALYTICS FUNCTIONS (Easy to use)
# =============================================================================

def run_risk_analysis(portfolio_ids, start_date='2020-01-01', end_date='2024-12-31',
                     benchmark='SPY', db_config=None):
    """
    วิเคราะห์ความเสี่ยงและผลตอบแทน

    Args:
        portfolio_ids: List of portfolio IDs เช่น [1, 2, 3]
        start_date: วันเริ่มต้น
        end_date: วันสิ้นสุด
        benchmark: Benchmark symbol (default: SPY)
        db_config: Database config

    Returns:
        Dict with results
    """
    if db_config is None:
        db_config = DB_CONFIG

    print(f"Running risk analysis for portfolios {portfolio_ids}...")
    print(f"Period: {start_date} to {end_date}")
    print(f"Benchmark: {benchmark}\n")

    result = analytics.generate_risk_adjusted_report(
        portfolio_ids=portfolio_ids,
        start_date=start_date,
        end_date=end_date,
        benchmark_symbol=benchmark,
        output_file='insight1_risk_adjusted_report.txt',
        db_config=db_config
    )

    print("\n✓ Analysis complete!")
    print("📄 Report saved to: insight1_risk_adjusted_report.txt")

    return result

def run_rebalancing_analysis(portfolio_id, start_date='2020-01-01', end_date='2024-12-31',
                            initial_capital=100000.0, db_config=None):
    """
    วิเคราะห์ความถี่ rebalancing ที่ดีที่สุด

    Args:
        portfolio_id: Portfolio ID
        start_date: วันเริ่มต้น
        end_date: วันสิ้นสุด
        initial_capital: เงินลงทุนเริ่มต้น
        db_config: Database config

    Returns:
        Dict with results
    """
    if db_config is None:
        db_config = DB_CONFIG

    print(f"Running rebalancing analysis for portfolio {portfolio_id}...")
    print(f"This will run 5 backtests and may take 3-5 minutes...\n")

    result = analytics.compare_rebalancing_strategies(
        portfolio_id=portfolio_id,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        output_file='insight2_rebalancing_analysis.txt',
        db_config=db_config
    )

    if result['success']:
        print("\n✓ Analysis complete!")
        print(f"🏆 Best Strategy: {result['best_strategy']}")
        print(f"📈 Best Return: {result['best_return']:.2f}%")
        print(f"📊 Best Sharpe: {result['best_sharpe']:.3f}")
        print("📄 Report saved to: insight2_rebalancing_analysis.txt")

    return result

def run_dca_analysis(portfolio_id, total_capital=100000.0, investment_months=12,
                    start_date='2020-01-01', end_date='2024-12-31', db_config=None):
    """
    เปรียบเทียบ DCA vs Lump Sum

    Args:
        portfolio_id: Portfolio ID
        total_capital: จำนวนเงินทั้งหมด
        investment_months: ระยะเวลาทยอยซื้อ (เดือน)
        start_date: วันเริ่มต้น
        end_date: วันสิ้นสุด
        db_config: Database config

    Returns:
        Dict with results
    """
    if db_config is None:
        db_config = DB_CONFIG

    print(f"Comparing DCA vs Lump Sum for portfolio {portfolio_id}...")
    print(f"Total Capital: ${total_capital:,.0f}")
    print(f"DCA Period: {investment_months} months\n")

    result = analytics.compare_dca_vs_lumpsum(
        portfolio_id=portfolio_id,
        total_capital=total_capital,
        investment_period_months=investment_months,
        start_date=start_date,
        end_date=end_date,
        output_file='insight3_dca_vs_lumpsum.txt',
        db_config=db_config
    )

    if result['success']:
        print("\n✓ Analysis complete!")
        print(f"💰 Lump Sum Return: {result['lumpsum_annualized_return']:.2f}%")
        print(f"📊 DCA Return: {result['dca_annualized_return']:.2f}%")
        print(f"🏆 Winner: {result['winner']}")
        print("📄 Report saved to: insight3_dca_vs_lumpsum.txt")

    return result

def run_backtest(portfolio_id, start_date='2020-01-01', end_date='2024-12-31',
                initial_capital=100000.0, strategy='buy_hold', db_config=None):
    """
    Run backtest

    Args:
        portfolio_id: Portfolio ID
        start_date: วันเริ่มต้น
        end_date: วันสิ้นสุด
        initial_capital: เงินลงทุนเริ่มต้น
        strategy: 'buy_hold', 'periodic_rebalancing', หรือ 'dca'
        db_config: Database config

    Returns:
        backtest_id
    """
    if db_config is None:
        db_config = DB_CONFIG

    print(f"Running {strategy} backtest for portfolio {portfolio_id}...")

    backtest_id = backtesting_engine.run_backtest(
        portfolio_id=portfolio_id,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        strategy_type=strategy,
        transaction_cost=0.001,
        db_config=db_config
    )

    print(f"\n✓ Backtest completed! ID: {backtest_id}")

    return backtest_id

# =============================================================================
# QUICK START MESSAGE
# =============================================================================

def show_quick_start():
    """แสดงคำแนะนำการใช้งานเร็ว"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   ETF Portfolio Backtesting System - Jupyter Interface        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

🚀 Quick Start Guide:

1️⃣ Setup Database Config (ครั้งแรก):

   DB_CONFIG = setup_database_config(password='YOUR_PASSWORD')
   test_connection(DB_CONFIG)

2️⃣ ดูข้อมูลพื้นฐาน:

   # ดู portfolios
   df = show_portfolios(DB_CONFIG)
   display(df)

   # ดูรายละเอียด portfolio
   show_portfolio_details(1, DB_CONFIG)

   # ดู ETFs
   df = show_etfs(DB_CONFIG)
   display(df)

3️⃣ Run Analytics:

   # Risk analysis
   run_risk_analysis([1, 2, 3], db_config=DB_CONFIG)

   # Rebalancing analysis
   run_rebalancing_analysis(1, db_config=DB_CONFIG)

   # DCA vs Lump Sum
   run_dca_analysis(1, db_config=DB_CONFIG)

4️⃣ Run Backtest:

   backtest_id = run_backtest(
       portfolio_id=1,
       strategy='buy_hold',
       db_config=DB_CONFIG
   )

5️⃣ ดูผลลัพธ์:

   # ดู backtest history
   df = show_backtest_history(db_config=DB_CONFIG)
   display(df)

   # อ่าน reports
   with open('insight1_risk_adjusted_report.txt', 'r') as f:
       print(f.read())

💡 Tips:
   - ใช้ display(df) แสดง DataFrame สวยๆ
   - Reports จะถูกบันทึกในไฟล์ .txt
   - ใช้ %matplotlib inline สำหรับ charts

📚 Documentation:
   - USER_GUIDE_TH.md (คู่มือภาษาไทย)
   - QUICKSTART_TH.md (เริ่มใช้งานเร็ว)

════════════════════════════════════════════════════════════════
""")

# แสดง quick start เมื่อ import
show_quick_start()

print("✓ Ready to use! Import successful.")
print("\n💡 Next step: DB_CONFIG = setup_database_config(password='YOUR_PASSWORD')")
