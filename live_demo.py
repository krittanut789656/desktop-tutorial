#!/usr/bin/env python3
"""
🎬 Live Demo - Portfolio Backtesting System
DADS 4002 - Database Systems Project

Interactive Analytics Demo with SQL Stored Procedures

วิธีใช้งาน:
    python3 live_demo.py

จากนั้นเลือก Option 1-5 เพื่อ Demo Analytics Features
เลือก 0 เพื่อออกจากโปรแกรม
"""

import mysql.connector
import os
from datetime import datetime

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krittanut123456',
    'database': 'portfolio_backtesting'
}


class DatabaseConnection:
    """จัดการการเชื่อมต่อ MySQL Database"""

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """เชื่อมต่อ Database"""
        try:
            self.conn = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            return True
        except mysql.connector.Error as e:
            print(f"❌ Connection Error: {e}")
            print("💡 กรุณาตรวจสอบว่า MySQL Server กำลังทำงานอยู่")
            return False

    def disconnect(self):
        """ตัดการเชื่อมต่อ"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def clear_screen():
    """ล้างหน้าจอ (ใช้งานได้ทั้ง Windows และ Unix)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """แสดง Analytics Menu"""
    print("\n" + "="*80)
    print("📈 Data Analytics Menu (SQL-based)")
    print("="*80)
    print("")
    print("1. 🏆 Top Performers - Top 5 ETFs ที่ดีที่สุด")
    print("2. ⚖️  Portfolio Comparison - เปรียบเทียบ Portfolios ทั้งหมด")
    print("3. 🔗 ETF Correlation - วิเคราะห์ความสัมพันธ์ระหว่าง ETFs")
    print("4. 📊 Sharpe Ratio Calculator - คำนวณ Sharpe Ratio")
    print("5. 📈 Top 10 ETFs Performance - ดูผลตอบแทนจาก SQL View")
    print("0. 🚪 Exit - ออกจากโปรแกรม")
    print("")
    print("="*80)


def top_performers(cursor):
    """Analytics #1: Top Performers using sp_get_top_performers"""
    print("\n" + "="*80)
    print("🏆 Top 5 ETFs ที่มี Sharpe Ratio สูงสุด")
    print("="*80)
    print("📌 ใช้ SQL Stored Procedure: sp_get_top_performers")
    print("="*80)

    try:
        # Call Stored Procedure
        cursor.callproc('sp_get_top_performers', ['sharpe', 5, '2009-01-01', '2025-01-01'])

        # Fetch results
        for result in cursor.stored_results():
            rows = result.fetchall()

        if rows:
            print(f"\n{'Rank':<6} {'Ticker':<10} {'ETF Name':<30} {'Return':<12} {'Volatility':<12} {'Sharpe':<10}")
            print("-"*80)

            for i, row in enumerate(rows, 1):
                ticker = row['ticker_symbol']
                name = row['etf_name'][:28]
                ret = f"{row['annualized_return_pct']:.2f}%"
                vol = f"{row['annualized_volatility_pct']:.2f}%"
                sharpe = f"{row['sharpe_ratio']:.4f}"
                print(f"#{i:<5} {ticker:<10} {name:<30} {ret:<12} {vol:<12} {sharpe:<10}")

            # Actionable Insights
            top = rows[0]
            print("\n💡 Actionable Insights:")
            print(f"   - 🎯 {top['ticker_symbol']} มี Sharpe Ratio สูงสุด ({top['sharpe_ratio']:.4f})")
            print(f"   - 📊 ผลตอบแทนต่อปี: {top['annualized_return_pct']:.2f}%")
            print(f"   - 💼 แนะนำสำหรับนักลงทุนที่ต้องการผลตอบแทนดีเมื่อปรับความเสี่ยง")
            if top['sharpe_ratio'] > 1.0:
                print(f"   - ✅ Sharpe Ratio > 1.0 = ผลตอบแทนคุ้มค่ากับความเสี่ยง")
        else:
            print("\n❌ ไม่พบข้อมูล")

    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("💡 กรุณาตรวจสอบว่า Stored Procedure ถูกติดตั้งแล้ว (รัน setup_procedures.py)")


def portfolio_comparison(cursor):
    """Analytics #2: Portfolio Comparison using sp_compare_portfolios"""
    print("\n" + "="*80)
    print("⚖️  เปรียบเทียบ Benchmark Portfolios")
    print("="*80)
    print("📌 ใช้ SQL Stored Procedure: sp_compare_portfolios")
    print("="*80)

    try:
        # Call Stored Procedure
        cursor.callproc('sp_compare_portfolios', ['2020-01-01', '2025-01-01'])

        # Fetch results
        for result in cursor.stored_results():
            rows = result.fetchall()

        if rows:
            print(f"\n{'Portfolio':<30} {'Risk Level':<15} {'Return':<12} {'Volatility':<12} {'Sharpe':<10}")
            print("-"*80)

            for row in rows:
                portfolio = row['benchmark_name'][:28]
                risk = row['risk_level'][:13]
                ret = f"{row['portfolio_return_pct']:.2f}%"
                vol = f"{row['annualized_volatility_pct']:.2f}%"
                sharpe = f"{row['sharpe_ratio']:.4f}"
                print(f"{portfolio:<30} {risk:<15} {ret:<12} {vol:<12} {sharpe:<10}")

            # Actionable Insights
            best = max(rows, key=lambda x: x['sharpe_ratio'])
            print("\n💡 Actionable Insights:")
            print(f"   - 🏆 Portfolio ที่ดีที่สุด: {best['benchmark_name']}")
            print(f"   - 📊 Sharpe Ratio: {best['sharpe_ratio']:.4f}")
            print(f"   - 💰 ผลตอบแทนต่อปี: {best['portfolio_return_pct']:.2f}%")
            print(f"   - 🎯 ระดับความเสี่ยง: {best['risk_level']}")
            print(f"   - 💼 แนะนำสำหรับนักลงทุนที่ต้องการ Risk-adjusted Return ที่ดี")
        else:
            print("\n❌ ไม่พบข้อมูล")

    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("💡 กรุณาตรวจสอบว่า Stored Procedure ถูกติดตั้งแล้ว (รัน setup_procedures.py)")


def etf_correlation(cursor):
    """Analytics #3: ETF Correlation using sp_get_etf_correlation"""
    print("\n" + "="*80)
    print("🔗 ETF Correlation Analysis")
    print("="*80)
    print("📌 ใช้ SQL Stored Procedure: sp_get_etf_correlation")
    print("="*80)

    ticker1 = input("\nป้อน Ticker 1 (เช่น SPY): ").strip().upper()
    ticker2 = input("ป้อน Ticker 2 (เช่น QQQ): ").strip().upper()

    try:
        # Call Stored Procedure
        result_args = cursor.callproc('sp_get_etf_correlation', [ticker1, ticker2, 0])
        correlation = result_args[2]

        if correlation is not None:
            print(f"\n📊 {ticker1} vs {ticker2}")
            print("-"*80)
            print(f"Correlation: {correlation:.4f}")

            # Interpretation
            if correlation > 0.8:
                strength = "แข็งแกร่งมาก (Highly Correlated)"
                recommendation = "⚠️  ไม่แนะนำให้ถือทั้ง 2 ETFs ในพอร์ตเดียวกัน"
                reason = "มีความเสี่ยงคล้ายกันมาก ไม่ได้ช่วย Diversify"
            elif correlation > 0.5:
                strength = "แข็งแกร่งปานกลาง (Moderately Correlated)"
                recommendation = "⚠️  ควรพิจารณาสัดส่วนการถืออย่างรอบคอบ"
                reason = "มีความสัมพันธ์ปานกลาง อาจช่วย Diversify ได้บ้าง"
            elif correlation > 0:
                strength = "อ่อน (Weakly Correlated)"
                recommendation = "✅ เหมาะสำหรับถือร่วมกัน"
                reason = "ช่วย Diversify ความเสี่ยงได้ดี"
            else:
                strength = "ติดลบ (Negative Correlation)"
                recommendation = "✅ ดีมากสำหรับ Diversification"
                reason = "เคลื่อนไหวในทิศทางตรงข้าม ช่วยลดความเสี่ยง"

            print(f"\nความสัมพันธ์: {strength}")
            print("\n💡 Actionable Insights:")
            print(f"   - {recommendation}")
            print(f"   - เหตุผล: {reason}")
        else:
            print("\n❌ ไม่พบข้อมูลหรือ Ticker ไม่ถูกต้อง")
            print("💡 ตัวอย่าง Ticker: SPY, QQQ, AGG, GLD, VTI, BND")

    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("💡 กรุณาตรวจสอบว่า Stored Procedure ถูกติดตั้งแล้ว (รัน setup_procedures.py)")


def sharpe_ratio_calculator(cursor):
    """Analytics #4: Sharpe Ratio Calculator using sp_calculate_sharpe_ratio"""
    print("\n" + "="*80)
    print("📊 Sharpe Ratio Calculator")
    print("="*80)
    print("📌 ใช้ SQL Stored Procedure: sp_calculate_sharpe_ratio")
    print("="*80)

    ticker = input("\nป้อน Ticker Symbol (เช่น SPY): ").strip().upper()

    try:
        risk_free = float(input("Risk-Free Rate (เช่น 0.02 = 2%): ").strip())
    except:
        risk_free = 0.02
        print(f"ใช้ค่า Default: {risk_free}")

    try:
        # Call Stored Procedure
        result_args = cursor.callproc('sp_calculate_sharpe_ratio', [ticker, risk_free, 0])
        sharpe = result_args[2]

        if sharpe is not None:
            print(f"\n📊 Sharpe Ratio Analysis: {ticker}")
            print("-"*80)
            print(f"Risk-Free Rate: {risk_free*100:.2f}%")
            print(f"Sharpe Ratio: {sharpe:.4f}")

            # Rating
            if sharpe > 2:
                rating = "Excellent (ยอดเยี่ยม)"
            elif sharpe > 1:
                rating = "Good (ดี)"
            elif sharpe > 0.5:
                rating = "Fair (พอใช้)"
            else:
                rating = "Poor (ควรหลีกเลี่ยง)"

            print(f"\n💡 Actionable Insights:")
            print(f"   - 🎯 Rating: {rating}")
            if sharpe > 1:
                print(f"   - ✅ Sharpe Ratio > 1.0 = ผลตอบแทนคุ้มค่ากับความเสี่ยง")
                print(f"   - 💼 เหมาะสำหรับการลงทุน")
            else:
                print(f"   - ⚠️  Sharpe Ratio < 1.0 = ควรพิจารณาความเสี่ยงอย่างรอบคอบ")
        else:
            print("\n❌ ไม่พบข้อมูลหรือ Ticker ไม่ถูกต้อง")
            print("💡 ตัวอย่าง Ticker: SPY, QQQ, AGG, GLD, VTI, BND")

    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("💡 กรุณาตรวจสอบว่า Stored Procedure ถูกติดตั้งแล้ว (รัน setup_procedures.py)")


def etf_performance_view(cursor):
    """Analytics #5: ETF Performance using SQL View"""
    print("\n" + "="*80)
    print("📈 Top 10 ETFs Performance (from SQL View)")
    print("="*80)
    print("📌 ใช้ SQL View: vw_etf_performance")
    print("="*80)

    query = """
    SELECT
        ticker_symbol,
        annualized_return_pct,
        annualized_volatility_pct,
        sharpe_ratio_approx
    FROM vw_etf_performance
    ORDER BY sharpe_ratio_approx DESC
    LIMIT 10
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print(f"\n{'Rank':<6} {'Ticker':<10} {'Return':<15} {'Volatility':<15} {'Sharpe Ratio':<15}")
            print("-"*80)

            for i, row in enumerate(rows, 1):
                ticker = row['ticker_symbol']
                ret = f"{row['annualized_return_pct']:.2f}%" if row['annualized_return_pct'] else 'N/A'
                vol = f"{row['annualized_volatility_pct']:.2f}%" if row['annualized_volatility_pct'] else 'N/A'
                sharpe = f"{row['sharpe_ratio_approx']:.4f}" if row['sharpe_ratio_approx'] else 'N/A'
                print(f"#{i:<5} {ticker:<10} {ret:<15} {vol:<15} {sharpe:<15}")

            print("\n💡 Actionable Insights:")
            print("   - ✅ ข้อมูลนี้คำนวณโดยใช้ SQL Window Functions (LAG, OVER)")
            print("   - ✅ ไม่ใช้ Python/pandas ในการคำนวณ")
            print("   - ✅ ตรงตามโจทย์อาจารย์ข้อ 3: ใช้ SQL เป็นเครื่องมือหลักในการวิเคราะห์")
        else:
            print("\n❌ ไม่พบข้อมูล")

    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("💡 กรุณาตรวจสอบว่า SQL View ถูกติดตั้งแล้ว (รัน setup_procedures.py)")


def main():
    """Main interactive loop"""
    # Show header
    print("\n" + "="*80)
    print("🎬 Portfolio Backtesting System - Live Demo")
    print("   DADS 4002 - Database Systems Project")
    print("="*80)

    # Connect to database
    db = DatabaseConnection()
    if not db.connect():
        print("\n❌ ไม่สามารถเชื่อมต่อ Database ได้")
        print("💡 กรุณาตรวจสอบว่า MySQL Server กำลังทำงานอยู่")
        return

    cursor = db.cursor

    # Get database statistics
    try:
        cursor.execute("SELECT COUNT(*) as total FROM etf_master")
        etf_count = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM benchmark_portfolios")
        portfolio_count = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as total FROM price_history")
        price_count = cursor.fetchone()['total']

        print(f"✅ Connected to MySQL successfully!")
        print(f"📊 Database: {MYSQL_CONFIG['database']}")
        print(f"\n📈 Database Statistics:")
        print(f"   - ETFs: {etf_count:,}")
        print(f"   - Portfolios: {portfolio_count:,}")
        print(f"   - Price History Records: {price_count:,}")
        print("\n💡 กรุณาเลือก Option 1-5 เพื่อ Demo Analytics Features")
        print("💡 เลือก 0 เพื่อออกจากโปรแกรม")
    except mysql.connector.Error as e:
        print(f"\n⚠️  Warning: {e}")

    # Main loop
    while True:
        try:
            show_menu()
            choice = input("\nเลือก Option (0-5): ").strip()

            if choice == '0':
                print("\n" + "="*80)
                print("🚪 ขอบคุณที่ใช้งาน Portfolio Backtesting System!")
                print("="*80)
                print("\n✅ สรุปการ Demo:")
                print("   - ใช้ SQL Stored Procedures ทั้งหมด (ตามโจทย์ข้อ 3)")
                print("   - มี Actionable Insights ในทุก Feature (ตามโจทย์ข้อ 5f)")
                print("   - ข้อมูลจริงจาก Yahoo Finance (ตามโจทย์ข้อ 4)")
                print("\n💼 ระบบหลักอยู่ที่: main.py (Integrated System)")
                print("\n👋 Goodbye!\n")
                break

            elif choice == '1':
                top_performers(cursor)

            elif choice == '2':
                portfolio_comparison(cursor)

            elif choice == '3':
                etf_correlation(cursor)

            elif choice == '4':
                sharpe_ratio_calculator(cursor)

            elif choice == '5':
                etf_performance_view(cursor)

            else:
                print("\n⚠️  กรุณาเลือก Option 0-5 เท่านั้น")

            input("\n⏎ กด Enter เพื่อกลับสู่ Menu...")

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n⏎ กด Enter เพื่อกลับสู่ Menu...")

    # Disconnect
    db.disconnect()
    print("✅ Database connection closed\n")


if __name__ == "__main__":
    main()
