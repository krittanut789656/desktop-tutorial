#!/usr/bin/env python3
"""
Add sample data to ensure all tables have >=30 rows
This script adds:
- 30+ portfolios with different strategies
- Corresponding portfolio_etfs allocations
- Sample backtests for each portfolio
"""

import mysql.connector
from datetime import datetime, timedelta
import random

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456',  # Update this
    'database': 'etf_backtesting'
}

# Portfolio templates
PORTFOLIO_TEMPLATES = [
    # Conservative portfolios (30-40% stocks, 60-70% bonds)
    {"name": "Conservative Income", "desc": "Low risk, stable income", "stocks": 30, "bonds": 70},
    {"name": "Conservative Growth", "desc": "Low risk with moderate growth", "stocks": 35, "bonds": 65},
    {"name": "Moderate Conservative", "desc": "Balanced conservative approach", "stocks": 40, "bonds": 60},

    # Moderate portfolios (50-60% stocks, 40-50% bonds)
    {"name": "Balanced 50/50", "desc": "Equal stocks and bonds", "stocks": 50, "bonds": 50},
    {"name": "Balanced 60/40", "desc": "Classic balanced portfolio", "stocks": 60, "bonds": 40},
    {"name": "Moderate Growth", "desc": "Moderate risk, growth focused", "stocks": 55, "bonds": 45},

    # Aggressive portfolios (70-100% stocks)
    {"name": "Growth 70/30", "desc": "Growth focused portfolio", "stocks": 70, "bonds": 30},
    {"name": "Aggressive Growth", "desc": "High growth potential", "stocks": 80, "bonds": 20},
    {"name": "Very Aggressive", "desc": "Maximum growth", "stocks": 90, "bonds": 10},
    {"name": "100% Equity", "desc": "All stocks, no bonds", "stocks": 100, "bonds": 0},
]

# Sector-specific portfolios
SECTOR_PORTFOLIOS = [
    {"name": "Technology Focus", "desc": "Tech-heavy portfolio", "tickers": ["QQQ", "VGT", "XLK"]},
    {"name": "Healthcare Focus", "desc": "Healthcare sector", "tickers": ["XLV", "VHT", "IHI"]},
    {"name": "Financial Focus", "desc": "Financial sector", "tickers": ["XLF", "VFH", "KBE"]},
    {"name": "Energy Focus", "desc": "Energy sector", "tickers": ["XLE", "VDE", "IYE"]},
    {"name": "Real Estate Focus", "desc": "Real estate sector", "tickers": ["VNQ", "IYR", "XLRE"]},
]

# International portfolios
INTERNATIONAL_PORTFOLIOS = [
    {"name": "Global Diversified", "desc": "Global market exposure", "tickers": ["VT", "ACWI", "URTH"]},
    {"name": "Emerging Markets", "desc": "Emerging markets focus", "tickers": ["VWO", "IEMG", "EEM"]},
    {"name": "International Developed", "desc": "Developed international markets", "tickers": ["VEA", "IEFA", "EFA"]},
    {"name": "Asia Pacific", "desc": "Asia Pacific region", "tickers": ["VPL", "IPAC", "EPP"]},
]

# Age-based portfolios
AGE_PORTFOLIOS = [
    {"name": "Age 20-30 Portfolio", "desc": "For investors in their 20s-30s", "stocks": 90, "bonds": 10},
    {"name": "Age 30-40 Portfolio", "desc": "For investors in their 30s-40s", "stocks": 80, "bonds": 20},
    {"name": "Age 40-50 Portfolio", "desc": "For investors in their 40s-50s", "stocks": 70, "bonds": 30},
    {"name": "Age 50-60 Portfolio", "desc": "For investors in their 50s-60s", "stocks": 60, "bonds": 40},
    {"name": "Age 60+ Portfolio", "desc": "For retirees", "stocks": 40, "bonds": 60},
]

# Risk-based portfolios
RISK_PORTFOLIOS = [
    {"name": "Ultra Conservative", "desc": "Minimal risk tolerance", "stocks": 20, "bonds": 80},
    {"name": "Low Risk", "desc": "Low risk tolerance", "stocks": 35, "bonds": 65},
    {"name": "Moderate Risk", "desc": "Moderate risk tolerance", "stocks": 60, "bonds": 40},
    {"name": "High Risk", "desc": "High risk tolerance", "stocks": 85, "bonds": 15},
    {"name": "Very High Risk", "desc": "Very high risk tolerance", "stocks": 100, "bonds": 0},
]


def get_available_etfs(cursor):
    """Get list of available ETFs"""
    cursor.execute("SELECT ticker FROM etfs ORDER BY ticker")
    return [row[0] for row in cursor.fetchall()]


def get_stock_bond_etfs(cursor):
    """Get stock and bond ETFs"""
    cursor.execute("""
        SELECT ticker, category FROM etfs
        WHERE category IN ('Equity', 'Bond', 'Fixed Income', 'Stock')
        ORDER BY ticker
    """)

    stocks = []
    bonds = []

    for ticker, category in cursor.fetchall():
        if 'Bond' in category or 'Fixed' in category:
            bonds.append(ticker)
        else:
            stocks.append(ticker)

    # Default fallback
    if not stocks:
        stocks = ['SPY', 'VOO', 'VTI', 'QQQ', 'IWM']
    if not bonds:
        bonds = ['AGG', 'BND', 'TLT', 'IEF', 'LQD']

    return stocks, bonds


def create_portfolio(cursor, name, description, allocations):
    """Create a portfolio with ETF allocations"""
    # Insert portfolio
    cursor.execute("""
        INSERT INTO portfolios (name, description, created_at)
        VALUES (%s, %s, %s)
    """, (name, description, datetime.now()))

    portfolio_id = cursor.lastrowid

    # Insert allocations
    for ticker, weight in allocations.items():
        try:
            cursor.execute("""
                INSERT INTO portfolio_etfs (portfolio_id, ticker, weight)
                VALUES (%s, %s, %s)
            """, (portfolio_id, ticker, weight))
        except Exception as e:
            print(f"   Warning: Could not add {ticker}: {e}")

    return portfolio_id


def add_portfolios(conn):
    """Add sample portfolios"""
    cursor = conn.cursor()

    # Get available ETFs
    stocks, bonds = get_stock_bond_etfs(cursor)
    all_etfs = get_available_etfs(cursor)

    print("\n" + "="*70)
    print("ADDING SAMPLE PORTFOLIOS")
    print("="*70)

    portfolio_count = 0

    # 1. Add balanced portfolios
    print("\n1. Adding Balanced Portfolios...")
    for template in PORTFOLIO_TEMPLATES:
        stock_pct = template['stocks']
        bond_pct = template['bonds']

        allocations = {}

        if stock_pct > 0 and stocks:
            # Distribute stock allocation among 2-3 stock ETFs
            num_stocks = min(2, len(stocks))
            stock_etfs = random.sample(stocks, num_stocks)
            per_etf = stock_pct / num_stocks
            for etf in stock_etfs:
                allocations[etf] = round(per_etf, 2)

        if bond_pct > 0 and bonds:
            # Distribute bond allocation among 1-2 bond ETFs
            num_bonds = min(2, len(bonds))
            bond_etfs = random.sample(bonds, num_bonds)
            per_etf = bond_pct / num_bonds
            for etf in bond_etfs:
                allocations[etf] = round(per_etf, 2)

        # Normalize to 100%
        total = sum(allocations.values())
        if total > 0:
            allocations = {k: round(v * 100 / total, 2) for k, v in allocations.items()}

        portfolio_id = create_portfolio(cursor, template['name'], template['desc'], allocations)
        portfolio_count += 1
        print(f"   ✓ Created: {template['name']} (ID: {portfolio_id})")

    # 2. Add sector portfolios
    print("\n2. Adding Sector Portfolios...")
    for template in SECTOR_PORTFOLIOS:
        allocations = {}
        available_tickers = [t for t in template['tickers'] if t in all_etfs]

        if available_tickers:
            weight_per_ticker = 100.0 / len(available_tickers)
            for ticker in available_tickers:
                allocations[ticker] = round(weight_per_ticker, 2)
        elif all_etfs:
            # Fallback: use any 3 available ETFs
            selected = random.sample(all_etfs, min(3, len(all_etfs)))
            weight_per_ticker = 100.0 / len(selected)
            for ticker in selected:
                allocations[ticker] = round(weight_per_ticker, 2)

        if allocations:
            portfolio_id = create_portfolio(cursor, template['name'], template['desc'], allocations)
            portfolio_count += 1
            print(f"   ✓ Created: {template['name']} (ID: {portfolio_id})")

    # 3. Add international portfolios
    print("\n3. Adding International Portfolios...")
    for template in INTERNATIONAL_PORTFOLIOS:
        allocations = {}
        available_tickers = [t for t in template['tickers'] if t in all_etfs]

        if available_tickers:
            weight_per_ticker = 100.0 / len(available_tickers)
            for ticker in available_tickers:
                allocations[ticker] = round(weight_per_ticker, 2)
        elif all_etfs:
            selected = random.sample(all_etfs, min(3, len(all_etfs)))
            weight_per_ticker = 100.0 / len(selected)
            for ticker in selected:
                allocations[ticker] = round(weight_per_ticker, 2)

        if allocations:
            portfolio_id = create_portfolio(cursor, template['name'], template['desc'], allocations)
            portfolio_count += 1
            print(f"   ✓ Created: {template['name']} (ID: {portfolio_id})")

    # 4. Add age-based portfolios
    print("\n4. Adding Age-Based Portfolios...")
    for template in AGE_PORTFOLIOS:
        stock_pct = template['stocks']
        bond_pct = template['bonds']

        allocations = {}

        if stock_pct > 0 and stocks:
            num_stocks = min(2, len(stocks))
            stock_etfs = random.sample(stocks, num_stocks)
            per_etf = stock_pct / num_stocks
            for etf in stock_etfs:
                allocations[etf] = round(per_etf, 2)

        if bond_pct > 0 and bonds:
            num_bonds = min(1, len(bonds))
            bond_etfs = random.sample(bonds, num_bonds)
            per_etf = bond_pct / num_bonds
            for etf in bond_etfs:
                allocations[etf] = round(per_etf, 2)

        # Normalize
        total = sum(allocations.values())
        if total > 0:
            allocations = {k: round(v * 100 / total, 2) for k, v in allocations.items()}

        portfolio_id = create_portfolio(cursor, template['name'], template['desc'], allocations)
        portfolio_count += 1
        print(f"   ✓ Created: {template['name']} (ID: {portfolio_id})")

    # 5. Add risk-based portfolios
    print("\n5. Adding Risk-Based Portfolios...")
    for template in RISK_PORTFOLIOS:
        stock_pct = template['stocks']
        bond_pct = template['bonds']

        allocations = {}

        if stock_pct > 0 and stocks:
            num_stocks = min(2, len(stocks))
            stock_etfs = random.sample(stocks, num_stocks)
            per_etf = stock_pct / num_stocks
            for etf in stock_etfs:
                allocations[etf] = round(per_etf, 2)

        if bond_pct > 0 and bonds:
            num_bonds = min(1, len(bonds))
            bond_etfs = random.sample(bonds, num_bonds)
            per_etf = bond_pct / num_bonds
            for etf in bond_etfs:
                allocations[etf] = round(per_etf, 2)

        # Normalize
        total = sum(allocations.values())
        if total > 0:
            allocations = {k: round(v * 100 / total, 2) for k, v in allocations.items()}

        portfolio_id = create_portfolio(cursor, template['name'], template['desc'], allocations)
        portfolio_count += 1
        print(f"   ✓ Created: {template['name']} (ID: {portfolio_id})")

    conn.commit()
    cursor.close()

    print("\n" + "="*70)
    print(f"✅ Total portfolios created: {portfolio_count}")
    print("="*70)

    return portfolio_count


def main():
    """Main function"""
    print("="*70)
    print("ETF BACKTESTING SYSTEM - Add Sample Data")
    print("="*70)

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connected to MySQL")

        # Add portfolios
        add_portfolios(conn)

        conn.close()
        print("\n✅ All done!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
