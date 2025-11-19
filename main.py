"""
Portfolio Backtesting System - Main Program
DADS 4002 Programming Project

ระบบ Backtesting Portfolio แบบครบวงจร
- Python เป็น interface หลัก (ข้อ 1)
- Integrated system with menu (ข้อ 5a)
- CRUD operations (ข้อ 5d)
- SQL-based analytics (ข้อ 3)
- Text file logging (ข้อ 5b)
"""

import mysql.connector
from datetime import datetime
import os
import sys
from decimal import Decimal

# ============================================================
# Configuration
# ============================================================

MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456',
    'database': 'portfolio_backtesting'
}

LOG_FILE = 'logs/transaction.log'
BACKUP_DIR = 'backup'

# ============================================================
# Utility Functions
# ============================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def log_transaction(action, details, user="System"):
    """
    บันทึก transaction ลง text file (ข้อ 5b)
    """
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {user} - {action}: {details}\n"

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    print(f"✅ Logged: {action}")

def pause():
    """Wait for user to press Enter"""
    input("\n📌 กด Enter เพื่อดำเนินการต่อ...")

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"{title:^70}")
    print("="*70 + "\n")

# ============================================================
# Database Connection
# ============================================================

class DatabaseConnection:
    """จัดการ database connection"""

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to MySQL database"""
        try:
            self.conn = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            log_transaction("DATABASE_CONNECT", "Connected to MySQL successfully")
            return True
        except mysql.connector.Error as e:
            print(f"❌ Connection Error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        log_transaction("DATABASE_DISCONNECT", "Disconnected from MySQL")

    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"❌ Query Error: {e}")
            return None

    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return self.cursor.rowcount
        except mysql.connector.Error as e:
            print(f"❌ Update Error: {e}")
            self.conn.rollback()
            return 0

    def call_procedure(self, proc_name, args):
        """Call stored procedure"""
        try:
            result = self.cursor.callproc(proc_name, args)
            self.conn.commit()
            return result
        except mysql.connector.Error as e:
            print(f"❌ Procedure Error: {e}")
            return None

# ============================================================
# Module 1: ETF Management (CRUD)
# ============================================================

def manage_etf_menu(db):
    """จัดการข้อมูล ETF - CRUD operations"""
    while True:
        clear_screen()
        print_header("📊 จัดการข้อมูล ETF")
        print("1. ดูรายการ ETF ทั้งหมด (Read)")
        print("2. เพิ่ม ETF ใหม่ (Create)")
        print("3. แก้ไขข้อมูล ETF (Update)")
        print("4. ลบ ETF (Delete)")
        print("5. ค้นหา ETF")
        print("0. ← กลับเมนูหลัก")
        print("="*70)

        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            view_all_etfs(db)
        elif choice == "2":
            create_etf(db)
        elif choice == "3":
            update_etf(db)
        elif choice == "4":
            delete_etf(db)
        elif choice == "5":
            search_etf(db)
        elif choice == "0":
            break
        else:
            print("❌ ตัวเลือกไม่ถูกต้อง")
            pause()

def view_all_etfs(db):
    """Read - ดูรายการ ETF ทั้งหมด"""
    clear_screen()
    print_header("📊 รายการ ETF ทั้งหมด")

    query = """
        SELECT etf_id, ticker_symbol, etf_name, asset_class,
               expense_ratio, inception_date
        FROM etf_master
        ORDER BY ticker_symbol
    """

    results = db.execute_query(query)

    if results:
        print(f"{'ID':<5} {'Ticker':<10} {'Name':<30} {'Class':<15} {'Expense':<10}")
        print("-"*70)
        for row in results:
            print(f"{row['etf_id']:<5} {row['ticker_symbol']:<10} "
                  f"{row['etf_name']:<30} {row['asset_class']:<15} "
                  f"{row['expense_ratio'] or 'N/A':<10}")
        print(f"\n✅ Total: {len(results)} ETFs")
    else:
        print("❌ ไม่พบข้อมูล")

    log_transaction("ETF_VIEW", f"Viewed {len(results) if results else 0} ETFs")
    pause()

def create_etf(db):
    """Create - เพิ่ม ETF ใหม่"""
    clear_screen()
    print_header("➕ เพิ่ม ETF ใหม่")

    ticker = input("Ticker Symbol (เช่น SPY): ").strip().upper()
    name = input("ETF Name: ").strip()
    asset_class = input("Asset Class (เช่น Equity, Bond): ").strip()
    expense_ratio = input("Expense Ratio (เช่น 0.0003): ").strip()
    inception_date = input("Inception Date (YYYY-MM-DD): ").strip()

    query = """
        INSERT INTO etf_master (ticker_symbol, etf_name, asset_class,
                                expense_ratio, inception_date)
        VALUES (%s, %s, %s, %s, %s)
    """

    params = (ticker, name, asset_class,
              float(expense_ratio) if expense_ratio else None,
              inception_date if inception_date else None)

    result = db.execute_update(query, params)

    if result > 0:
        print(f"\n✅ เพิ่ม ETF {ticker} สำเร็จ!")
        log_transaction("ETF_CREATE", f"Added new ETF: {ticker} - {name}")
    else:
        print("\n❌ เพิ่ม ETF ไม่สำเร็จ")

    pause()

def update_etf(db):
    """Update - แก้ไขข้อมูล ETF"""
    clear_screen()
    print_header("✏️ แก้ไขข้อมูล ETF")

    ticker = input("ใส่ Ticker ที่ต้องการแก้ไข: ").strip().upper()

    # ตรวจสอบว่ามี ETF นี้หรือไม่
    check_query = "SELECT * FROM etf_master WHERE ticker_symbol = %s"
    result = db.execute_query(check_query, (ticker,))

    if not result:
        print(f"❌ ไม่พบ ETF: {ticker}")
        pause()
        return

    etf = result[0]
    print(f"\n📊 ข้อมูลปัจจุบัน:")
    print(f"Name: {etf['etf_name']}")
    print(f"Asset Class: {etf['asset_class']}")
    print(f"Expense Ratio: {etf['expense_ratio']}")

    print("\n✏️ ใส่ข้อมูลใหม่ (เว้นว่างถ้าไม่เปลี่ยน):")
    new_name = input(f"ETF Name [{etf['etf_name']}]: ").strip()
    new_class = input(f"Asset Class [{etf['asset_class']}]: ").strip()
    new_expense = input(f"Expense Ratio [{etf['expense_ratio']}]: ").strip()

    # Update
    update_query = """
        UPDATE etf_master
        SET etf_name = %s, asset_class = %s, expense_ratio = %s
        WHERE ticker_symbol = %s
    """

    params = (
        new_name if new_name else etf['etf_name'],
        new_class if new_class else etf['asset_class'],
        float(new_expense) if new_expense else etf['expense_ratio'],
        ticker
    )

    result = db.execute_update(update_query, params)

    if result > 0:
        print(f"\n✅ แก้ไขข้อมูล {ticker} สำเร็จ!")
        log_transaction("ETF_UPDATE", f"Updated ETF: {ticker}")
    else:
        print("\n❌ แก้ไขไม่สำเร็จ")

    pause()

def delete_etf(db):
    """Delete - ลบ ETF"""
    clear_screen()
    print_header("🗑️ ลบ ETF")

    ticker = input("ใส่ Ticker ที่ต้องการลบ: ").strip().upper()

    # ตรวจสอบว่ามี ETF นี้หรือไม่
    check_query = "SELECT * FROM etf_master WHERE ticker_symbol = %s"
    result = db.execute_query(check_query, (ticker,))

    if not result:
        print(f"❌ ไม่พบ ETF: {ticker}")
        pause()
        return

    etf = result[0]
    print(f"\n⚠️ ต้องการลบ ETF นี้หรือไม่?")
    print(f"Ticker: {etf['ticker_symbol']}")
    print(f"Name: {etf['etf_name']}")

    confirm = input("\nพิมพ์ 'YES' เพื่อยืนยันการลบ: ").strip()

    if confirm == "YES":
        delete_query = "DELETE FROM etf_master WHERE ticker_symbol = %s"
        result = db.execute_update(delete_query, (ticker,))

        if result > 0:
            print(f"\n✅ ลบ {ticker} สำเร็จ!")
            log_transaction("ETF_DELETE", f"Deleted ETF: {ticker}")
        else:
            print("\n❌ ลบไม่สำเร็จ")
    else:
        print("\n❌ ยกเลิกการลบ")

    pause()

def search_etf(db):
    """ค้นหา ETF"""
    clear_screen()
    print_header("🔍 ค้นหา ETF")

    keyword = input("ใส่คำค้นหา (Ticker หรือ Name): ").strip()

    query = """
        SELECT etf_id, ticker_symbol, etf_name, asset_class, expense_ratio
        FROM etf_master
        WHERE ticker_symbol LIKE %s OR etf_name LIKE %s
        ORDER BY ticker_symbol
    """

    results = db.execute_query(query, (f'%{keyword}%', f'%{keyword}%'))

    if results:
        print(f"\n{'ID':<5} {'Ticker':<10} {'Name':<35} {'Class':<15}")
        print("-"*70)
        for row in results:
            print(f"{row['etf_id']:<5} {row['ticker_symbol']:<10} "
                  f"{row['etf_name']:<35} {row['asset_class']:<15}")
        print(f"\n✅ พบ {len(results)} รายการ")
    else:
        print("❌ ไม่พบข้อมูล")

    log_transaction("ETF_SEARCH", f"Searched for: {keyword}, found {len(results) if results else 0}")
    pause()

# [ต่อในส่วนถัดไป - Portfolio Management, Analytics, etc.]
# ไฟล์ยาวมาก ผมจะแบ่งส่งในข้อความถัดไป

# ============================================================
# Main Menu (Simplified version)
# ============================================================

def main_menu(db):
    """เมนูหลักของระบบ"""
    while True:
        clear_screen()
        print_header("🏦 Portfolio Backtesting System - Main Menu")
        print("1. 📊 จัดการข้อมูล ETF (CRUD)")
        print("2. 📂 จัดการ Benchmark Portfolios")
        print("3. 📈 Data Analytics (SQL-based)")
        print("4. ⚙️  System Utilities (Logs, Backup)")
        print("5. ℹ️  About System")
        print("0. 🚪 ออกจากระบบ")
        print("="*70)

        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            manage_etf_menu(db)
        elif choice == "0":
            confirm = input("\n⚠️ ต้องการออกจากระบบ? (y/n): ").strip().lower()
            if confirm == 'y':
                print("\n👋 ขอบคุณที่ใช้งานระบบ Portfolio Backtesting!")
                log_transaction("SYSTEM_EXIT", "User exited system")
                break
        else:
            print("❌ ตัวเลือกไม่ถูกต้อง (ระบบกำลังพัฒนา)")
            pause()

# ============================================================
# Main Program Entry Point
# ============================================================

def main():
    """โปรแกรมหลัก - Entry Point"""
    try:
        # Clear screen
        clear_screen()

        # Splash Screen
        print("="*70)
        print("Portfolio Backtesting System".center(70))
        print("DADS 4002 Programming Project".center(70))
        print("="*70)
        print()

        # สร้าง directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('backup', exist_ok=True)
        os.makedirs('charts', exist_ok=True)

        # Connect to database
        print("🔌 กำลังเชื่อมต่อ MySQL...")
        db = DatabaseConnection()

        if not db.connect():
            print("\n❌ ไม่สามารถเชื่อมต่อ database ได้")
            print("กรุณาตรวจสอบ:")
            print("  1. MySQL service กำลังทำงานหรือไม่")
            print("  2. Username/Password ถูกต้องหรือไม่")
            print("  3. Database 'portfolio_backtesting' มีอยู่หรือไม่")
            return

        print("✅ เชื่อมต่อสำเร็จ!\n")

        # Log startup
        log_transaction("SYSTEM_START", "System started successfully")

        # เข้าสู่ main menu
        main_menu(db)

        # Disconnect
        db.disconnect()

    except KeyboardInterrupt:
        print("\n\n⚠️ ระบบถูกหยุดโดยผู้ใช้")
        log_transaction("SYSTEM_INTERRUPT", "System interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        log_transaction("SYSTEM_ERROR", f"Error: {str(e)}")
    finally:
        print("\n👋 ปิดระบบเรียบร้อย")

if __name__ == "__main__":
    main()
