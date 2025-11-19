#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import Weekly Price History - Portfolio Backtesting System
ข้อมูลจริงจาก Yahoo Finance (แปลงเป็น Weekly)
รัน: python import_weekly_price_history.py
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
print("📥 Import Weekly Price History (41,800 rows)".center(70))
print("=" * 70)
print(f"\n📁 Working directory: {Path.cwd()}")
print("📊 Data source: Yahoo Finance (converted to weekly)")
print()

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
    print("💡 กรุณาตรวจสอบ:")
    print("   1. MySQL server ทำงานอยู่หรือไม่?")
    print("   2. Password ถูกต้องหรือไม่?")
    print("   3. Database 'portfolio_backtesting' มีอยู่หรือไม่?")
    sys.exit(1)

# ========================================
# ตรวจสอบว่ามี ETF แล้ว
# ========================================
print("📋 ตรวจสอบข้อมูล ETF...")
cursor.execute("SELECT COUNT(*) as cnt FROM etf_master")
etf_count = cursor.fetchone()['cnt']

if etf_count == 0:
    print("❌ ไม่มีข้อมูล ETF ในตาราง etf_master")
    print("💡 กรุณารัน IMPORT_ALL_DATA.sql ก่อน")
    sys.exit(1)

print(f"✅ พบ {etf_count} ETFs\n")

# Get ETF mapping
cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master ORDER BY ticker_symbol")
etf_map = {r['ticker_symbol']: r['etf_id'] for r in cursor.fetchall()}
print(f"📋 สร้าง mapping: {len(etf_map)} tickers → IDs\n")

# ========================================
# เช็คว่ามีข้อมูล price_history อยู่แล้วหรือไม่
# ========================================
cursor.execute("SELECT COUNT(*) as cnt FROM price_history")
existing_count = cursor.fetchone()['cnt']

if existing_count > 0:
    print(f"⚠️  พบข้อมูล {existing_count:,} rows อยู่แล้วใน price_history")
    print("\n💡 ต้องการลบและ import ใหม่หรือไม่?")
    print("   y = ลบข้อมูลเก่าและ import ใหม่")
    print("   n = ยกเลิกการ import")
    confirm = input("\nตอบ (y/n) [n]: ").strip().lower()

    if confirm == 'y':
        print("\n🗑️  ลบข้อมูลเก่า...")
        cursor.execute("TRUNCATE TABLE price_history")
        conn.commit()
        print("✅ ลบเสร็จแล้ว\n")
    else:
        print("❌ ยกเลิกการ import")
        sys.exit(0)

# ========================================
# Import Weekly Price History
# ========================================
start_time = datetime.now()
print("\n" + "=" * 70)
print("📊 Import Weekly Price History...")
print("=" * 70)

try:
    # อ่านไฟล์
    print("\n📁 อ่านไฟล์ CSV...")
    csv_path = SCRIPT_DIR / 'data' / 'etf_price_history_weekly.csv'

    if not csv_path.exists():
        print(f"\n❌ Error: ไม่พบไฟล์ {csv_path}")
        print(f"\n💡 รัน convert_daily_to_weekly.py ก่อน")
        sys.exit(1)

    df_price = pd.read_csv(csv_path)
    print(f"   ✅ อ่านได้ {len(df_price):,} rows จาก {csv_path.name}")

    # แปลง ticker → etf_id
    print("🔄 แปลง ticker → etf_id...")
    df_price['etf_id'] = df_price['ticker'].map(etf_map)
    df_price = df_price.dropna(subset=['etf_id'])
    print(f"   ✅ แปลงแล้ว {len(df_price):,} rows\n")

    # Import เป็น batch
    batch_size = 5000
    total_batches = (len(df_price) + batch_size - 1) // batch_size
    imported = 0

    print(f"📥 กำลัง Import ({total_batches} batches)...\n")

    for i in range(0, len(df_price), batch_size):
        batch = df_price.iloc[i:i+batch_size]

        # Prepare data
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
            for _, row in batch.iterrows()
        ]

        # Batch insert
        cursor.executemany("""
            INSERT INTO price_history
            (etf_id, price_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, data)

        conn.commit()

        imported += len(batch)
        current_batch = i // batch_size + 1
        percent = (imported / len(df_price)) * 100

        # Progress bar
        bar_length = 40
        filled = int(bar_length * imported / len(df_price))
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"   [{bar}] {percent:5.1f}% | {imported:,}/{len(df_price):,} rows | Batch {current_batch}/{total_batches}", end='\r')

    print()  # New line after progress

    # ========================================
    # สรุปผลลัพธ์
    # ========================================
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "=" * 70)
    print("🎉 Import เสร็จสมบูรณ์!".center(70))
    print("=" * 70)
    print(f"\n⏱️  ใช้เวลา: {elapsed:.1f} วินาที ({elapsed/60:.1f} นาที)")
    print(f"📦 Import: {imported:,} rows")
    print(f"📊 Data type: Weekly price history from Yahoo Finance")

    # ตรวจสอบ
    print("\n📊 ตรวจสอบข้อมูล:")
    cursor.execute("SELECT COUNT(*) as cnt FROM price_history")
    final_count = cursor.fetchone()['cnt']
    print(f"   ✅ price_history: {final_count:,} rows")

    # Show data range
    cursor.execute("""
        SELECT
            MIN(price_date) as min_date,
            MAX(price_date) as max_date,
            COUNT(DISTINCT etf_id) as etf_count
        FROM price_history
    """)
    stats = cursor.fetchone()
    print(f"   ✅ Date range: {stats['min_date']} to {stats['max_date']}")
    print(f"   ✅ ETFs: {stats['etf_count']}")

    # Sample data
    print("\n📋 ตัวอย่างข้อมูล (5 rows ล่าสุด):")
    cursor.execute("""
        SELECT e.ticker_symbol, ph.price_date, ph.close_price, ph.volume
        FROM price_history ph
        JOIN etf_master e ON ph.etf_id = e.etf_id
        ORDER BY ph.price_date DESC, e.ticker_symbol
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(f"   {row['ticker_symbol']:5s} | {row['price_date']} | ${row['close_price']:8.2f} | Vol: {row['volume']:,}")

    print("\n" + "=" * 70)
    print("✅ ทุกอย่างเสร็จสมบูรณ์!".center(70))
    print("=" * 70)
    print("\n🎉 พร้อมใช้งาน! เปิด main.ipynb หรือ analytics.ipynb ได้เลย\n")

except mysql.connector.IntegrityError as e:
    print(f"\n\n⚠️  IntegrityError: {e}\n")
    print("💡 มีข้อมูลอยู่แล้ว! รัน script นี้อีกครั้งแล้วเลือก 'y' เพื่อลบข้อมูลเก่า")

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
