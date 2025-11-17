"""
Quick Test Script for ETF Data Collection
Tests with a small number of ETFs to verify everything is working
"""

from data_collection import ETFDataCollector
import sys

def main():
    """Run a quick test with a few ETFs"""
    print("="*80)
    print("QUICK TEST - ETF DATA COLLECTION")
    print("="*80)
    print("\nThis script will test data collection with just 3 ETFs:")
    print("  - SPY (US Large Cap)")
    print("  - AGG (Bonds)")
    print("  - GLD (Commodities)")
    print("\nThis should complete in 1-2 minutes.")
    print("="*80)

    response = input("\nProceed with test? (y/n): ").strip().lower()

    if response != 'y':
        print("Test cancelled.")
        return

    # Test tickers
    test_tickers = ['SPY', 'AGG', 'GLD']

    print(f"\nStarting test collection for {len(test_tickers)} ETFs...")
    print("="*80)

    # Create collector
    collector = ETFDataCollector()

    # Collect data
    collector.collect_all_data(tickers=test_tickers)

    # Generate report
    collector.generate_summary_report()

    print("\n" + "="*80)
    print("TEST COMPLETED!")
    print("="*80)
    print("\nCheck the following files:")
    print("  - data_import.log (detailed logs)")
    print("  - data_summary.txt (summary report)")
    print("\nYou can also check the database:")
    print("  SELECT ticker, COUNT(*) FROM daily_prices WHERE ticker IN ('SPY','AGG','GLD') GROUP BY ticker;")
    print("="*80)

if __name__ == '__main__':
    main()
