"""
Example Analytics Script - Comprehensive Demonstration

This script demonstrates how to use all 3 analytics insights:
1. Risk-Adjusted Performance Analysis
2. Optimal Rebalancing Frequency Analysis
3. DCA vs Lump Sum Market Timing Analysis

It also shows how to create professional visualizations for all insights.

Prerequisites:
- MySQL database with ETF backtesting data
- Python packages: mysql-connector-python, pandas, matplotlib, seaborn

Usage:
    python example_analytics.py

Author: ETF Portfolio Backtesting System
"""

import analytics
import visualizations
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analytics_example.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # UPDATE THIS
    'database': 'etf_backtesting'
}

# =============================================================================
# EXAMPLE 1: RISK-ADJUSTED PERFORMANCE ANALYSIS
# =============================================================================

def example_risk_adjusted_analysis():
    """
    Demonstrate Insight 1: Risk-Adjusted Performance Analysis

    This example:
    1. Analyzes risk-adjusted metrics for multiple portfolios
    2. Compares with SPY benchmark
    3. Generates comprehensive report
    4. Creates risk-return scatter plot and drawdown chart
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: RISK-ADJUSTED PERFORMANCE ANALYSIS")
    print("="*80)

    try:
        # Define analysis parameters
        portfolio_ids = [1, 2, 3]  # Analyze first 3 portfolios
        start_date = '2020-01-01'
        end_date = '2024-12-31'

        logger.info(f"Analyzing portfolios {portfolio_ids} from {start_date} to {end_date}")

        # Step 1: Calculate risk-adjusted metrics for each portfolio
        portfolio_data = []
        for portfolio_id in portfolio_ids:
            print(f"\nAnalyzing Portfolio {portfolio_id}...")

            result = analytics.calculate_risk_adjusted_metrics(
                portfolio_id=portfolio_id,
                start_date=start_date,
                end_date=end_date,
                db_config=DB_CONFIG
            )

            if result['success']:
                portfolio_data.append({
                    'name': f"Portfolio {portfolio_id}",
                    'return': result['annualized_return'],
                    'volatility': result['volatility'],
                    'sharpe': result['sharpe_ratio'],
                    'sortino': result['sortino_ratio'],
                    'calmar': result['calmar_ratio'],
                    'max_drawdown': result['max_drawdown']
                })
                print(f"  ✓ Sharpe Ratio: {result['sharpe_ratio']:.3f}")
                print(f"  ✓ Max Drawdown: {result['max_drawdown']:.2f}%")

        # Step 2: Compare with SPY benchmark
        print("\nComparing with SPY benchmark...")
        benchmark_result = analytics.compare_with_benchmark(
            portfolio_id=portfolio_ids[0],
            start_date=start_date,
            end_date=end_date,
            benchmark_symbol='SPY',
            db_config=DB_CONFIG
        )

        if benchmark_result['success']:
            benchmark_data = {
                'name': 'SPY',
                'return': benchmark_result['benchmark_annualized_return'],
                'volatility': benchmark_result['benchmark_volatility'],
                'sharpe': benchmark_result['benchmark_sharpe_ratio']
            }
            print(f"  ✓ SPY Sharpe Ratio: {benchmark_result['benchmark_sharpe_ratio']:.3f}")
            print(f"  ✓ Alpha: {benchmark_result['alpha']:.2f}%")
            print(f"  ✓ Beta: {benchmark_result['beta']:.3f}")

        # Step 3: Generate comprehensive report
        print("\nGenerating comprehensive report...")
        analytics.generate_risk_adjusted_report(
            portfolio_ids=portfolio_ids,
            start_date=start_date,
            end_date=end_date,
            benchmark_symbol='SPY',
            output_file='insight1_risk_adjusted_report.txt',
            db_config=DB_CONFIG
        )
        print("  ✓ Report saved to: insight1_risk_adjusted_report.txt")

        # Step 4: Create visualizations
        print("\nCreating visualizations...")

        # Risk-Return Scatter Plot
        visualizations.plot_risk_return_scatter(
            portfolio_data=portfolio_data,
            benchmark_data=benchmark_data,
            output_file='insight1_risk_return_scatter.png'
        )
        print("  ✓ Risk-return scatter plot saved")

        print("\n" + "="*80)
        print("INSIGHT 1 COMPLETED SUCCESSFULLY!")
        print("="*80)

    except Exception as e:
        logger.error(f"Error in risk-adjusted analysis example: {e}")
        raise


# =============================================================================
# EXAMPLE 2: OPTIMAL REBALANCING FREQUENCY ANALYSIS
# =============================================================================

def example_rebalancing_analysis():
    """
    Demonstrate Insight 2: Optimal Rebalancing Frequency Analysis

    This example:
    1. Runs backtests for 5 rebalancing strategies automatically
    2. Performs cost-benefit analysis
    3. Generates actionable recommendations
    4. Creates comparison charts
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: OPTIMAL REBALANCING FREQUENCY ANALYSIS")
    print("="*80)

    try:
        # Define analysis parameters
        portfolio_id = 1
        start_date = '2020-01-01'
        end_date = '2024-12-31'
        initial_capital = 100000.0

        logger.info(f"Analyzing optimal rebalancing for Portfolio {portfolio_id}")

        # Run comparison analysis (automatically runs 5 backtests)
        print("\nRunning backtests for 5 rebalancing strategies...")
        print("This will take a few minutes...")

        result = analytics.compare_rebalancing_strategies(
            portfolio_id=portfolio_id,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            output_file='insight2_rebalancing_analysis.txt',
            db_config=DB_CONFIG
        )

        if result['success']:
            print("\n✓ Analysis completed successfully!")
            print(f"\nKey Findings:")
            print(f"  Best Strategy: {result['best_strategy']}")
            print(f"  Best Return: {result['best_return']:.2f}%")
            print(f"  Best Sharpe: {result['best_sharpe']:.3f}")

            # Prepare data for visualization
            strategy_data = []
            for strategy_name, metrics in result['results'].items():
                strategy_data.append({
                    'strategy': strategy_name,
                    'return': metrics['annualized_return'],
                    'volatility': metrics['volatility'],
                    'sharpe': metrics['sharpe_ratio'],
                    'total_costs': metrics.get('total_transaction_costs', 0)
                })

            # Create visualizations
            print("\nCreating visualizations...")

            # Bar chart comparison
            visualizations.plot_rebalancing_frequency_comparison(
                strategy_data=strategy_data,
                output_file='insight2_rebalancing_comparison.png'
            )
            print("  ✓ Rebalancing comparison chart saved")

            print("\n✓ Report saved to: insight2_rebalancing_analysis.txt")

        print("\n" + "="*80)
        print("INSIGHT 2 COMPLETED SUCCESSFULLY!")
        print("="*80)

    except Exception as e:
        logger.error(f"Error in rebalancing analysis example: {e}")
        raise


# =============================================================================
# EXAMPLE 3: DCA VS LUMP SUM ANALYSIS
# =============================================================================

def example_dca_vs_lumpsum_analysis():
    """
    Demonstrate Insight 3: DCA vs Lump Sum Market Timing Analysis

    This example:
    1. Compares DCA vs Lump Sum investment strategies
    2. Analyzes performance across different market conditions
    3. Provides psychological and behavioral insights
    4. Creates comparison visualizations
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: DCA VS LUMP SUM MARKET TIMING ANALYSIS")
    print("="*80)

    try:
        # Define analysis parameters
        portfolio_id = 1
        total_capital = 100000.0
        investment_period_months = 12  # Invest over 12 months for DCA
        start_date = '2020-01-01'
        end_date = '2024-12-31'

        logger.info(f"Comparing DCA vs Lump Sum for Portfolio {portfolio_id}")

        # Run comparison analysis
        print(f"\nComparing strategies:")
        print(f"  Lump Sum: Invest ${total_capital:,.0f} on {start_date}")
        print(f"  DCA: Invest ${total_capital:,.0f} over {investment_period_months} months")
        print("\nRunning backtests...")

        result = analytics.compare_dca_vs_lumpsum(
            portfolio_id=portfolio_id,
            total_capital=total_capital,
            investment_period_months=investment_period_months,
            start_date=start_date,
            end_date=end_date,
            output_file='insight3_dca_vs_lumpsum.txt',
            db_config=DB_CONFIG
        )

        if result['success']:
            print("\n✓ Analysis completed successfully!")

            # Display key findings
            ls_return = result['lumpsum_annualized_return']
            dca_return = result['dca_annualized_return']
            winner = result['winner']

            print(f"\nKey Findings:")
            print(f"  Lump Sum Return: {ls_return:.2f}%")
            print(f"  DCA Return: {dca_return:.2f}%")
            print(f"  Winner: {winner}")
            print(f"  Win Rate (DCA): {result['dca_win_rate']:.1f}%")

            # Market condition analysis
            if 'market_conditions' in result:
                print(f"\nMarket Condition Analysis:")
                for condition, data in result['market_conditions'].items():
                    print(f"  {condition.capitalize()} Market:")
                    print(f"    - DCA Win Rate: {data['win_rate']:.1f}%")
                    print(f"    - Days in condition: {data['total_days']}")

            print("\n✓ Report saved to: insight3_dca_vs_lumpsum.txt")
            print("\nNote: Check the report for detailed psychological insights and recommendations")

        print("\n" + "="*80)
        print("INSIGHT 3 COMPLETED SUCCESSFULLY!")
        print("="*80)

    except Exception as e:
        logger.error(f"Error in DCA vs Lump Sum analysis example: {e}")
        raise


# =============================================================================
# COMPREHENSIVE EXAMPLE: RUN ALL INSIGHTS
# =============================================================================

def run_all_insights():
    """
    Run all 3 analytics insights sequentially

    This demonstrates a complete analytics workflow for portfolio evaluation
    """
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + " "*20 + "ETF PORTFOLIO ANALYTICS - FULL ANALYSIS" + " "*18 + "#")
    print("#" + " "*78 + "#")
    print("#"*80)

    start_time = datetime.now()

    try:
        # Run all insights
        example_risk_adjusted_analysis()
        example_rebalancing_analysis()
        example_dca_vs_lumpsum_analysis()

        # Calculate total execution time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "#"*80)
        print("#" + " "*78 + "#")
        print("#" + " "*25 + "ALL INSIGHTS COMPLETED!" + " "*28 + "#")
        print("#" + " "*78 + "#")
        print("#"*80)
        print(f"\nTotal execution time: {duration:.1f} seconds")

        print("\nGenerated Files:")
        print("  Reports:")
        print("    - insight1_risk_adjusted_report.txt")
        print("    - insight2_rebalancing_analysis.txt")
        print("    - insight3_dca_vs_lumpsum.txt")
        print("\n  Visualizations:")
        print("    - insight1_risk_return_scatter.png")
        print("    - insight2_rebalancing_comparison.png")
        print("\n  Logs:")
        print("    - analytics.log")
        print("    - analytics_example.log")

        print("\nNext Steps:")
        print("  1. Review the generated reports for detailed findings")
        print("  2. Examine visualizations for visual insights")
        print("  3. Use the recommendations to optimize your portfolio strategy")
        print("  4. Adjust parameters and re-run for different scenarios")

    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        print(f"\n❌ Error occurred: {e}")
        print("Please check the log files for details")
        raise


# =============================================================================
# CUSTOM ANALYSIS EXAMPLE
# =============================================================================

def custom_analysis_example():
    """
    Example of custom analysis combining multiple insights

    This shows how to build your own analytics workflow
    """
    print("\n" + "="*80)
    print("CUSTOM ANALYSIS EXAMPLE")
    print("="*80)

    # Example: Compare multiple portfolios on risk-adjusted basis,
    # then analyze optimal rebalancing for the best performer

    try:
        portfolio_ids = [1, 2, 3]
        start_date = '2020-01-01'
        end_date = '2024-12-31'

        print("\nStep 1: Evaluate all portfolios on risk-adjusted metrics...")

        best_sharpe = -999
        best_portfolio = None

        for pid in portfolio_ids:
            result = analytics.calculate_risk_adjusted_metrics(
                portfolio_id=pid,
                start_date=start_date,
                end_date=end_date,
                db_config=DB_CONFIG
            )

            if result['success'] and result['sharpe_ratio'] > best_sharpe:
                best_sharpe = result['sharpe_ratio']
                best_portfolio = pid

        print(f"\n✓ Best Portfolio: {best_portfolio} (Sharpe: {best_sharpe:.3f})")

        print(f"\nStep 2: Analyze optimal rebalancing for Portfolio {best_portfolio}...")

        analytics.compare_rebalancing_strategies(
            portfolio_id=best_portfolio,
            start_date=start_date,
            end_date=end_date,
            initial_capital=100000.0,
            output_file=f'custom_analysis_portfolio_{best_portfolio}.txt',
            db_config=DB_CONFIG
        )

        print("\n✓ Custom analysis completed!")
        print(f"✓ Report saved to: custom_analysis_portfolio_{best_portfolio}.txt")

    except Exception as e:
        logger.error(f"Error in custom analysis: {e}")
        raise


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║              ETF Portfolio Analytics - Example Demonstrations             ║
    ║                                                                            ║
    ║  This script demonstrates all 3 analytics insights with visualizations    ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)

    print("\nAvailable Examples:")
    print("  1. Risk-Adjusted Performance Analysis (Insight 1)")
    print("  2. Optimal Rebalancing Frequency Analysis (Insight 2)")
    print("  3. DCA vs Lump Sum Market Timing Analysis (Insight 3)")
    print("  4. Run All Insights (Comprehensive)")
    print("  5. Custom Analysis Example")
    print("  0. Exit")

    choice = input("\nSelect example to run (0-5): ").strip()

    if choice == '1':
        example_risk_adjusted_analysis()
    elif choice == '2':
        example_rebalancing_analysis()
    elif choice == '3':
        example_dca_vs_lumpsum_analysis()
    elif choice == '4':
        run_all_insights()
    elif choice == '5':
        custom_analysis_example()
    elif choice == '0':
        print("\nExiting...")
    else:
        print("\n❌ Invalid choice. Please run again and select 0-5.")

    print("\n" + "="*80)
    print("Thank you for using ETF Portfolio Analytics!")
    print("="*80 + "\n")
