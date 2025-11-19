#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import Mini Price History - Portfolio Backtesting System
รัน: python import_mini_price_history.py
"""

import mysql.connector
import pandas as pd
from datetime import datetime
import sys
import os
from pathlib import Path

# ========================================
# หา path ของ script และเปลี่ยน working directory
# ========================================
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

print("=" * 70)
print("📥 Import Mini Price History (756 rows)".center(70))
print("=" * 70)
print(f"\n📁 Script directory: {SCRIPT_DIR}")
print(f"📁 Working directory: {Path.cwd()}\n")

# ========================================
# ตั้งค่า MySQL
# ========================================
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456',  # แก้ไขถ้าต้องการ
    'database': 'portfolio_backtesting'
}

print(f"MySQL: {MYSQL_CONFIG['user']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}\n")

# ========================================
# เชื่อมต่อ MySQL
# ========================================
print("🔌 เชื่อมต่อ MySQL...")
try:
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    print("✅ เชื่อมต่อสำเร็จ\n")
except mysql.connector.Error as e:
    print(f"❌ Error: {e}\n")
    sys.exit(1)

# ========================================
# ตรวจสอบว่ามี ETF แล้ว
# ========================================
print("📋 ตรวจสอบข้อมูล ETF...")
cursor.execute("SELECT COUNT(*) as cnt FROM etf_master")
etf_count = cursor.fetchone()['cnt']

if etf_count == 0:
    print("❌ ไม่มีข้อมูล ETF ในตาราง etf_master")
    print("💡 กรุณารัน IMPORT_MINI_DATA.sql ก่อน")
    sys.exit(1)

print(f"✅ พบ {etf_count} ETFs\n")

# Get ETF mapping
cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
etf_map = {r['ticker_symbol']: r['etf_id'] for r in cursor.fetchall()}
print(f"📋 สร้าง mapping: {len(etf_map)} tickers → IDs")
for ticker, etf_id in etf_map.items():
    print(f"   {ticker} → etf_id = {etf_id}")
print()

# ========================================
# Import Price History
# ========================================
start_time = datetime.now()
print("\n" + "=" * 70)
print("📊 Import Mini Price History...")
print("=" * 70)

try:
    # อ่านไฟล์
    print("\n📁 อ่านไฟล์ CSV...")
    csv_path = SCRIPT_DIR / 'data' / 'mini_price_history.csv'

    if not csv_path.exists():
        print(f"\n❌ Error: ไม่พบไฟล์ {csv_path}")
        print(f"\n💡 รัน generate_mini_price_history.py ก่อน")
        sys.exit(1)

    df_price = pd.read_csv(csv_path)
    print(f"   ✅ อ่านได้ {len(df_price):,} rows จาก {csv_path.name}")

    # แปลง ticker → etf_id
    print("🔄 แปลง ticker → etf_id...")
    df_price['etf_id'] = df_price['ticker'].map(etf_map)
    df_price = df_price.dropna(subset=['etf_id'])
    print(f"   ✅ แปลงแล้ว {len(df_price):,} rows\n")

    # Import ทั้งหมด (ไม่ต้อง batch เพราะน้อย)
    print("📥 กำลัง Import...")

    data = [
        (
            int(row['etf_id']),
            row['date'],
            float(row['open']),
            float(row['high']),
            float(row['low']),
            float(row['close']),
            int(row['volume'])
        )
        for _, row in df_price.iterrows()
    ]

    cursor.executemany("""
        INSERT INTO price_history
        (etf_id, price_date, open_price, high_price, low_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, data)

    conn.commit()

    print(f"   ✅ Import เสร็จ: {len(data):,} rows")

    # ========================================
    # สรุปผลลัพธ์
    # ========================================
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "=" * 70)
    print("🎉 Import เสร็จสมบูรณ์!".center(70))
    print("=" * 70)
    print(f"\n⏱️  ใช้เวลา: {elapsed:.1f} วินาที")
    print(f"📦 Import: {len(data):,} rows")

    # ตรวจสอบ
    print("\n📊 ตรวจสอบข้อมูลทั้งหมด:")
    cursor.execute("SELECT COUNT(*) as cnt FROM price_history")
    final_count = cursor.fetchone()['cnt']
    print(f"   ✅ price_history: {final_count:,} rows")

    # Sample data
    print("\n📋 ตัวอย่างข้อมูล (5 rows ล่าสุด):")
    cursor.execute("""
        SELECT e.ticker_symbol, ph.price_date, ph.close_price, ph.volume
        FROM price_history ph
        JOIN etf_master e ON ph.etf_id = e.etf_id
        ORDER BY ph.price_date DESC
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(f"   {row['ticker_symbol']:5s} | {row['price_date']} | ${row['close_price']:8.2f} | Vol: {row['volume']:,}")

    print("\n" + "=" * 70)
    print("✅ ทุกอย่างเสร็จสมบูรณ์!".center(70))
    print("=" * 70)
    print("\n🎉 พร้อมทดสอบระบบ! เปิด test_mini_backtest.ipynb ได้เลย\n")

except Exception as e:
    print(f"\n\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("✅ ปิดการเชื่อมต่อ MySQL แล้ว\n")
