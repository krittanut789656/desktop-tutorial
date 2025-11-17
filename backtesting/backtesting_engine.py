"""
Backtesting Engine for ETF Portfolio Backtesting System
Supports 3 strategies: Buy & Hold, Periodic Rebalancing, Dollar Cost Averaging (DCA)

MySQL Version - Optimized with pandas and batch processing

Author: ETF Backtesting System
Version: 1.0.0
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import logging
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm
import json


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'etf_backtesting',
    'port': 3306
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_FILE = 'backtest.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_db_connection():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def get_portfolio_allocations(portfolio_id: int) -> pd.DataFrame:
    """
    Get portfolio allocations from database

    Args:
        portfolio_id: Portfolio ID

    Returns:
        DataFrame with ticker and weight columns
    """
    conn = get_db_connection()
    query = """
    SELECT ticker, weight
    FROM portfolio_allocations
    WHERE portfolio_id = %s
    ORDER BY ticker
    """
    df = pd.read_sql(query, conn, params=(portfolio_id,))
    conn.close()
    return df


def get_price_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Get price data for multiple tickers using SQL query

    Args:
        tickers: List of ticker symbols
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        DataFrame with date, ticker, and adjusted_close columns
    """
    conn = get_db_connection()

    # Create placeholders for tickers
    placeholders = ','.join(['%s'] * len(tickers))

    query = f"""
    SELECT date, ticker, adjusted_close
    FROM daily_prices
    WHERE ticker IN ({placeholders})
      AND date >= %s
      AND date <= %s
    ORDER BY date, ticker
    """

    params = tuple(tickers) + (start_date, end_date)
    df = pd.read_sql(query, conn, params=params)
    conn.close()

    return df


def calculate_trading_days(start_date: str, end_date: str, price_data: pd.DataFrame) -> List[str]:
    """
    Get list of trading days from price data

    Args:
        start_date: Start date
        end_date: End date
        price_data: DataFrame with price data

    Returns:
        List of trading day dates as strings
    """
    trading_days = sorted(price_data['date'].unique())
    return [str(d) for d in trading_days]


def get_rebalance_dates(start_date: str, end_date: str, frequency: str, trading_days: List[str]) -> List[str]:
    """
    Calculate rebalance dates based on frequency

    Args:
        start_date: Start date
        end_date: End date
        frequency: 'monthly', 'quarterly', 'semi_annually', 'annually'
        trading_days: List of valid trading days

    Returns:
        List of rebalance dates
    """
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    trading_days_dt = pd.to_datetime(trading_days)

    rebalance_dates = [start_date]  # Start date is always included

    if frequency == 'monthly':
        freq = 'MS'  # Month start
    elif frequency == 'quarterly':
        freq = 'QS'  # Quarter start
    elif frequency == 'semi_annually':
        freq = '6MS'  # Semi-annual start
    elif frequency == 'annually':
        freq = 'AS'  # Annual start
    else:
        return [start_date]

    # Generate dates
    date_range = pd.date_range(start=start, end=end, freq=freq)

    for date in date_range:
        if date > start:  # Skip start date (already added)
            # Find nearest trading day
            nearest_idx = trading_days_dt.searchsorted(date)
            if nearest_idx < len(trading_days):
                nearest_date = str(trading_days[nearest_idx])[:10]
                if nearest_date not in rebalance_dates:
                    rebalance_dates.append(nearest_date)

    return sorted(rebalance_dates)


# ============================================================================
# STRATEGY IMPLEMENTATIONS
# ============================================================================

def strategy_buy_and_hold(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    initial_capital: float,
    transaction_cost: float
) -> Tuple[pd.DataFrame, Dict]:
    """
    Buy and Hold Strategy
    - Buy according to weights on first day
    - Hold without rebalancing
    - Calculate portfolio value daily

    Args:
        portfolio_id: Portfolio ID
        start_date: Start date
        end_date: End date
        initial_capital: Initial capital
        transaction_cost: Transaction cost rate

    Returns:
        Tuple of (results DataFrame, summary dict)
    """
    logger.info("Executing Buy and Hold strategy")

    # Get allocations
    allocations = get_portfolio_allocations(portfolio_id)
    tickers = allocations['ticker'].tolist()
    weights = allocations['weight'].values / 100.0  # Convert to decimal

    # Get price data
    logger.info(f"Fetching price data for {len(tickers)} ETFs from {start_date} to {end_date}")
    price_data = get_price_data(tickers, start_date, end_date)

    if price_data.empty:
        raise ValueError("No price data available for the specified date range")

    # Pivot price data for easier access
    prices_pivot = price_data.pivot(index='date', columns='ticker', values='adjusted_close')

    # Get trading days
    trading_days = prices_pivot.index.tolist()
    logger.info(f"Found {len(trading_days)} trading days")

    # Initialize on first day
    first_day_prices = prices_pivot.iloc[0]

    # Calculate shares to buy (after transaction cost)
    capital_after_cost = initial_capital * (1 - transaction_cost)
    shares = {}
    for ticker, weight in zip(tickers, weights):
        allocation_amount = capital_after_cost * weight
        price = first_day_prices[ticker]
        shares[ticker] = allocation_amount / price

    logger.info(f"Initial shares purchased: {shares}")

    # Calculate daily portfolio values
    results = []
    cash_balance = 0  # No cash in buy and hold

    for i, date in enumerate(tqdm(trading_days, desc="Calculating daily returns")):
        current_prices = prices_pivot.loc[date]

        # Calculate portfolio value
        portfolio_value = sum(shares[ticker] * current_prices[ticker] for ticker in tickers)

        # Calculate returns
        if i == 0:
            daily_return = 0.0
            cumulative_return = 0.0
        else:
            prev_value = results[-1]['portfolio_value']
            daily_return = (portfolio_value - prev_value) / prev_value
            cumulative_return = (portfolio_value - initial_capital) / initial_capital

        results.append({
            'date': date,
            'portfolio_value': portfolio_value,
            'daily_return': daily_return,
            'cumulative_return': cumulative_return,
            'cash_balance': cash_balance,
            'total_contributions': initial_capital
        })

    results_df = pd.DataFrame(results)

    # Calculate summary
    final_value = results_df.iloc[-1]['portfolio_value']
    total_return = (final_value - initial_capital) / initial_capital

    summary = {
        'strategy': 'Buy and Hold',
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'total_return_pct': total_return * 100,
        'num_trading_days': len(trading_days),
        'num_rebalances': 0,
        'total_transaction_cost': initial_capital * transaction_cost
    }

    logger.info(f"Buy and Hold completed. Final value: ${final_value:,.2f}, Return: {total_return*100:.2f}%")

    return results_df, summary


def strategy_periodic_rebalancing(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    initial_capital: float,
    rebalance_frequency: str,
    transaction_cost: float
) -> Tuple[pd.DataFrame, Dict, List[Dict]]:
    """
    Periodic Rebalancing Strategy
    - Buy according to weights on first day
    - Rebalance to target weights periodically
    - Calculate transaction costs

    Args:
        portfolio_id: Portfolio ID
        start_date: Start date
        end_date: End date
        initial_capital: Initial capital
        rebalance_frequency: Frequency ('monthly', 'quarterly', 'semi_annually', 'annually')
        transaction_cost: Transaction cost rate

    Returns:
        Tuple of (results DataFrame, summary dict, rebalance history list)
    """
    logger.info(f"Executing Periodic Rebalancing strategy ({rebalance_frequency})")

    # Get allocations
    allocations = get_portfolio_allocations(portfolio_id)
    tickers = allocations['ticker'].tolist()
    weights = allocations['weight'].values / 100.0
    target_weights = dict(zip(tickers, weights))

    # Get price data
    price_data = get_price_data(tickers, start_date, end_date)
    prices_pivot = price_data.pivot(index='date', columns='ticker', values='adjusted_close')
    trading_days = [str(d)[:10] for d in prices_pivot.index.tolist()]

    # Get rebalance dates
    rebalance_dates = get_rebalance_dates(start_date, end_date, rebalance_frequency, trading_days)
    logger.info(f"Rebalance dates: {len(rebalance_dates)} times")

    # Initialize
    shares = {ticker: 0.0 for ticker in tickers}
    cash_balance = initial_capital
    total_transaction_costs = 0.0
    rebalance_history = []

    # Initial purchase
    first_day_prices = prices_pivot.loc[pd.to_datetime(trading_days[0])]
    for ticker in tickers:
        allocation = initial_capital * target_weights[ticker]
        shares_to_buy = allocation / first_day_prices[ticker]
        shares[ticker] = shares_to_buy
    cash_balance = 0
    total_transaction_costs += initial_capital * transaction_cost

    # Calculate daily portfolio values
    results = []

    for i, date_str in enumerate(tqdm(trading_days, desc="Calculating with rebalancing")):
        date = pd.to_datetime(date_str)
        current_prices = prices_pivot.loc[date]

        # Check if rebalance date
        if date_str in rebalance_dates and i > 0:
            # Calculate current portfolio value
            current_value = sum(shares[ticker] * current_prices[ticker] for ticker in tickers) + cash_balance

            # Rebalance
            trades = []
            for ticker in tickers:
                target_value = current_value * target_weights[ticker]
                current_holding_value = shares[ticker] * current_prices[ticker]
                difference = target_value - current_holding_value

                if abs(difference) > 0.01:  # Trade if difference > $0.01
                    shares_traded = difference / current_prices[ticker]
                    shares[ticker] += shares_traded
                    trade_cost = abs(difference) * transaction_cost
                    total_transaction_costs += trade_cost

                    trades.append({
                        'ticker': ticker,
                        'shares': shares_traded,
                        'price': float(current_prices[ticker]),
                        'value': float(difference)
                    })

            if trades:
                rebalance_history.append({
                    'date': date_str,
                    'portfolio_value_before': float(current_value),
                    'trades': trades,
                    'transaction_cost': float(sum(abs(t['value']) * transaction_cost for t in trades))
                })

        # Calculate portfolio value
        portfolio_value = sum(shares[ticker] * current_prices[ticker] for ticker in tickers) + cash_balance

        # Calculate returns
        if i == 0:
            daily_return = 0.0
            cumulative_return = 0.0
        else:
            prev_value = results[-1]['portfolio_value']
            daily_return = (portfolio_value - prev_value) / prev_value
            cumulative_return = (portfolio_value - initial_capital) / initial_capital

        results.append({
            'date': date,
            'portfolio_value': portfolio_value,
            'daily_return': daily_return,
            'cumulative_return': cumulative_return,
            'cash_balance': cash_balance,
            'total_contributions': initial_capital
        })

    results_df = pd.DataFrame(results)

    # Summary
    final_value = results_df.iloc[-1]['portfolio_value']
    total_return = (final_value - initial_capital) / initial_capital

    summary = {
        'strategy': f'Periodic Rebalancing ({rebalance_frequency})',
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'total_return_pct': total_return * 100,
        'num_trading_days': len(trading_days),
        'num_rebalances': len(rebalance_history),
        'total_transaction_cost': total_transaction_costs
    }

    logger.info(f"Rebalancing completed. Final value: ${final_value:,.2f}, Return: {total_return*100:.2f}%, Rebalances: {len(rebalance_history)}")

    return results_df, summary, rebalance_history


def strategy_dollar_cost_averaging(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    initial_capital: float,
    monthly_contribution: float,
    transaction_cost: float,
    rebalance: bool = False
) -> Tuple[pd.DataFrame, Dict]:
    """
    Dollar Cost Averaging (DCA) Strategy
    - Invest initial capital at start
    - Add monthly contribution
    - Buy according to target weights
    - Optional rebalancing

    Args:
        portfolio_id: Portfolio ID
        start_date: Start date
        end_date: End date
        initial_capital: Initial capital
        monthly_contribution: Monthly contribution amount
        transaction_cost: Transaction cost rate
        rebalance: Whether to rebalance on contribution dates

    Returns:
        Tuple of (results DataFrame, summary dict)
    """
    logger.info(f"Executing Dollar Cost Averaging strategy (Monthly contribution: ${monthly_contribution})")

    # Get allocations
    allocations = get_portfolio_allocations(portfolio_id)
    tickers = allocations['ticker'].tolist()
    weights = allocations['weight'].values / 100.0
    target_weights = dict(zip(tickers, weights))

    # Get price data
    price_data = get_price_data(tickers, start_date, end_date)
    prices_pivot = price_data.pivot(index='date', columns='ticker', values='adjusted_close')
    trading_days = [str(d)[:10] for d in prices_pivot.index.tolist()]

    # Get monthly contribution dates (first trading day of each month)
    contribution_dates = []
    prev_month = None
    for date_str in trading_days:
        date = pd.to_datetime(date_str)
        if prev_month is None or date.month != prev_month:
            contribution_dates.append(date_str)
            prev_month = date.month

    logger.info(f"DCA contribution dates: {len(contribution_dates)} times")

    # Initialize
    shares = {ticker: 0.0 for ticker in tickers}
    cash_balance = 0
    total_contributions = initial_capital
    total_transaction_costs = 0.0

    # Initial purchase
    first_day_prices = prices_pivot.loc[pd.to_datetime(trading_days[0])]
    capital_after_cost = initial_capital * (1 - transaction_cost)
    for ticker in tickers:
        allocation = capital_after_cost * target_weights[ticker]
        shares[ticker] = allocation / first_day_prices[ticker]
    total_transaction_costs += initial_capital * transaction_cost

    # Calculate daily values
    results = []

    for i, date_str in enumerate(tqdm(trading_days, desc="Calculating DCA")):
        date = pd.to_datetime(date_str)
        current_prices = prices_pivot.loc[date]

        # Check if contribution date
        if date_str in contribution_dates and i > 0:
            total_contributions += monthly_contribution
            contribution_after_cost = monthly_contribution * (1 - transaction_cost)
            total_transaction_costs += monthly_contribution * transaction_cost

            # Buy shares according to target weights
            for ticker in tickers:
                allocation = contribution_after_cost * target_weights[ticker]
                shares_to_buy = allocation / current_prices[ticker]
                shares[ticker] += shares_to_buy

        # Calculate portfolio value
        portfolio_value = sum(shares[ticker] * current_prices[ticker] for ticker in tickers) + cash_balance

        # Calculate returns
        if i == 0:
            daily_return = 0.0
            cumulative_return = 0.0
        else:
            prev_value = results[-1]['portfolio_value']
            daily_return = (portfolio_value - prev_value) / prev_value
            cumulative_return = (portfolio_value - total_contributions) / total_contributions

        results.append({
            'date': date,
            'portfolio_value': portfolio_value,
            'daily_return': daily_return,
            'cumulative_return': cumulative_return,
            'cash_balance': cash_balance,
            'total_contributions': total_contributions
        })

    results_df = pd.DataFrame(results)

    # Summary
    final_value = results_df.iloc[-1]['portfolio_value']
    total_return = (final_value - total_contributions) / total_contributions

    summary = {
        'strategy': 'Dollar Cost Averaging',
        'initial_capital': initial_capital,
        'monthly_contribution': monthly_contribution,
        'total_contributions': total_contributions,
        'final_value': final_value,
        'total_return': total_return,
        'total_return_pct': total_return * 100,
        'num_trading_days': len(trading_days),
        'num_contributions': len(contribution_dates),
        'total_transaction_cost': total_transaction_costs
    }

    logger.info(f"DCA completed. Final value: ${final_value:,.2f}, Total contributed: ${total_contributions:,.2f}, Return: {total_return*100:.2f}%")

    return results_df, summary


# ============================================================================
# MAIN BACKTEST FUNCTION
# ============================================================================

def run_backtest(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    initial_capital: float,
    strategy_type: str,
    rebalance_frequency: str = None,
    monthly_contribution: float = 0,
    transaction_cost: float = 0.001
) -> int:
    """
    Run backtest with specified strategy

    Args:
        portfolio_id: Portfolio ID
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        initial_capital: Initial capital
        strategy_type: Strategy type ('buy_hold', 'rebalancing', 'dca')
        rebalance_frequency: Rebalance frequency for rebalancing strategy
        monthly_contribution: Monthly contribution for DCA strategy
        transaction_cost: Transaction cost rate (default 0.1%)

    Returns:
        backtest_id: ID of created backtest record

    Raises:
        ValueError: If invalid parameters
    """
    logger.info("="*80)
    logger.info("STARTING BACKTEST")
    logger.info("="*80)
    logger.info(f"Portfolio ID: {portfolio_id}")
    logger.info(f"Date range: {start_date} to {end_date}")
    logger.info(f"Initial capital: ${initial_capital:,.2f}")
    logger.info(f"Strategy: {strategy_type}")
    logger.info(f"Transaction cost: {transaction_cost*100:.2f}%")

    # Validate inputs
    if strategy_type not in ['buy_hold', 'rebalancing', 'dca']:
        raise ValueError(f"Invalid strategy type: {strategy_type}")

    if strategy_type == 'rebalancing' and rebalance_frequency is None:
        raise ValueError("rebalance_frequency is required for rebalancing strategy")

    # Create backtest record
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_backtest_query = """
    INSERT INTO backtests
    (portfolio_id, start_date, end_date, initial_capital, strategy_type,
     rebalance_frequency, monthly_contribution, execution_date, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    strategy_name_map = {
        'buy_hold': 'Buy-and-Hold',
        'rebalancing': 'Rebalanced',
        'dca': 'Dollar-Cost-Averaging'
    }

    cursor.execute(insert_backtest_query, (
        portfolio_id,
        start_date,
        end_date,
        initial_capital,
        strategy_name_map[strategy_type],
        rebalance_frequency if rebalance_frequency else 'None',
        monthly_contribution,
        datetime.now(),
        'Running'
    ))
    conn.commit()
    backtest_id = cursor.lastrowid
    logger.info(f"Created backtest record with ID: {backtest_id}")

    try:
        # Execute strategy
        rebalance_history = []

        if strategy_type == 'buy_hold':
            results_df, summary = strategy_buy_and_hold(
                portfolio_id, start_date, end_date, initial_capital, transaction_cost
            )
        elif strategy_type == 'rebalancing':
            results_df, summary, rebalance_history = strategy_periodic_rebalancing(
                portfolio_id, start_date, end_date, initial_capital,
                rebalance_frequency, transaction_cost
            )
        elif strategy_type == 'dca':
            results_df, summary = strategy_dollar_cost_averaging(
                portfolio_id, start_date, end_date, initial_capital,
                monthly_contribution, transaction_cost
            )

        # Save results to database (batch insert)
        logger.info("Saving results to database...")
        save_results_to_database(backtest_id, results_df)

        # Save rebalance history if applicable
        if rebalance_history:
            save_rebalance_history(backtest_id, rebalance_history)

        # Update backtest status
        cursor.execute(
            "UPDATE backtests SET status = %s WHERE backtest_id = %s",
            ('Completed', backtest_id)
        )
        conn.commit()

        # Generate reports
        generate_summary_report(backtest_id, portfolio_id, summary, results_df)
        backup_results(backtest_id, results_df)

        logger.info("="*80)
        logger.info("BACKTEST COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        logger.info(f"Backtest ID: {backtest_id}")
        logger.info(f"Final portfolio value: ${summary['final_value']:,.2f}")
        logger.info(f"Total return: {summary['total_return_pct']:.2f}%")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"Backtest failed: {e}")
        cursor.execute(
            "UPDATE backtests SET status = %s WHERE backtest_id = %s",
            ('Failed', backtest_id)
        )
        conn.commit()
        raise
    finally:
        cursor.close()
        conn.close()

    return backtest_id


def save_results_to_database(backtest_id: int, results_df: pd.DataFrame):
    """
    Save backtest results to database using batch insert

    Args:
        backtest_id: Backtest ID
        results_df: DataFrame with results
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO backtest_results
    (backtest_id, date, portfolio_value, daily_return, cumulative_return, cash_balance, total_contributions)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Prepare batch data
    batch_data = []
    for _, row in results_df.iterrows():
        batch_data.append((
            backtest_id,
            row['date'],
            float(row['portfolio_value']),
            float(row['daily_return']),
            float(row['cumulative_return']),
            float(row['cash_balance']),
            float(row['total_contributions'])
        ))

    # Batch insert
    cursor.executemany(insert_query, batch_data)
    conn.commit()

    logger.info(f"Inserted {len(batch_data)} result records")

    cursor.close()
    conn.close()


def save_rebalance_history(backtest_id: int, rebalance_history: List[Dict]):
    """
    Save rebalance history to database

    Args:
        backtest_id: Backtest ID
        rebalance_history: List of rebalance events
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO rebalance_history
    (backtest_id, rebalance_date, rebalance_details, transaction_cost)
    VALUES (%s, %s, %s, %s)
    """

    for event in rebalance_history:
        cursor.execute(insert_query, (
            backtest_id,
            event['date'],
            json.dumps(event),
            event['transaction_cost']
        ))

    conn.commit()
    logger.info(f"Saved {len(rebalance_history)} rebalance events")

    cursor.close()
    conn.close()


def generate_summary_report(backtest_id: int, portfolio_id: int, summary: Dict, results_df: pd.DataFrame):
    """
    Generate summary report text file

    Args:
        backtest_id: Backtest ID
        portfolio_id: Portfolio ID
        summary: Summary dictionary
        results_df: Results DataFrame
    """
    filename = f"backtest_summary_{backtest_id}.txt"

    # Get portfolio info
    conn = get_db_connection()
    query = """
    SELECT p.name, pa.ticker, pa.weight, e.name as etf_name
    FROM portfolios p
    JOIN portfolio_allocations pa ON p.portfolio_id = pa.portfolio_id
    JOIN etfs e ON pa.ticker = e.ticker
    WHERE p.portfolio_id = %s
    ORDER BY pa.weight DESC
    """
    allocations = pd.read_sql(query, conn, params=(portfolio_id,))
    conn.close()

    with open(filename, 'w') as f:
        f.write("="*80 + "\n")
        f.write("BACKTEST SUMMARY REPORT\n")
        f.write("="*80 + "\n\n")

        f.write(f"Backtest ID: {backtest_id}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("PORTFOLIO COMPOSITION\n")
        f.write("-"*80 + "\n")
        f.write(f"Portfolio: {allocations.iloc[0]['name']}\n\n")
        for _, row in allocations.iterrows():
            f.write(f"  {row['ticker']:6} - {row['weight']:5.1f}% - {row['etf_name']}\n")
        f.write("\n")

        f.write("STRATEGY PARAMETERS\n")
        f.write("-"*80 + "\n")
        f.write(f"Strategy: {summary['strategy']}\n")
        f.write(f"Initial Capital: ${summary['initial_capital']:,.2f}\n")
        if 'monthly_contribution' in summary:
            f.write(f"Monthly Contribution: ${summary['monthly_contribution']:,.2f}\n")
            f.write(f"Total Contributions: ${summary['total_contributions']:,.2f}\n")
        f.write(f"Transaction Cost: ${summary['total_transaction_cost']:,.2f}\n")
        f.write("\n")

        f.write("BACKTEST PERIOD\n")
        f.write("-"*80 + "\n")
        f.write(f"Start Date: {results_df.iloc[0]['date']}\n")
        f.write(f"End Date: {results_df.iloc[-1]['date']}\n")
        f.write(f"Trading Days: {summary['num_trading_days']}\n")
        if 'num_rebalances' in summary and summary['num_rebalances'] > 0:
            f.write(f"Rebalances: {summary['num_rebalances']}\n")
        f.write("\n")

        f.write("PERFORMANCE RESULTS\n")
        f.write("-"*80 + "\n")
        f.write(f"Final Portfolio Value: ${summary['final_value']:,.2f}\n")
        f.write(f"Total Return: {summary['total_return_pct']:.2f}%\n")
        f.write(f"Annualized Return: {(summary['total_return'] / (summary['num_trading_days']/252)) * 100:.2f}%\n")

        # Calculate volatility
        daily_returns = results_df['daily_return'].values[1:]  # Skip first day
        volatility = np.std(daily_returns) * np.sqrt(252)  # Annualized
        sharpe = (summary['total_return'] / (summary['num_trading_days']/252)) / volatility if volatility > 0 else 0

        f.write(f"Volatility (Annual): {volatility*100:.2f}%\n")
        f.write(f"Sharpe Ratio: {sharpe:.2f}\n")

        # Max drawdown
        cumulative_returns = results_df['portfolio_value'].values
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdowns)

        f.write(f"Maximum Drawdown: {max_drawdown*100:.2f}%\n")

        f.write("\n")
        f.write("="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")

    logger.info(f"Summary report saved to {filename}")


def backup_results(backtest_id: int, results_df: pd.DataFrame):
    """
    Backup results to text file

    Args:
        backtest_id: Backtest ID
        results_df: Results DataFrame
    """
    filename = f"backtest_results_{backtest_id}.txt"

    with open(filename, 'w') as f:
        f.write("="*80 + "\n")
        f.write(f"BACKTEST RESULTS - Backtest ID: {backtest_id}\n")
        f.write("="*80 + "\n\n")

        f.write(f"{'Date':<12} {'Portfolio Value':>18} {'Daily Return':>15} {'Cumulative Return':>18}\n")
        f.write("-"*80 + "\n")

        for _, row in results_df.iterrows():
            f.write(f"{str(row['date'])[:10]:<12} "
                   f"${row['portfolio_value']:>15,.2f} "
                   f"{row['daily_return']*100:>13.4f}% "
                   f"{row['cumulative_return']*100:>16.2f}%\n")

    logger.info(f"Results backup saved to {filename}")


# ============================================================================
# MAIN (FOR TESTING)
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print("BACKTESTING ENGINE - ETF Portfolio Backtesting System")
    print("="*80)
    print("\nThis module provides backtesting functionality for portfolio strategies.")
    print("\nSupported strategies:")
    print("  1. Buy and Hold")
    print("  2. Periodic Rebalancing")
    print("  3. Dollar Cost Averaging (DCA)")
    print("\nImport this module and use run_backtest() function.")
    print("See example_backtest.py for usage examples.")
    print("="*80)
