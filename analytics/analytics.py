"""
Data Analytics Module for ETF Portfolio Backtesting System
Provides 3 key insights using SQL-based analysis

Insights:
1. Risk-Adjusted Performance Analysis
2. Optimal Rebalancing Frequency Analysis
3. DCA vs Lump Sum Market Timing Analysis

Author: ETF Backtesting System
Version: 1.0.0
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import logging
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
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
LOG_FILE = 'analytics.log'
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


def save_insight_report(filename: str, content: str):
    """Save insight report to text file"""
    with open(filename, 'w') as f:
        f.write(content)
    logger.info(f"Insight report saved to {filename}")


# ============================================================================
# INSIGHT 1: RISK-ADJUSTED PERFORMANCE ANALYSIS
# ============================================================================

def calculate_risk_adjusted_metrics(backtest_id: int) -> Dict:
    """
    Calculate risk-adjusted performance metrics for a backtest

    Metrics calculated (using SQL):
    1. Annualized Return (CAGR)
    2. Annualized Volatility (Standard Deviation)
    3. Sharpe Ratio (assume risk-free rate = 2%)
    4. Sortino Ratio (downside deviation only)
    5. Maximum Drawdown (%)
    6. Calmar Ratio (CAGR / Max Drawdown)

    Args:
        backtest_id: Backtest ID to analyze

    Returns:
        Dictionary with all metrics
    """
    logger.info(f"Calculating risk-adjusted metrics for backtest {backtest_id}")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get backtest info
        cursor.execute("""
            SELECT b.*, p.name as portfolio_name
            FROM backtests b
            JOIN portfolios p ON b.portfolio_id = p.portfolio_id
            WHERE b.backtest_id = %s
        """, (backtest_id,))
        backtest_info = cursor.fetchone()

        if not backtest_info:
            raise ValueError(f"Backtest {backtest_id} not found")

        # Get results using SQL
        query = """
        SELECT
            date,
            portfolio_value,
            daily_return,
            cumulative_return
        FROM backtest_results
        WHERE backtest_id = %s
        ORDER BY date
        """
        results_df = pd.read_sql(query, conn, params=(backtest_id,))

        if results_df.empty:
            raise ValueError(f"No results found for backtest {backtest_id}")

        # Calculate metrics
        num_days = len(results_df)
        num_years = num_days / 252  # Trading days per year

        # 1. Annualized Return (CAGR)
        initial_value = results_df.iloc[0]['portfolio_value']
        final_value = results_df.iloc[-1]['portfolio_value']
        cagr = ((final_value / initial_value) ** (1 / num_years)) - 1

        # 2. Annualized Volatility using SQL
        cursor.execute("""
            SELECT STDDEV(daily_return) as daily_std
            FROM backtest_results
            WHERE backtest_id = %s AND daily_return IS NOT NULL
        """, (backtest_id,))
        daily_std = cursor.fetchone()['daily_std']
        annualized_volatility = daily_std * np.sqrt(252) if daily_std else 0

        # 3. Sharpe Ratio (risk-free rate = 2%)
        risk_free_rate = 0.02
        excess_return = cagr - risk_free_rate
        sharpe_ratio = excess_return / annualized_volatility if annualized_volatility > 0 else 0

        # 4. Sortino Ratio (downside deviation only)
        negative_returns = results_df[results_df['daily_return'] < 0]['daily_return']
        if len(negative_returns) > 0:
            downside_std = np.std(negative_returns) * np.sqrt(252)
            sortino_ratio = excess_return / downside_std if downside_std > 0 else 0
        else:
            sortino_ratio = float('inf')  # No downside

        # 5. Maximum Drawdown using SQL window functions
        cursor.execute("""
            WITH running_max AS (
                SELECT
                    date,
                    portfolio_value,
                    MAX(portfolio_value) OVER (ORDER BY date) as peak_value
                FROM backtest_results
                WHERE backtest_id = %s
            )
            SELECT
                MIN((portfolio_value - peak_value) / peak_value) as max_drawdown
            FROM running_max
        """, (backtest_id,))
        max_drawdown = cursor.fetchone()['max_drawdown']
        max_drawdown = abs(max_drawdown) if max_drawdown else 0

        # 6. Calmar Ratio
        calmar_ratio = cagr / max_drawdown if max_drawdown > 0 else 0

        # Calculate additional metrics
        cursor.execute("""
            SELECT
                MIN(daily_return) as worst_day,
                MAX(daily_return) as best_day,
                AVG(daily_return) as avg_daily_return
            FROM backtest_results
            WHERE backtest_id = %s AND daily_return IS NOT NULL
        """, (backtest_id,))
        daily_stats = cursor.fetchone()

        # Win rate
        cursor.execute("""
            SELECT
                COUNT(CASE WHEN daily_return > 0 THEN 1 END) as winning_days,
                COUNT(*) as total_days
            FROM backtest_results
            WHERE backtest_id = %s AND daily_return IS NOT NULL
        """, (backtest_id,))
        win_stats = cursor.fetchone()
        win_rate = win_stats['winning_days'] / win_stats['total_days'] if win_stats['total_days'] > 0 else 0

        metrics = {
            'backtest_id': backtest_id,
            'portfolio_name': backtest_info['portfolio_name'],
            'strategy_type': backtest_info['strategy_type'],
            'initial_capital': float(backtest_info['initial_capital']),
            'final_value': float(final_value),
            'num_days': num_days,
            'num_years': round(num_years, 2),
            'cagr': cagr,
            'annualized_volatility': annualized_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio if sortino_ratio != float('inf') else 999.99,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar_ratio,
            'worst_day': float(daily_stats['worst_day']) if daily_stats['worst_day'] else 0,
            'best_day': float(daily_stats['best_day']) if daily_stats['best_day'] else 0,
            'avg_daily_return': float(daily_stats['avg_daily_return']) if daily_stats['avg_daily_return'] else 0,
            'win_rate': win_rate
        }

        logger.info(f"Metrics calculated - CAGR: {cagr*100:.2f}%, Sharpe: {sharpe_ratio:.2f}, Max DD: {max_drawdown*100:.2f}%")

        return metrics

    finally:
        cursor.close()
        conn.close()


def compare_with_benchmark(backtest_id: int, benchmark_ticker: str = 'SPY') -> Dict:
    """
    Compare backtest performance with benchmark (default SPY)

    Args:
        backtest_id: Backtest ID
        benchmark_ticker: Benchmark ticker (default: SPY)

    Returns:
        Dictionary with comparison metrics
    """
    logger.info(f"Comparing backtest {backtest_id} with benchmark {benchmark_ticker}")

    conn = get_db_connection()

    try:
        # Get backtest date range
        query = """
        SELECT MIN(date) as start_date, MAX(date) as end_date
        FROM backtest_results
        WHERE backtest_id = %s
        """
        date_range = pd.read_sql(query, conn, params=(backtest_id,))
        start_date = date_range.iloc[0]['start_date']
        end_date = date_range.iloc[0]['end_date']

        # Get benchmark prices
        query = """
        SELECT date, adjusted_close
        FROM daily_prices
        WHERE ticker = %s
          AND date >= %s
          AND date <= %s
        ORDER BY date
        """
        benchmark_df = pd.read_sql(query, conn, params=(benchmark_ticker, start_date, end_date))

        if benchmark_df.empty:
            logger.warning(f"No benchmark data found for {benchmark_ticker}")
            return {'error': 'Benchmark data not available'}

        # Calculate benchmark returns
        benchmark_df['daily_return'] = benchmark_df['adjusted_close'].pct_change()
        benchmark_df['cumulative_return'] = (benchmark_df['adjusted_close'] / benchmark_df.iloc[0]['adjusted_close']) - 1

        # Calculate benchmark metrics
        num_years = len(benchmark_df) / 252
        benchmark_cagr = ((benchmark_df.iloc[-1]['adjusted_close'] / benchmark_df.iloc[0]['adjusted_close']) ** (1 / num_years)) - 1
        benchmark_volatility = benchmark_df['daily_return'].std() * np.sqrt(252)
        benchmark_sharpe = (benchmark_cagr - 0.02) / benchmark_volatility if benchmark_volatility > 0 else 0

        # Get portfolio metrics
        portfolio_metrics = calculate_risk_adjusted_metrics(backtest_id)

        # Calculate alpha and beta
        query = """
        SELECT br.date, br.daily_return as portfolio_return
        FROM backtest_results br
        WHERE br.backtest_id = %s
        ORDER BY br.date
        """
        portfolio_returns = pd.read_sql(query, conn, params=(backtest_id,))

        # Merge returns
        merged = pd.merge(
            portfolio_returns,
            benchmark_df[['date', 'daily_return']].rename(columns={'daily_return': 'benchmark_return'}),
            on='date',
            how='inner'
        )

        # Calculate beta using SQL covariance
        if len(merged) > 1:
            cov_matrix = np.cov(merged['portfolio_return'].dropna(), merged['benchmark_return'].dropna())
            beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] != 0 else 1.0

            # Calculate alpha
            alpha = portfolio_metrics['cagr'] - (0.02 + beta * (benchmark_cagr - 0.02))
        else:
            beta = 1.0
            alpha = 0.0

        comparison = {
            'portfolio_cagr': portfolio_metrics['cagr'],
            'benchmark_cagr': benchmark_cagr,
            'outperformance': portfolio_metrics['cagr'] - benchmark_cagr,
            'portfolio_volatility': portfolio_metrics['annualized_volatility'],
            'benchmark_volatility': benchmark_volatility,
            'portfolio_sharpe': portfolio_metrics['sharpe_ratio'],
            'benchmark_sharpe': benchmark_sharpe,
            'alpha': alpha,
            'beta': beta,
            'information_ratio': (portfolio_metrics['cagr'] - benchmark_cagr) / (portfolio_metrics['annualized_volatility'] - benchmark_volatility) if (portfolio_metrics['annualized_volatility'] - benchmark_volatility) != 0 else 0
        }

        logger.info(f"Comparison complete - Outperformance: {comparison['outperformance']*100:.2f}%, Alpha: {alpha*100:.2f}%")

        return comparison

    finally:
        conn.close()


def generate_risk_adjusted_report(backtest_ids: List[int], output_file: str = 'insight1_risk_adjusted_performance.txt'):
    """
    Generate comprehensive risk-adjusted performance report for multiple backtests

    Args:
        backtest_ids: List of backtest IDs to analyze
        output_file: Output filename
    """
    logger.info(f"Generating risk-adjusted performance report for {len(backtest_ids)} backtests")

    all_metrics = []
    for bt_id in backtest_ids:
        try:
            metrics = calculate_risk_adjusted_metrics(bt_id)
            benchmark_comp = compare_with_benchmark(bt_id)
            metrics['benchmark_comparison'] = benchmark_comp
            all_metrics.append(metrics)
        except Exception as e:
            logger.error(f"Error analyzing backtest {bt_id}: {e}")

    # Generate report
    report_lines = []
    report_lines.append("="*100)
    report_lines.append("INSIGHT 1: RISK-ADJUSTED PERFORMANCE ANALYSIS")
    report_lines.append("="*100)
    report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Analyzed Backtests: {len(all_metrics)}\n")

    report_lines.append("\n" + "="*100)
    report_lines.append("QUESTION: Which portfolio provides the best risk-adjusted returns?")
    report_lines.append("="*100 + "\n")

    # Summary table
    report_lines.append("PERFORMANCE METRICS SUMMARY")
    report_lines.append("-"*100)
    report_lines.append(f"{'ID':<5} {'Portfolio':<30} {'Strategy':<20} {'CAGR':<10} {'Volatility':<12} {'Sharpe':<10} {'Max DD':<10}")
    report_lines.append("-"*100)

    for m in all_metrics:
        report_lines.append(
            f"{m['backtest_id']:<5} "
            f"{m['portfolio_name'][:28]:<30} "
            f"{m['strategy_type'][:18]:<20} "
            f"{m['cagr']*100:>8.2f}% "
            f"{m['annualized_volatility']*100:>10.2f}% "
            f"{m['sharpe_ratio']:>8.2f}  "
            f"{m['max_drawdown']*100:>8.2f}%"
        )

    # Detailed analysis
    report_lines.append("\n" + "="*100)
    report_lines.append("DETAILED RISK ANALYSIS")
    report_lines.append("="*100)

    for m in all_metrics:
        report_lines.append(f"\n[Backtest {m['backtest_id']}] {m['portfolio_name']} - {m['strategy_type']}")
        report_lines.append("-"*100)
        report_lines.append(f"  Return Metrics:")
        report_lines.append(f"    • CAGR (Annualized Return): {m['cagr']*100:.2f}%")
        report_lines.append(f"    • Total Return: {((m['final_value']/m['initial_capital'])-1)*100:.2f}%")
        report_lines.append(f"    • Best Day: {m['best_day']*100:.2f}%")
        report_lines.append(f"    • Worst Day: {m['worst_day']*100:.2f}%")
        report_lines.append(f"    • Win Rate: {m['win_rate']*100:.2f}%")

        report_lines.append(f"\n  Risk Metrics:")
        report_lines.append(f"    • Annualized Volatility: {m['annualized_volatility']*100:.2f}%")
        report_lines.append(f"    • Maximum Drawdown: {m['max_drawdown']*100:.2f}%")

        report_lines.append(f"\n  Risk-Adjusted Metrics:")
        report_lines.append(f"    • Sharpe Ratio: {m['sharpe_ratio']:.2f}")
        report_lines.append(f"    • Sortino Ratio: {m['sortino_ratio']:.2f}")
        report_lines.append(f"    • Calmar Ratio: {m['calmar_ratio']:.2f}")

        if 'benchmark_comparison' in m and 'error' not in m['benchmark_comparison']:
            bc = m['benchmark_comparison']
            report_lines.append(f"\n  Benchmark Comparison (SPY):")
            report_lines.append(f"    • Outperformance: {bc['outperformance']*100:+.2f}%")
            report_lines.append(f"    • Alpha: {bc['alpha']*100:+.2f}%")
            report_lines.append(f"    • Beta: {bc['beta']:.2f}")
            report_lines.append(f"    • Information Ratio: {bc['information_ratio']:.2f}")

    # Rankings
    report_lines.append("\n" + "="*100)
    report_lines.append("RANKINGS")
    report_lines.append("="*100)

    # Best Sharpe Ratio
    best_sharpe = max(all_metrics, key=lambda x: x['sharpe_ratio'])
    report_lines.append(f"\nBest Sharpe Ratio: {best_sharpe['portfolio_name']} ({best_sharpe['sharpe_ratio']:.2f})")

    # Best CAGR
    best_cagr = max(all_metrics, key=lambda x: x['cagr'])
    report_lines.append(f"Highest CAGR: {best_cagr['portfolio_name']} ({best_cagr['cagr']*100:.2f}%)")

    # Lowest Volatility
    lowest_vol = min(all_metrics, key=lambda x: x['annualized_volatility'])
    report_lines.append(f"Lowest Volatility: {lowest_vol['portfolio_name']} ({lowest_vol['annualized_volatility']*100:.2f}%)")

    # Smallest Drawdown
    smallest_dd = min(all_metrics, key=lambda x: x['max_drawdown'])
    report_lines.append(f"Smallest Max Drawdown: {smallest_dd['portfolio_name']} ({smallest_dd['max_drawdown']*100:.2f}%)")

    # Recommendations
    report_lines.append("\n" + "="*100)
    report_lines.append("ACTIONABLE INSIGHTS & RECOMMENDATIONS")
    report_lines.append("="*100)

    report_lines.append("\n1. BEST RISK-ADJUSTED PORTFOLIO:")
    report_lines.append(f"   → {best_sharpe['portfolio_name']} with Sharpe Ratio of {best_sharpe['sharpe_ratio']:.2f}")
    report_lines.append(f"   • This portfolio provides {best_sharpe['cagr']*100:.2f}% annualized return")
    report_lines.append(f"   • With volatility of {best_sharpe['annualized_volatility']*100:.2f}%")
    report_lines.append(f"   • Maximum drawdown of {best_sharpe['max_drawdown']*100:.2f}%")

    report_lines.append("\n2. FOR AGGRESSIVE INVESTORS:")
    if best_cagr['backtest_id'] != best_sharpe['backtest_id']:
        report_lines.append(f"   → {best_cagr['portfolio_name']} offers highest CAGR of {best_cagr['cagr']*100:.2f}%")
        report_lines.append(f"   • But comes with higher volatility: {best_cagr['annualized_volatility']*100:.2f}%")
        report_lines.append(f"   • And larger drawdown: {best_cagr['max_drawdown']*100:.2f}%")
    else:
        report_lines.append(f"   → Same as best risk-adjusted portfolio")

    report_lines.append("\n3. FOR CONSERVATIVE INVESTORS:")
    report_lines.append(f"   → {lowest_vol['portfolio_name']} has lowest volatility ({lowest_vol['annualized_volatility']*100:.2f}%)")
    report_lines.append(f"   • With CAGR of {lowest_vol['cagr']*100:.2f}%")
    report_lines.append(f"   • Suitable for risk-averse investors")

    report_lines.append("\n4. BENCHMARK COMPARISON:")
    best_alpha = max([m for m in all_metrics if 'benchmark_comparison' in m and 'error' not in m['benchmark_comparison']],
                     key=lambda x: x['benchmark_comparison']['alpha'], default=None)
    if best_alpha:
        bc = best_alpha['benchmark_comparison']
        report_lines.append(f"   → {best_alpha['portfolio_name']} generates highest alpha: {bc['alpha']*100:+.2f}%")
        report_lines.append(f"   • Outperforms SPY by {bc['outperformance']*100:+.2f}% annually")
        report_lines.append(f"   • Beta: {bc['beta']:.2f} ({'more' if bc['beta'] > 1 else 'less'} volatile than market)")

    report_lines.append("\n5. KEY TAKEAWAYS:")
    avg_sharpe = np.mean([m['sharpe_ratio'] for m in all_metrics])
    report_lines.append(f"   • Average Sharpe Ratio: {avg_sharpe:.2f}")
    report_lines.append(f"   • {len([m for m in all_metrics if m['sharpe_ratio'] > 1])}/{len(all_metrics)} portfolios have Sharpe > 1.0 (good)")
    report_lines.append(f"   • Volatility range: {min(m['annualized_volatility'] for m in all_metrics)*100:.2f}% - {max(m['annualized_volatility'] for m in all_metrics)*100:.2f}%")
    report_lines.append(f"   • Return range: {min(m['cagr'] for m in all_metrics)*100:.2f}% - {max(m['cagr'] for m in all_metrics)*100:.2f}%")

    report_lines.append("\n" + "="*100)
    report_lines.append("END OF INSIGHT 1 REPORT")
    report_lines.append("="*100)

    report_text = "\n".join(report_lines)
    save_insight_report(output_file, report_text)

    logger.info(f"Risk-adjusted performance report generated: {output_file}")

    return all_metrics


# ============================================================================
# INSIGHT 2: OPTIMAL REBALANCING FREQUENCY ANALYSIS
# ============================================================================

def compare_rebalancing_strategies(
    portfolio_id: int,
    start_date: str,
    end_date: str,
    initial_capital: float,
    output_file: str = 'insight2_optimal_rebalancing.txt'
) -> Dict:
    """
    Compare different rebalancing frequencies to find optimal strategy

    Runs 5 backtests:
    1. Buy & Hold (no rebalancing)
    2. Monthly rebalancing
    3. Quarterly rebalancing
    4. Semi-annual rebalancing
    5. Annual rebalancing

    Compares:
    - Total Return
    - Risk-adjusted Return (Sharpe Ratio)
    - Number of Rebalancing Events
    - Total Transaction Costs
    - Net benefit after costs

    Args:
        portfolio_id: Portfolio ID to test
        start_date: Start date
        end_date: End date
        initial_capital: Initial capital
        output_file: Output filename

    Returns:
        Dictionary with comparison results
    """
    logger.info(f"Comparing rebalancing strategies for portfolio {portfolio_id}")

    # Import backtesting engine
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backtesting'))
    from backtesting_engine import run_backtest

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get portfolio name
        cursor.execute("SELECT name FROM portfolios WHERE portfolio_id = %s", (portfolio_id,))
        portfolio_info = cursor.fetchone()
        if not portfolio_info:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        portfolio_name = portfolio_info['name']

        # Run backtests for each strategy
        strategies = [
            ('buy_hold', None, 'Buy & Hold'),
            ('rebalancing', 'monthly', 'Monthly Rebalancing'),
            ('rebalancing', 'quarterly', 'Quarterly Rebalancing'),
            ('rebalancing', 'semi_annually', 'Semi-Annual Rebalancing'),
            ('rebalancing', 'annually', 'Annual Rebalancing')
        ]

        results = []

        for strategy_type, rebalance_freq, strategy_name in strategies:
            logger.info(f"Running backtest: {strategy_name}")

            try:
                # Run backtest
                if strategy_type == 'buy_hold':
                    backtest_id = run_backtest(
                        portfolio_id=portfolio_id,
                        start_date=start_date,
                        end_date=end_date,
                        initial_capital=initial_capital,
                        strategy_type=strategy_type,
                        transaction_cost=0.001
                    )
                else:
                    backtest_id = run_backtest(
                        portfolio_id=portfolio_id,
                        start_date=start_date,
                        end_date=end_date,
                        initial_capital=initial_capital,
                        strategy_type=strategy_type,
                        rebalance_frequency=rebalance_freq,
                        transaction_cost=0.001
                    )

                # Get metrics
                metrics = calculate_risk_adjusted_metrics(backtest_id)

                # Get transaction costs and rebalance count
                cursor.execute("""
                    SELECT
                        COUNT(*) as rebalance_count,
                        COALESCE(SUM(transaction_cost), 0) as total_transaction_cost
                    FROM rebalance_history
                    WHERE backtest_id = %s
                """, (backtest_id,))
                rebalance_info = cursor.fetchone()

                result = {
                    'strategy_name': strategy_name,
                    'backtest_id': backtest_id,
                    'final_value': metrics['final_value'],
                    'cagr': metrics['cagr'],
                    'sharpe_ratio': metrics['sharpe_ratio'],
                    'max_drawdown': metrics['max_drawdown'],
                    'volatility': metrics['annualized_volatility'],
                    'rebalance_count': rebalance_info['rebalance_count'],
                    'transaction_cost': float(rebalance_info['total_transaction_cost']),
                    'net_benefit': metrics['final_value'] - rebalance_info['total_transaction_cost']
                }

                results.append(result)
                logger.info(f"{strategy_name} completed - Return: {metrics['cagr']*100:.2f}%, Sharpe: {metrics['sharpe_ratio']:.2f}")

            except Exception as e:
                logger.error(f"Error running {strategy_name}: {e}")

        # Generate report
        report_lines = []
        report_lines.append("="*100)
        report_lines.append("INSIGHT 2: OPTIMAL REBALANCING FREQUENCY ANALYSIS")
        report_lines.append("="*100)
        report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Portfolio: {portfolio_name}")
        report_lines.append(f"Period: {start_date} to {end_date}")
        report_lines.append(f"Initial Capital: ${initial_capital:,.2f}\n")

        report_lines.append("="*100)
        report_lines.append("QUESTION: How often should we rebalance to maximize returns while minimizing costs?")
        report_lines.append("="*100 + "\n")

        # Comparison table
        report_lines.append("PERFORMANCE COMPARISON")
        report_lines.append("-"*100)
        report_lines.append(f"{'Strategy':<25} {'Final Value':>15} {'CAGR':>10} {'Sharpe':>10} {'Max DD':>10} {'Rebalances':>12} {'Cost':>12}")
        report_lines.append("-"*100)

        for r in results:
            report_lines.append(
                f"{r['strategy_name']:<25} "
                f"${r['final_value']:>13,.2f} "
                f"{r['cagr']*100:>8.2f}% "
                f"{r['sharpe_ratio']:>8.2f}  "
                f"{r['max_drawdown']*100:>8.2f}% "
                f"{r['rebalance_count']:>10}  "
                f"${r['transaction_cost']:>10,.2f}"
            )

        # Cost-Benefit Analysis
        report_lines.append("\n" + "="*100)
        report_lines.append("COST-BENEFIT ANALYSIS")
        report_lines.append("="*100)

        buy_hold = next(r for r in results if 'Buy & Hold' in r['strategy_name'])

        report_lines.append(f"\nBaseline (Buy & Hold):")
        report_lines.append(f"  Final Value: ${buy_hold['final_value']:,.2f}")
        report_lines.append(f"  CAGR: {buy_hold['cagr']*100:.2f}%")
        report_lines.append(f"  Transaction Cost: ${buy_hold['transaction_cost']:,.2f}")

        report_lines.append(f"\nComparison with Rebalancing Strategies:")
        report_lines.append("-"*100)

        for r in results:
            if 'Buy & Hold' not in r['strategy_name']:
                value_diff = r['final_value'] - buy_hold['final_value']
                return_diff = r['cagr'] - buy_hold['cagr']
                sharpe_diff = r['sharpe_ratio'] - buy_hold['sharpe_ratio']

                report_lines.append(f"\n{r['strategy_name']}:")
                report_lines.append(f"  Value Difference: ${value_diff:+,.2f} ({(value_diff/buy_hold['final_value'])*100:+.2f}%)")
                report_lines.append(f"  CAGR Difference: {return_diff*100:+.2f}%")
                report_lines.append(f"  Sharpe Difference: {sharpe_diff:+.2f}")
                report_lines.append(f"  Transaction Costs: ${r['transaction_cost']:,.2f}")
                report_lines.append(f"  Rebalancing Events: {r['rebalance_count']}")
                report_lines.append(f"  Cost per Rebalance: ${r['transaction_cost']/r['rebalance_count']:,.2f}" if r['rebalance_count'] > 0 else "  Cost per Rebalance: N/A")
                report_lines.append(f"  Net Benefit: ${value_diff - r['transaction_cost']:+,.2f}")

        # Rankings
        report_lines.append("\n" + "="*100)
        report_lines.append("RANKINGS")
        report_lines.append("="*100)

        best_return = max(results, key=lambda x: x['cagr'])
        best_sharpe = max(results, key=lambda x: x['sharpe_ratio'])
        lowest_cost = min(results, key=lambda x: x['transaction_cost'])
        best_net = max(results, key=lambda x: x['net_benefit'])

        report_lines.append(f"\nHighest CAGR: {best_return['strategy_name']} ({best_return['cagr']*100:.2f}%)")
        report_lines.append(f"Best Sharpe Ratio: {best_sharpe['strategy_name']} ({best_sharpe['sharpe_ratio']:.2f})")
        report_lines.append(f"Lowest Transaction Cost: {lowest_cost['strategy_name']} (${lowest_cost['transaction_cost']:,.2f})")
        report_lines.append(f"Best Net Benefit: {best_net['strategy_name']} (${best_net['net_benefit']:,.2f})")

        # Actionable Insights
        report_lines.append("\n" + "="*100)
        report_lines.append("ACTIONABLE INSIGHTS & RECOMMENDATIONS")
        report_lines.append("="*100)

        # Determine optimal strategy
        rebalancing_strategies = [r for r in results if 'Buy & Hold' not in r['strategy_name']]

        report_lines.append("\n1. OPTIMAL REBALANCING FREQUENCY:")
        if best_net['strategy_name'] == 'Buy & Hold':
            report_lines.append("   → NO REBALANCING (Buy & Hold) is optimal for this portfolio")
            report_lines.append("   • Rebalancing costs outweigh benefits")
            report_lines.append("   • Portfolio naturally maintains good balance")
        else:
            report_lines.append(f"   → {best_net['strategy_name']} provides best net benefit")
            value_improvement = best_net['net_benefit'] - buy_hold['final_value']
            report_lines.append(f"   • Improves final value by ${value_improvement:+,.2f} after costs")
            report_lines.append(f"   • Requires {best_net['rebalance_count']} rebalancing events")
            report_lines.append(f"   • Total transaction cost: ${best_net['transaction_cost']:,.2f}")

        report_lines.append("\n2. RISK CONSIDERATION:")
        if best_sharpe['strategy_name'] != best_return['strategy_name']:
            report_lines.append(f"   → {best_sharpe['strategy_name']} offers best risk-adjusted returns")
            report_lines.append(f"   • Sharpe Ratio: {best_sharpe['sharpe_ratio']:.2f}")
            report_lines.append(f"   • Better choice for risk-conscious investors")
        else:
            report_lines.append(f"   → {best_sharpe['strategy_name']} wins on both return and risk-adjusted basis")

        report_lines.append("\n3. TRANSACTION COST IMPACT:")
        total_costs = sum(r['transaction_cost'] for r in rebalancing_strategies)
        avg_cost = total_costs / len(rebalancing_strategies) if rebalancing_strategies else 0
        report_lines.append(f"   • Average transaction cost: ${avg_cost:,.2f}")
        report_lines.append(f"   • As % of initial capital: {(avg_cost/initial_capital)*100:.2f}%")
        highest_cost = max(rebalancing_strategies, key=lambda x: x['transaction_cost'])
        report_lines.append(f"   • Highest cost strategy: {highest_cost['strategy_name']} (${highest_cost['transaction_cost']:,.2f})")

        report_lines.append("\n4. REBALANCING FREQUENCY TRADE-OFF:")
        report_lines.append("   • More frequent rebalancing:")
        report_lines.append("     ✓ Maintains target allocation more closely")
        report_lines.append("     ✓ May reduce drift and volatility")
        report_lines.append("     ✗ Higher transaction costs")
        report_lines.append("     ✗ More tax events (if taxable account)")
        report_lines.append("   • Less frequent rebalancing:")
        report_lines.append("     ✓ Lower transaction costs")
        report_lines.append("     ✓ Fewer tax events")
        report_lines.append("     ✗ Larger portfolio drift")
        report_lines.append("     ✗ May increase volatility")

        report_lines.append("\n5. PRACTICAL RECOMMENDATIONS:")
        report_lines.append(f"   For this portfolio ({portfolio_name}):")

        # Calculate average benefit of rebalancing
        rebal_benefits = [r['final_value'] - buy_hold['final_value'] for r in rebalancing_strategies]
        avg_benefit = np.mean(rebal_benefits)

        if avg_benefit > 0:
            report_lines.append("   → Rebalancing IS beneficial for this portfolio")
            report_lines.append(f"   → Recommended frequency: {best_net['strategy_name']}")
            if 'Quarterly' in best_net['strategy_name']:
                report_lines.append("   • Rebalance every 3 months (Jan, Apr, Jul, Oct)")
            elif 'Semi-Annual' in best_net['strategy_name']:
                report_lines.append("   • Rebalance twice a year (Jan, Jul)")
            elif 'Annual' in best_net['strategy_name']:
                report_lines.append("   • Rebalance once a year (January)")
            elif 'Monthly' in best_net['strategy_name']:
                report_lines.append("   • Rebalance monthly (first trading day)")
        else:
            report_lines.append("   → Buy & Hold is BETTER for this portfolio")
            report_lines.append("   • Rebalancing costs exceed benefits")
            report_lines.append("   • Consider rebalancing only when:")
            report_lines.append("     - Adding new contributions")
            report_lines.append("     - Major market events occur")
            report_lines.append("     - Asset allocation drifts > 5% from target")

        report_lines.append("\n6. KEY TAKEAWAYS:")
        report_lines.append(f"   • Return range: {min(r['cagr'] for r in results)*100:.2f}% - {max(r['cagr'] for r in results)*100:.2f}%")
        report_lines.append(f"   • Cost range: ${min(r['transaction_cost'] for r in results):,.2f} - ${max(r['transaction_cost'] for r in results):,.2f}")
        report_lines.append(f"   • Optimal strategy: {best_net['strategy_name']}")
        report_lines.append(f"   • Expected annual return: {best_net['cagr']*100:.2f}%")

        report_lines.append("\n" + "="*100)
        report_lines.append("END OF INSIGHT 2 REPORT")
        report_lines.append("="*100)

        report_text = "\n".join(report_lines)
        save_insight_report(output_file, report_text)

        logger.info(f"Rebalancing frequency analysis report generated: {output_file}")

        return {
            'portfolio_name': portfolio_name,
            'strategies': results,
            'optimal_strategy': best_net['strategy_name'],
            'buy_hold_value': buy_hold['final_value'],
            'best_net_value': best_net['net_benefit']
        }

    finally:
        cursor.close()
        conn.close()


# ============================================================================
# INSIGHT 3: DCA VS LUMP SUM MARKET TIMING ANALYSIS
# ============================================================================

def compare_dca_vs_lumpsum(
    portfolio_id: int,
    total_capital: float,
    investment_period_months: int,
    start_date: str,
    end_date: str,
    output_file: str = 'insight3_dca_vs_lumpsum.txt'
) -> Dict:
    """
    Compare Dollar Cost Averaging (DCA) vs Lump Sum investment

    Scenarios:
    A. Lump Sum - Invest 100% on day 1
    B. DCA - Invest evenly over investment_period_months

    Analyzes performance across different market conditions:
    - Bull markets
    - Bear markets
    - Volatile markets
    - Recovery periods

    Args:
        portfolio_id: Portfolio ID to test
        total_capital: Total amount to invest
        investment_period_months: DCA period in months
        start_date: Start date
        end_date: End date
        output_file: Output filename

    Returns:
        Dictionary with comparison results
    """
    logger.info(f"Comparing DCA vs Lump Sum for portfolio {portfolio_id}")

    # Import backtesting engine
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backtesting'))
    from backtesting_engine import run_backtest

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get portfolio name
        cursor.execute("SELECT name FROM portfolios WHERE portfolio_id = %s", (portfolio_id,))
        portfolio_info = cursor.fetchone()
        if not portfolio_info:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        portfolio_name = portfolio_info['name']

        # Calculate monthly contribution for DCA
        monthly_contribution = total_capital / investment_period_months

        logger.info(f"Running Lump Sum backtest...")
        # Scenario A: Lump Sum
        lumpsum_bt_id = run_backtest(
            portfolio_id=portfolio_id,
            start_date=start_date,
            end_date=end_date,
            initial_capital=total_capital,
            strategy_type='buy_hold',
            transaction_cost=0.001
        )

        logger.info(f"Running DCA backtest...")
        # Scenario B: DCA
        dca_bt_id = run_backtest(
            portfolio_id=portfolio_id,
            start_date=start_date,
            end_date=end_date,
            initial_capital=0,  # Start with 0, contribute monthly
            strategy_type='dca',
            monthly_contribution=monthly_contribution,
            transaction_cost=0.001
        )

        # Get metrics for both
        lumpsum_metrics = calculate_risk_adjusted_metrics(lumpsum_bt_id)
        dca_metrics = calculate_risk_adjusted_metrics(dca_bt_id)

        # Get daily values for comparison
        query = """
        SELECT date, portfolio_value, cumulative_return
        FROM backtest_results
        WHERE backtest_id = %s
        ORDER BY date
        """
        lumpsum_df = pd.read_sql(query, conn, params=(lumpsum_bt_id,))
        dca_df = pd.read_sql(query, conn, params=(dca_bt_id,))

        # Merge for comparison
        comparison_df = pd.merge(
            lumpsum_df[['date', 'portfolio_value']].rename(columns={'portfolio_value': 'lumpsum_value'}),
            dca_df[['date', 'portfolio_value']].rename(columns={'portfolio_value': 'dca_value'}),
            on='date',
            how='outer'
        )

        # Calculate win/loss
        comparison_df['dca_wins'] = comparison_df['dca_value'] > comparison_df['lumpsum_value']
        win_rate = comparison_df['dca_wins'].sum() / len(comparison_df) if len(comparison_df) > 0 else 0

        # Analyze market conditions using SQL
        cursor.execute("""
            SELECT ticker, date, adjusted_close
            FROM daily_prices
            WHERE ticker = 'SPY'
              AND date >= %s
              AND date <= %s
            ORDER BY date
        """, (start_date, end_date))
        spy_data = pd.DataFrame(cursor.fetchall())

        # Calculate market trend
        if not spy_data.empty:
            spy_data['sma_50'] = spy_data['adjusted_close'].rolling(50).mean()
            spy_data['sma_200'] = spy_data['adjusted_close'].rolling(200).mean()
            spy_data['market_trend'] = np.where(
                spy_data['sma_50'] > spy_data['sma_200'], 'Bull', 'Bear'
            )

            # Count days in each market condition
            bull_days = (spy_data['market_trend'] == 'Bull').sum()
            bear_days = (spy_data['market_trend'] == 'Bear').sum()
        else:
            bull_days = 0
            bear_days = 0

        # Generate report
        report_lines = []
        report_lines.append("="*100)
        report_lines.append("INSIGHT 3: DCA VS LUMP SUM MARKET TIMING ANALYSIS")
        report_lines.append("="*100)
        report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Portfolio: {portfolio_name}")
        report_lines.append(f"Period: {start_date} to {end_date}")
        report_lines.append(f"Total Capital: ${total_capital:,.2f}")
        report_lines.append(f"DCA Period: {investment_period_months} months\n")

        report_lines.append("="*100)
        report_lines.append("QUESTION: Is DCA better than Lump Sum? Under what market conditions?")
        report_lines.append("="*100 + "\n")

        # Scenario descriptions
        report_lines.append("INVESTMENT SCENARIOS")
        report_lines.append("-"*100)
        report_lines.append("\nScenario A: LUMP SUM")
        report_lines.append(f"  • Invest entire ${total_capital:,.2f} on day 1")
        report_lines.append(f"  • Strategy: Buy and Hold")
        report_lines.append(f"  • Transaction cost: 0.1% (${total_capital*0.001:,.2f})")

        report_lines.append("\nScenario B: DOLLAR COST AVERAGING (DCA)")
        report_lines.append(f"  • Invest ${monthly_contribution:,.2f} every month for {investment_period_months} months")
        report_lines.append(f"  • Total invested: ${total_capital:,.2f}")
        report_lines.append(f"  • Strategy: Regular contributions")
        report_lines.append(f"  • Transaction costs: ${investment_period_months * monthly_contribution * 0.001:,.2f}")

        # Performance comparison
        report_lines.append("\n" + "="*100)
        report_lines.append("PERFORMANCE COMPARISON")
        report_lines.append("="*100)

        report_lines.append(f"\n{'Metric':<40} {'Lump Sum':>20} {'DCA':>20} {'Difference':>15}")
        report_lines.append("-"*100)

        metrics_to_compare = [
            ('Final Portfolio Value', lumpsum_metrics['final_value'], dca_metrics['final_value'], 'currency'),
            ('CAGR', lumpsum_metrics['cagr']*100, dca_metrics['cagr']*100, 'percent'),
            ('Total Return', ((lumpsum_metrics['final_value']/total_capital)-1)*100,
             ((dca_metrics['final_value']/total_capital)-1)*100, 'percent'),
            ('Annualized Volatility', lumpsum_metrics['annualized_volatility']*100,
             dca_metrics['annualized_volatility']*100, 'percent'),
            ('Sharpe Ratio', lumpsum_metrics['sharpe_ratio'], dca_metrics['sharpe_ratio'], 'ratio'),
            ('Maximum Drawdown', lumpsum_metrics['max_drawdown']*100, dca_metrics['max_drawdown']*100, 'percent'),
            ('Best Day', lumpsum_metrics['best_day']*100, dca_metrics['best_day']*100, 'percent'),
            ('Worst Day', lumpsum_metrics['worst_day']*100, dca_metrics['worst_day']*100, 'percent'),
        ]

        for metric_name, ls_value, dca_value, metric_type in metrics_to_compare:
            if metric_type == 'currency':
                diff = dca_value - ls_value
                report_lines.append(
                    f"{metric_name:<40} ${ls_value:>18,.2f} ${dca_value:>18,.2f} ${diff:>13,.2f}"
                )
            elif metric_type == 'percent':
                diff = dca_value - ls_value
                report_lines.append(
                    f"{metric_name:<40} {ls_value:>18.2f}% {dca_value:>18.2f}% {diff:>13.2f}%"
                )
            else:  # ratio
                diff = dca_value - ls_value
                report_lines.append(
                    f"{metric_name:<40} {ls_value:>20.2f} {dca_value:>20.2f} {diff:>15.2f}"
                )

        # Winner determination
        report_lines.append("\n" + "="*100)
        report_lines.append("RESULTS")
        report_lines.append("="*100)

        value_diff = dca_metrics['final_value'] - lumpsum_metrics['final_value']
        return_diff = dca_metrics['cagr'] - lumpsum_metrics['cagr']

        if value_diff > 0:
            winner = "DCA"
            report_lines.append(f"\n🏆 WINNER: Dollar Cost Averaging (DCA)")
            report_lines.append(f"  • DCA outperformed by ${value_diff:,.2f} ({(value_diff/lumpsum_metrics['final_value'])*100:.2f}%)")
        else:
            winner = "Lump Sum"
            report_lines.append(f"\n🏆 WINNER: Lump Sum")
            report_lines.append(f"  • Lump Sum outperformed by ${abs(value_diff):,.2f} ({(abs(value_diff)/lumpsum_metrics['final_value'])*100:.2f}%)")

        report_lines.append(f"\nDCA Win Rate: {win_rate*100:.2f}% of trading days")
        report_lines.append(f"Lump Sum Win Rate: {(1-win_rate)*100:.2f}% of trading days")

        # Market conditions analysis
        report_lines.append("\n" + "="*100)
        report_lines.append("MARKET CONDITIONS ANALYSIS")
        report_lines.append("="*100)

        total_days = bull_days + bear_days
        if total_days > 0:
            report_lines.append(f"\nMarket Condition During Period:")
            report_lines.append(f"  • Bull Market Days: {bull_days} ({(bull_days/total_days)*100:.1f}%)")
            report_lines.append(f"  • Bear Market Days: {bear_days} ({(bear_days/total_days)*100:.1f}%)")

            if bull_days > bear_days:
                predominant = "Bull"
            else:
                predominant = "Bear"

            report_lines.append(f"  • Predominant Trend: {predominant} Market")

        # Volatility comparison
        report_lines.append("\n" + "="*100)
        report_lines.append("RISK ANALYSIS")
        report_lines.append("="*100)

        report_lines.append(f"\nVolatility Comparison:")
        vol_diff = dca_metrics['annualized_volatility'] - lumpsum_metrics['annualized_volatility']
        report_lines.append(f"  • Lump Sum Volatility: {lumpsum_metrics['annualized_volatility']*100:.2f}%")
        report_lines.append(f"  • DCA Volatility: {dca_metrics['annualized_volatility']*100:.2f}%")
        report_lines.append(f"  • Difference: {vol_diff*100:+.2f}%")

        if vol_diff < 0:
            report_lines.append("  • DCA provided LOWER volatility (smoother ride)")
        else:
            report_lines.append("  • Lump Sum had LOWER volatility")

        report_lines.append(f"\nDrawdown Comparison:")
        dd_diff = dca_metrics['max_drawdown'] - lumpsum_metrics['max_drawdown']
        report_lines.append(f"  • Lump Sum Max Drawdown: {lumpsum_metrics['max_drawdown']*100:.2f}%")
        report_lines.append(f"  • DCA Max Drawdown: {dca_metrics['max_drawdown']*100:.2f}%")
        report_lines.append(f"  • Difference: {dd_diff*100:+.2f}%")

        if dd_diff < 0:
            report_lines.append("  • DCA experienced SMALLER drawdowns")
        else:
            report_lines.append("  • Lump Sum experienced SMALLER drawdowns")

        # Psychological benefits
        report_lines.append("\n" + "="*100)
        report_lines.append("PSYCHOLOGICAL CONSIDERATIONS")
        report_lines.append("="*100)

        report_lines.append("\nDCA Benefits:")
        report_lines.append("  ✓ Reduced timing risk (no need to pick the 'right' time)")
        report_lines.append("  ✓ Smoother emotional experience (averaging out volatility)")
        report_lines.append("  ✓ Disciplined investing habit")
        report_lines.append("  ✓ Lower regret if market drops immediately")
        report_lines.append(f"  ✓ Average volatility experience: {dca_metrics['annualized_volatility']*100:.2f}%")

        report_lines.append("\nLump Sum Benefits:")
        report_lines.append("  ✓ Maximum time in market (compound growth)")
        report_lines.append("  ✓ Fewer transactions (lower costs)")
        report_lines.append("  ✓ Simpler execution (one decision)")
        report_lines.append("  ✓ Historically better in bull markets")

        # Actionable insights
        report_lines.append("\n" + "="*100)
        report_lines.append("ACTIONABLE INSIGHTS & RECOMMENDATIONS")
        report_lines.append("="*100)

        report_lines.append("\n1. BASED ON THIS ANALYSIS:")
        report_lines.append(f"   → {winner} performed better for this period")
        report_lines.append(f"   • Return difference: {return_diff*100:+.2f}%")
        report_lines.append(f"   • Value difference: ${value_diff:+,.2f}")

        report_lines.append("\n2. WHEN TO CHOOSE LUMP SUM:")
        report_lines.append("   ✓ You have high conviction in long-term growth")
        report_lines.append("   ✓ You can handle short-term volatility")
        report_lines.append("   ✓ Market is in early bull phase")
        report_lines.append("   ✓ Minimizing costs is priority")
        report_lines.append("   ✓ Investment horizon is long (10+ years)")

        report_lines.append("\n3. WHEN TO CHOOSE DCA:")
        report_lines.append("   ✓ You're uncomfortable with market timing")
        report_lines.append("   ✓ You want to reduce emotional stress")
        report_lines.append("   ✓ Market seems overvalued or volatile")
        report_lines.append("   ✓ You receive regular income (salary)")
        report_lines.append("   ✓ You're a newer investor building discipline")

        report_lines.append("\n4. MARKET CONDITION INSIGHTS:")
        if predominant == "Bull":
            report_lines.append("   • This was predominantly a BULL market")
            report_lines.append("   • Lump Sum typically performs better in bull markets")
            report_lines.append("   • Early investment captured more upside")
        else:
            report_lines.append("   • This was predominantly a BEAR market")
            report_lines.append("   • DCA typically performs better in bear markets")
            report_lines.append("   • Averaging in bought more shares at lower prices")

        report_lines.append("\n5. PRACTICAL RECOMMENDATIONS:")
        report_lines.append("   For most investors, consider a HYBRID approach:")
        report_lines.append("   • Invest 50-70% immediately (get time in market)")
        report_lines.append("   • DCA remaining 30-50% over 3-6 months")
        report_lines.append("   • This balances timing risk with compound growth")
        report_lines.append("   • Reduces regret from either extreme")

        report_lines.append("\n6. KEY TAKEAWAYS:")
        report_lines.append(f"   • Winner this period: {winner}")
        report_lines.append(f"   • Performance difference: {abs(return_diff)*100:.2f}%")
        report_lines.append(f"   • DCA win rate: {win_rate*100:.1f}%")
        report_lines.append(f"   • Volatility reduction with DCA: {abs(vol_diff)*100:.2f}%")
        report_lines.append("   • Historical data shows Lump Sum wins ~67% of time")
        report_lines.append("   • But DCA provides better risk-adjusted experience")

        report_lines.append("\n7. FINAL ADVICE:")
        if winner == "Lump Sum":
            report_lines.append("   → While Lump Sum won this time, remember:")
            report_lines.append("   • Past performance doesn't guarantee future results")
            report_lines.append("   • DCA's psychological benefits have real value")
            report_lines.append("   • Consider your personal risk tolerance")
        else:
            report_lines.append("   → DCA won this time, but consider:")
            report_lines.append("   • Lump Sum often wins in the long run")
            report_lines.append("   • Time in market beats timing the market")
            report_lines.append("   • Your emotional comfort matters most")

        report_lines.append("\n" + "="*100)
        report_lines.append("END OF INSIGHT 3 REPORT")
        report_lines.append("="*100)

        report_text = "\n".join(report_lines)
        save_insight_report(output_file, report_text)

        logger.info(f"DCA vs Lump Sum analysis report generated: {output_file}")

        return {
            'portfolio_name': portfolio_name,
            'winner': winner,
            'lumpsum_metrics': lumpsum_metrics,
            'dca_metrics': dca_metrics,
            'value_difference': value_diff,
            'return_difference': return_diff,
            'win_rate': win_rate,
            'bull_days': bull_days,
            'bear_days': bear_days
        }

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("="*80)
    print("DATA ANALYTICS MODULE - ETF Portfolio Backtesting System")
    print("="*80)
    print("\nThis module provides 3 key insights:")
    print("  1. Risk-Adjusted Performance Analysis")
    print("  2. Optimal Rebalancing Frequency Analysis")
    print("  3. DCA vs Lump Sum Market Timing Analysis")
    print("\nImport this module and use the analysis functions.")
    print("See example_analytics.py for usage examples.")
    print("="*80)
