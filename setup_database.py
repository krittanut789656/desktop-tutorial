"""
Setup MySQL Database for Portfolio Backtesting System
Creates database, tables, and imports initial data
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# MySQL Configuration
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456'
}

DATABASE_NAME = 'portfolio_backtesting'

def connect_to_mysql():
    """Connect to MySQL server (without database)"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print(f"✅ Connected to MySQL server at {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}")
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def create_database(cursor):
    """Create the portfolio_backtesting database"""
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
        print(f"🗑️  Dropped existing database '{DATABASE_NAME}' (if existed)")

        cursor.execute(f"CREATE DATABASE {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Created database '{DATABASE_NAME}'")

        cursor.execute(f"USE {DATABASE_NAME}")
        print(f"✅ Using database '{DATABASE_NAME}'")
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def read_sql_file(filepath):
    """Read SQL file and return content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading file {filepath}: {e}")
        return None

def execute_sql_statements(cursor, sql_content):
    """Execute SQL statements from file content"""
    # Split by semicolon but handle cases where semicolons might be in strings
    statements = []
    current_statement = []

    for line in sql_content.split('\n'):
        # Skip comments
        line = line.strip()
        if line.startswith('--') or line.startswith('#') or not line:
            continue

        current_statement.append(line)

        # If line ends with semicolon, it's end of statement
        if line.rstrip().endswith(';'):
            statement = ' '.join(current_statement)
            statements.append(statement)
            current_statement = []

    # Execute each statement
    executed = 0
    for statement in statements:
        statement = statement.strip()
        if not statement or statement.upper().startswith('USE '):
            continue

        try:
            cursor.execute(statement)
            executed += 1
        except Error as e:
            print(f"⚠️  Error executing statement: {e}")
            print(f"Statement: {statement[:100]}...")

    return executed

def create_tables(cursor, connection):
    """Create all tables from schema.sql"""
    print("\n📋 Creating tables...")

    schema_file = 'database/schema.sql'
    if not os.path.exists(schema_file):
        print(f"❌ Schema file not found: {schema_file}")
        return False

    sql_content = read_sql_file(schema_file)
    if not sql_content:
        return False

    # Remove database creation and USE statements from schema
    sql_lines = []
    for line in sql_content.split('\n'):
        if not (line.strip().startswith('CREATE DATABASE') or
                line.strip().startswith('USE ') or
                line.strip().startswith('DROP DATABASE')):
            sql_lines.append(line)

    sql_content = '\n'.join(sql_lines)

    executed = execute_sql_statements(cursor, sql_content)
    connection.commit()

    print(f"✅ Executed {executed} SQL statements")

    # Verify tables created
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📊 Created {len(tables)} tables:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   - {table_name}: {count} rows")

    return True

def import_etf_master(cursor, connection):
    """Import ETF master data"""
    print("\n📥 Importing ETF master data...")

    import csv

    etf_file = 'data/etf_list.csv'
    if not os.path.exists(etf_file):
        print(f"❌ ETF file not found: {etf_file}")
        return False

    with open(etf_file, 'r') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            try:
                cursor.execute("""
                    INSERT INTO etf_master
                    (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['ticker_symbol'],
                    row['etf_name'],
                    row['asset_class'],
                    row.get('region'),
                    row.get('sector'),
                    float(row['expense_ratio']) if row.get('expense_ratio') else None,
                    row.get('inception_date')
                ))
                count += 1
            except Error as e:
                print(f"⚠️  Error importing {row['ticker_symbol']}: {e}")

    connection.commit()
    print(f"✅ Imported {count} ETFs")
    return True

def import_benchmark_portfolios(cursor, connection):
    """Import benchmark portfolios"""
    print("\n📥 Importing benchmark portfolios...")

    import csv

    benchmark_file = 'data/benchmark_portfolios.csv'
    if not os.path.exists(benchmark_file):
        print(f"❌ Benchmark file not found: {benchmark_file}")
        return False

    with open(benchmark_file, 'r') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            try:
                cursor.execute("""
                    INSERT INTO benchmark_portfolios
                    (benchmark_name, description, risk_level, target_return, asset_allocation)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    row['benchmark_name'],
                    row.get('description'),
                    row.get('risk_level', 'Moderate'),
                    float(row['target_return']) if row.get('target_return') else None,
                    row.get('asset_allocation')
                ))
                count += 1
            except Error as e:
                print(f"⚠️  Error importing {row['benchmark_name']}: {e}")

    connection.commit()
    print(f"✅ Imported {count} benchmark portfolios")
    return True

def import_benchmark_holdings(cursor, connection):
    """Import benchmark holdings"""
    print("\n📥 Importing benchmark holdings...")

    import csv

    holdings_file = 'data/benchmark_holdings.csv'
    if not os.path.exists(holdings_file):
        print(f"❌ Holdings file not found: {holdings_file}")
        return False

    # First, get benchmark and ETF IDs
    cursor.execute("SELECT benchmark_id, benchmark_name FROM benchmark_portfolios")
    benchmark_map = {row[1]: row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {row[1]: row[0] for row in cursor.fetchall()}

    with open(holdings_file, 'r') as f:
        reader = csv.DictReader(f)
        count = 0

        for row in reader:
            try:
                benchmark_id = benchmark_map.get(row['benchmark_name'])
                etf_id = etf_map.get(row['ticker_symbol'])

                if not benchmark_id:
                    print(f"⚠️  Benchmark not found: {row['benchmark_name']}")
                    continue
                if not etf_id:
                    print(f"⚠️  ETF not found: {row['ticker_symbol']}")
                    continue

                cursor.execute("""
                    INSERT INTO benchmark_holdings
                    (benchmark_id, etf_id, target_weight)
                    VALUES (%s, %s, %s)
                """, (
                    benchmark_id,
                    etf_id,
                    float(row['target_weight'])
                ))
                count += 1
            except Error as e:
                print(f"⚠️  Error importing holding: {e}")

    connection.commit()
    print(f"✅ Imported {count} benchmark holdings")
    return True

def import_price_history(cursor, connection):
    """Import price history data"""
    print("\n📥 Importing price history (this may take a while)...")

    import csv

    price_file = 'data/etf_price_history.csv'
    if not os.path.exists(price_file):
        print(f"❌ Price history file not found: {price_file}")
        print("ℹ️  You can generate it by running: python scripts/generate_sample_data.py")
        return False

    # Get ETF ID mapping
    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {row[1]: row[0] for row in cursor.fetchall()}

    with open(price_file, 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        batch_size = 1000

        for row in reader:
            etf_id = etf_map.get(row['ticker_symbol'])
            if not etf_id:
                continue

            batch.append((
                etf_id,
                row['date'],
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                float(row['adj_close']),
                int(float(row['volume']))
            ))

            # Insert in batches for performance
            if len(batch) >= batch_size:
                try:
                    cursor.executemany("""
                        INSERT INTO price_history
                        (etf_id, date, open, high, low, close, adj_close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, batch)
                    connection.commit()
                    count += len(batch)
                    print(f"   Imported {count:,} price records...", end='\r')
                    batch = []
                except Error as e:
                    print(f"\n⚠️  Error importing batch: {e}")
                    batch = []

        # Insert remaining records
        if batch:
            try:
                cursor.executemany("""
                    INSERT INTO price_history
                    (etf_id, date, open, high, low, close, adj_close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, batch)
                connection.commit()
                count += len(batch)
            except Error as e:
                print(f"\n⚠️  Error importing final batch: {e}")

    print(f"\n✅ Imported {count:,} price records")
    return True

def main():
    """Main setup function"""
    print("=" * 70)
    print("Portfolio Backtesting System - Database Setup".center(70))
    print("=" * 70)

    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        sys.exit(1)

    cursor = connection.cursor()

    # Create database
    if not create_database(cursor):
        connection.close()
        sys.exit(1)

    # Create tables
    if not create_tables(cursor, connection):
        connection.close()
        sys.exit(1)

    # Import data
    import_etf_master(cursor, connection)
    import_benchmark_portfolios(cursor, connection)
    import_benchmark_holdings(cursor, connection)
    import_price_history(cursor, connection)

    # Final summary
    print("\n" + "=" * 70)
    print("DATABASE SETUP COMPLETE!".center(70))
    print("=" * 70)

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📊 Database: {DATABASE_NAME}")
    print(f"📋 Total Tables: {len(tables)}\n")

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   {table_name:30s} {count:>10,} rows")

    print("\n✅ Ready to run: python main.py")

    # Close connection
    cursor.close()
    connection.close()
    print("\n👋 Database connection closed")

if __name__ == "__main__":
    main()
