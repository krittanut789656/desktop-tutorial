"""
Generate Sample ETF Data for Testing
Create realistic sample data based on historical patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_etf_price_series(ticker, start_date, end_date, initial_price, annual_return, annual_vol):
    """
    Generate realistic price series using geometric Brownian motion

    Args:
        ticker: ETF ticker symbol
        start_date: Start date
        end_date: End date
        initial_price: Starting price
        annual_return: Expected annual return (e.g., 0.10 for 10%)
        annual_vol: Annual volatility (e.g., 0.20 for 20%)
    """
    # Generate dates (trading days only - approximately 252/year)
    date_range = pd.bdate_range(start=start_date, end=end_date)

    # Parameters
    dt = 1/252  # Daily time step
    mu = annual_return  # Drift
    sigma = annual_vol  # Volatility

    # Generate random returns
    np.random.seed(hash(ticker) % 2**32)  # Reproducible but different per ticker
    returns = np.random.normal(mu * dt, sigma * np.sqrt(dt), len(date_range))

    # Calculate cumulative returns and prices
    price_multipliers = np.exp(np.cumsum(returns))
    close_prices = initial_price * price_multipliers

    # Generate OHLC data
    # Open: previous close with small random movement
    open_prices = np.roll(close_prices, 1)
    open_prices[0] = initial_price
    open_prices = open_prices * (1 + np.random.uniform(-0.002, 0.002, len(date_range)))

    # High/Low: based on daily volatility
    daily_range = close_prices * np.random.uniform(0.01, 0.03, len(date_range))
    high_prices = np.maximum(open_prices, close_prices) + daily_range * np.random.uniform(0, 0.5, len(date_range))
    low_prices = np.minimum(open_prices, close_prices) - daily_range * np.random.uniform(0, 0.5, len(date_range))

    # Volume: realistic volume based on price
    base_volume = 1000000 * (initial_price / 100)
    volume = base_volume * (1 + np.random.uniform(-0.5, 0.5, len(date_range)))
    volume = volume.astype(int)

    # Adjusted close (same as close for simplicity, in reality accounts for splits/dividends)
    adj_close_prices = close_prices

    # Create DataFrame
    df = pd.DataFrame({
        'ticker': ticker,
        'date': date_range,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'adj_close': adj_close_prices,
        'volume': volume
    })

    return df


def generate_all_sample_data():
    """Generate sample data for all 50 ETFs"""

    # ETF characteristics (ticker, initial_price, annual_return, annual_volatility)
    etf_params = [
        # US Equity - Large Cap
        ('SPY', 90, 0.12, 0.18),
        ('VOO', 60, 0.12, 0.18),
        ('VTI', 45, 0.12, 0.19),
        ('QQQ', 40, 0.18, 0.25),
        ('IWM', 50, 0.10, 0.24),
        ('DIA', 80, 0.11, 0.17),
        ('VUG', 45, 0.14, 0.20),
        ('VTV', 40, 0.10, 0.16),
        ('IVV', 90, 0.12, 0.18),

        # International Equity
        ('VEA', 35, 0.07, 0.20),
        ('VWO', 40, 0.04, 0.24),
        ('EFA', 50, 0.06, 0.19),
        ('IEMG', 45, 0.04, 0.23),
        ('EEM', 35, 0.03, 0.25),
        ('IXUS', 40, 0.07, 0.20),

        # Bonds
        ('AGG', 100, 0.03, 0.04),
        ('BND', 75, 0.03, 0.04),
        ('TLT', 90, 0.04, 0.15),
        ('IEF', 100, 0.03, 0.07),
        ('SHY', 84, 0.02, 0.02),
        ('LQD', 110, 0.04, 0.06),
        ('TIP', 100, 0.03, 0.05),
        ('HYG', 85, 0.05, 0.08),
        ('MUB', 105, 0.03, 0.04),
        ('BNDX', 50, 0.02, 0.05),

        # Commodities
        ('GLD', 100, 0.06, 0.16),
        ('SLV', 15, 0.04, 0.30),
        ('DBC', 20, 0.02, 0.20),
        ('USO', 35, -0.02, 0.35),
        ('UNG', 25, -0.05, 0.50),

        # REITs
        ('VNQ', 60, 0.09, 0.22),
        ('IYR', 65, 0.08, 0.23),
        ('VNQI', 45, 0.06, 0.20),

        # Sector ETFs
        ('XLK', 20, 0.16, 0.22),
        ('XLF', 18, 0.11, 0.21),
        ('XLV', 22, 0.13, 0.15),
        ('XLE', 45, 0.05, 0.28),
        ('XLI', 30, 0.11, 0.19),
        ('XLP', 35, 0.10, 0.14),
        ('XLY', 28, 0.14, 0.20),
        ('XLU', 38, 0.08, 0.14),
        ('XLRE', 30, 0.09, 0.22),
        ('XLB', 35, 0.09, 0.20),
        ('VGT', 45, 0.17, 0.23),
        ('VHT', 55, 0.14, 0.16),
        ('VFH', 40, 0.10, 0.22),
        ('VDE', 65, 0.04, 0.30),
        ('VIS', 50, 0.11, 0.19),
        ('VDC', 45, 0.10, 0.13),
        ('VAW', 50, 0.08, 0.21),
    ]

    print(f"\n{'='*60}")
    print(f"Generating Sample ETF Data")
    print(f"{'='*60}\n")

    # Date range
    start_date = '2009-01-01'
    end_date = '2024-12-31'

    all_data = []

    for ticker, initial_price, annual_return, annual_vol in etf_params:
        print(f"Generating {ticker}...", end=" ")

        df = generate_etf_price_series(
            ticker, start_date, end_date,
            initial_price, annual_return, annual_vol
        )

        all_data.append(df)
        print(f"✅ {len(df)} rows")

    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)

    # Save to CSV
    output_dir = '../data'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'etf_price_history.csv')
    combined_data.to_csv(output_file, index=False)

    print(f"\n{'='*60}")
    print(f"GENERATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total ETFs: {len(etf_params)}")
    print(f"Total rows: {len(combined_data):,}")
    print(f"Date range: {combined_data['date'].min()} to {combined_data['date'].max()}")
    print(f"Output file: {output_file}")
    print(f"{'='*60}\n")

    # Save individual files
    etf_dir = os.path.join(output_dir, 'individual_etfs')
    os.makedirs(etf_dir, exist_ok=True)

    for ticker in combined_data['ticker'].unique():
        etf_data = combined_data[combined_data['ticker'] == ticker]
        etf_file = os.path.join(etf_dir, f'{ticker}.csv')
        etf_data.to_csv(etf_file, index=False)

    print(f"✅ Saved individual ETF files to {etf_dir}\n")

    # Show sample
    print("Sample data (first 10 rows):")
    print(combined_data.head(10).to_string(index=False))
    print("\n")

    # Statistics
    print(f"{'='*60}")
    print(f"STATISTICS BY ETF")
    print(f"{'='*60}\n")

    stats = combined_data.groupby('ticker').agg({
        'date': ['min', 'max', 'count'],
        'close': ['first', 'last']
    }).reset_index()

    stats.columns = ['Ticker', 'Start Date', 'End Date', 'Rows', 'Start Price', 'End Price']
    stats['Total Return %'] = ((stats['End Price'] / stats['Start Price'] - 1) * 100).round(2)

    print(stats.to_string(index=False))
    print(f"\n{'='*60}\n")

    return combined_data


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║       Sample ETF Data Generator                           ║
    ║                                                            ║
    ║  Creating realistic sample data for 50 ETFs               ║
    ║  Period: 2009-01-01 to 2024-12-31                         ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    data = generate_all_sample_data()

    print("✅ Sample data generation completed!")
    print("\nNote: This is simulated data for testing purposes.")
    print("For real data, run the download script on your local machine with yfinance installed.")
