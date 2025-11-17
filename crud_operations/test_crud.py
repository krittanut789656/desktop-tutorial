"""
Test Script for CRUD Operations Module
Demonstrates usage of all CRUD functions

Run this script to test the CRUD operations module
"""

import json
from crud_operations import (
    # Portfolio functions
    create_portfolio,
    read_portfolio,
    update_portfolio_weights,
    delete_portfolio,
    # ETF functions
    add_etf,
    get_etf_info,
    update_etf_prices,
    delete_etf,
    # Backtest functions
    list_backtests,
    delete_backtest,
    # Utility functions
    get_database_stats
)


def print_result(title, result):
    """Pretty print result"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    if 'data' in result and result['data']:
        print("\nData:")
        print(json.dumps(result['data'], indent=2, default=str))
    if 'portfolio_id' in result:
        print(f"Portfolio ID: {result['portfolio_id']}")
    if 'records_added' in result:
        print(f"Records Added: {result['records_added']}")
    print("="*80)


def test_portfolio_operations():
    """Test portfolio CRUD operations"""
    print("\n" + "#"*80)
    print("# TESTING PORTFOLIO OPERATIONS")
    print("#"*80)

    # Test 1: Create Portfolio
    print("\n[TEST 1] Creating a new portfolio...")
    result = create_portfolio(
        name="Test Portfolio 60/40",
        description="Balanced portfolio for testing",
        etf_list=["SPY", "AGG"],
        weights=[60.0, 40.0],
        user_id=1
    )
    print_result("Create Portfolio", result)
    test_portfolio_id = result.get('portfolio_id')

    # Test 2: Read Single Portfolio
    if test_portfolio_id:
        print("\n[TEST 2] Reading the created portfolio...")
        result = read_portfolio(portfolio_id=test_portfolio_id)
        print_result(f"Read Portfolio {test_portfolio_id}", result)

    # Test 3: Read All Portfolios
    print("\n[TEST 3] Reading all portfolios...")
    result = read_portfolio()
    print_result("Read All Portfolios", result)

    # Test 4: Update Portfolio Weights
    if test_portfolio_id:
        print("\n[TEST 4] Updating portfolio weights...")
        result = update_portfolio_weights(
            portfolio_id=test_portfolio_id,
            etf_list=["SPY", "AGG", "GLD"],
            weights=[50.0, 30.0, 20.0]
        )
        print_result(f"Update Portfolio {test_portfolio_id} Weights", result)

        # Read updated portfolio
        print("\n[TEST 4b] Reading updated portfolio...")
        result = read_portfolio(portfolio_id=test_portfolio_id)
        print_result(f"Read Updated Portfolio {test_portfolio_id}", result)

    # Test 5: Delete Portfolio (commented out to preserve data)
    # if test_portfolio_id:
    #     print("\n[TEST 5] Deleting portfolio...")
    #     result = delete_portfolio(portfolio_id=test_portfolio_id, confirm=False)
    #     print_result(f"Delete Portfolio {test_portfolio_id}", result)

    return test_portfolio_id


def test_etf_operations():
    """Test ETF CRUD operations"""
    print("\n" + "#"*80)
    print("# TESTING ETF OPERATIONS")
    print("#"*80)

    # Test 1: Add New ETF
    print("\n[TEST 1] Adding a new ETF...")
    result = add_etf(
        ticker="TEST",
        name="Test ETF",
        asset_class="Test Class",
        expense_ratio=0.10,
        inception_date="2020-01-01",
        description="ETF for testing purposes"
    )
    print_result("Add ETF", result)

    # Test 2: Get Single ETF Info
    print("\n[TEST 2] Getting ETF info for SPY...")
    result = get_etf_info(ticker="SPY")
    print_result("Get ETF Info (SPY)", result)

    # Test 3: Get All ETFs
    print("\n[TEST 3] Getting all ETFs (first 5)...")
    result = get_etf_info()
    if result['success'] and result['data']:
        result['data'] = result['data'][:5]  # Show only first 5
    print_result("Get All ETFs (First 5)", result)

    # Test 4: Update ETF Prices (commented out to avoid API calls)
    # print("\n[TEST 4] Updating ETF prices for SPY...")
    # result = update_etf_prices(ticker="SPY", start_date="2024-01-01")
    # print_result("Update ETF Prices (SPY)", result)

    # Test 5: Delete ETF (commented out to preserve data)
    # print("\n[TEST 5] Deleting test ETF...")
    # result = delete_etf(ticker="TEST", confirm=False)
    # print_result("Delete ETF (TEST)", result)


def test_backtest_operations():
    """Test backtest CRUD operations"""
    print("\n" + "#"*80)
    print("# TESTING BACKTEST OPERATIONS")
    print("#"*80)

    # Test 1: List All Backtests
    print("\n[TEST 1] Listing all backtests...")
    result = list_backtests()
    print_result("List All Backtests", result)

    # Test 2: List Backtests for Specific Portfolio
    print("\n[TEST 2] Listing backtests for portfolio 1...")
    result = list_backtests(portfolio_id=1)
    print_result("List Backtests (Portfolio 1)", result)

    # Test 3: Delete Backtest (commented out to preserve data)
    # if result['success'] and result['data']:
    #     backtest_id = result['data'][0]['backtest_id']
    #     print(f"\n[TEST 3] Deleting backtest {backtest_id}...")
    #     result = delete_backtest(backtest_id=backtest_id)
    #     print_result(f"Delete Backtest {backtest_id}", result)


def test_validation():
    """Test validation functions"""
    print("\n" + "#"*80)
    print("# TESTING VALIDATION")
    print("#"*80)

    # Test 1: Invalid weights (don't sum to 100)
    print("\n[TEST 1] Testing invalid weights (sum != 100)...")
    result = create_portfolio(
        name="Invalid Portfolio",
        description="Should fail",
        etf_list=["SPY", "AGG"],
        weights=[50.0, 40.0],  # Only sums to 90
        user_id=1
    )
    print_result("Create Portfolio (Invalid Weights)", result)

    # Test 2: Negative weights
    print("\n[TEST 2] Testing negative weights...")
    result = create_portfolio(
        name="Invalid Portfolio",
        description="Should fail",
        etf_list=["SPY", "AGG"],
        weights=[110.0, -10.0],  # Negative weight
        user_id=1
    )
    print_result("Create Portfolio (Negative Weights)", result)

    # Test 3: Non-existent ETF
    print("\n[TEST 3] Testing non-existent ETF...")
    result = create_portfolio(
        name="Invalid Portfolio",
        description="Should fail",
        etf_list=["SPY", "NONEXIST"],
        weights=[60.0, 40.0],
        user_id=1
    )
    print_result("Create Portfolio (Non-existent ETF)", result)

    # Test 4: Invalid ticker format
    print("\n[TEST 4] Testing invalid ticker format...")
    result = add_etf(
        ticker="INVALID_TICKER_123",  # Too long
        name="Invalid ETF",
        asset_class="Test",
        expense_ratio=0.10,
        inception_date="2020-01-01"
    )
    print_result("Add ETF (Invalid Ticker)", result)


def test_database_stats():
    """Test database statistics"""
    print("\n" + "#"*80)
    print("# DATABASE STATISTICS")
    print("#"*80)

    result = get_database_stats()
    print_result("Database Statistics", result)


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("ETF PORTFOLIO BACKTESTING SYSTEM - CRUD OPERATIONS TEST")
    print("="*80)
    print("\nThis script tests all CRUD operations in the system.")
    print("Some destructive operations (delete) are commented out by default.")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        return

    try:
        # Test database stats first
        test_database_stats()

        # Test portfolio operations
        test_portfolio_id = test_portfolio_operations()

        # Test ETF operations
        test_etf_operations()

        # Test backtest operations
        test_backtest_operations()

        # Test validation
        test_validation()

        print("\n" + "="*80)
        print("ALL TESTS COMPLETED")
        print("="*80)
        print("\nCheck crud_operations.log for detailed logs.")
        print("="*80)

    except Exception as e:
        print(f"\n\nERROR during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
