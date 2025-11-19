#!/usr/bin/env python3
"""
Setup SQL Stored Procedures and Views
อ่านไฟล์ database/stored_procedures.sql และรันใน MySQL
"""

import mysql.connector
import os

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krittanut123456',
    'database': 'portfolio_backtesting'
}

def run_sql_file(filepath):
    """อ่านและรัน SQL file"""
    try:
        # เชื่อมต่อ MySQL
        print("🔌 กำลังเชื่อมต่อ MySQL...")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # อ่านไฟล์ SQL
        print(f"📖 กำลังอ่านไฟล์: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # แยก SQL statements โดยใช้ delimiter
        print("⚙️  กำลังประมวลผล SQL statements...")

        # Split by DELIMITER and process
        statements = []
        current_delimiter = ';'
        buffer = ''

        for line in sql_content.split('\n'):
            line = line.strip()

            # ข้าม comments
            if line.startswith('--') or not line:
                continue

            # เช็ค DELIMITER change
            if line.upper().startswith('DELIMITER'):
                if '//(' in line:
                    current_delimiter = ';'
                elif '//' in line:
                    current_delimiter = '//'
                else:
                    current_delimiter = ';'
                continue

            buffer += line + ' '

            # ถ้าจบ statement ด้วย current delimiter
            if line.endswith(current_delimiter):
                # ลบ delimiter ออก
                stmt = buffer.rstrip(current_delimiter).strip()
                if stmt:
                    statements.append(stmt)
                buffer = ''

        # รัน statements
        success_count = 0
        error_count = 0

        for i, stmt in enumerate(statements, 1):
            try:
                # ข้าม USE database statement
                if stmt.upper().startswith('USE '):
                    continue

                cursor.execute(stmt)
                success_count += 1

                # แสดงความคืบหน้า
                if 'CREATE VIEW' in stmt.upper():
                    view_name = stmt.split('VIEW')[1].split('AS')[0].strip().split()[0]
                    print(f"  ✅ สร้าง View: {view_name}")
                elif 'CREATE PROCEDURE' in stmt.upper():
                    proc_name = stmt.split('PROCEDURE')[1].split('(')[0].strip()
                    print(f"  ✅ สร้าง Procedure: {proc_name}")
                elif 'DROP VIEW' in stmt.upper():
                    view_name = stmt.split('VIEW')[1].split('IF EXISTS')[1].strip().rstrip(';')
                    print(f"  🗑️  Drop View: {view_name}")
                elif 'DROP PROCEDURE' in stmt.upper():
                    proc_name = stmt.split('PROCEDURE')[1].split('IF EXISTS')[1].strip().rstrip(';')
                    print(f"  🗑️  Drop Procedure: {proc_name}")

            except mysql.connector.Error as e:
                error_count += 1
                print(f"  ❌ Error in statement {i}: {e}")
                # ไม่ break เพื่อให้ลอง execute ต่อ

        conn.commit()

        # สรุปผลลัพธ์
        print("\n" + "="*60)
        print("📊 สรุปผลการติดตั้ง SQL Stored Procedures & Views")
        print("="*60)
        print(f"✅ สำเร็จ: {success_count} statements")
        print(f"❌ ล้มเหลว: {error_count} statements")

        # ตรวจสอบ Views และ Procedures ที่สร้างขึ้น
        print("\n📋 Views ที่สร้างแล้ว:")
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        for view in views:
            print(f"  ✓ {view[0]}")

        print("\n📋 Stored Procedures ที่สร้างแล้ว:")
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'portfolio_backtesting'")
        procedures = cursor.fetchall()
        for proc in procedures:
            print(f"  ✓ {proc[1]}")

        cursor.close()
        conn.close()

        print("\n✅ ติดตั้งเสร็จสมบูรณ์!")
        return True

    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    sql_file = "database/stored_procedures.sql"

    print("="*60)
    print("🚀 ติดตั้ง SQL Stored Procedures & Views")
    print("="*60)
    print()

    if run_sql_file(sql_file):
        print("\n🎉 พร้อมใช้งาน! ตอนนี้สามารถรัน python main.py ได้แล้ว")
    else:
        print("\n⚠️  เกิดข้อผิดพลาด กรุณาตรวจสอบและลองใหม่")
