"""
Text File Logging Module for ETF Backtester
Logs backtest results to text files for record-keeping
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TextLogger:
    """
    Handles logging of backtest results to text files
    """

    def __init__(self, log_directory: str = "logs"):
        """
        Initialize text logger

        Args:
            log_directory: Directory to store log files
        """
        self.log_directory = log_directory

        # Create log directory if it doesn't exist
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

    def log_backtest_summary(self, results: Dict, filename: Optional[str] = None) -> str:
        """
        Log backtest summary to a text file

        Args:
            results: Dictionary containing backtest results from backtest_engine
            filename: Optional custom filename, generates default if None

        Returns:
            Path to the created log file
        """

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"backtest_log_{timestamp}.txt"

        filepath = os.path.join(self.log_directory, filename)

        with open(filepath, 'w') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("ETF PORTFOLIO BACKTESTER - RESULTS SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            # Backtest Configuration
            f.write("BACKTEST CONFIGURATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"Run ID:              {results.get('run_id', 'N/A')}\n")
            f.write(f"Strategy:            Momentum Strategy\n")
            f.write(f"Date Range:          {results.get('start_date', 'N/A')} to {results.get('end_date', 'N/A')}\n")
            f.write(f"Lookback Period:     {results.get('lookback_days', 'N/A')} days\n")
            f.write(f"Holding Period:      {results.get('holding_period_days', 'N/A')} days\n")
            f.write(f"Rebalance Frequency: {results.get('rebalance_days', 'N/A')} days\n")
            f.write(f"Portfolio Size:      Top {results.get('top_n', 'N/A')} ETFs\n")
            f.write("\n")

            # Performance Summary
            f.write("PERFORMANCE SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Rebalances:          {results.get('total_rebalances', 0)}\n")

            cumulative_return = results.get('cumulative_return', 0) * 100
            f.write(f"Cumulative Return:         {cumulative_return:.2f}%\n")

            avg_return = results.get('avg_return_per_period', 0) * 100
            f.write(f"Avg Return per Period:     {avg_return:.2f}%\n")

            cagr = results.get('cagr', 0) * 100
            f.write(f"Compound Annual Growth Rate (CAGR): {cagr:.2f}%\n")

            # Calculate additional metrics if available
            if 'all_returns' in results and results['all_returns']:
                returns = results['all_returns']

                # Max/Min returns
                max_return = max(returns) * 100
                min_return = min(returns) * 100
                f.write(f"Best Period Return:        {max_return:.2f}%\n")
                f.write(f"Worst Period Return:       {min_return:.2f}%\n")

                # Win rate
                winning_periods = sum(1 for r in returns if r > 0)
                win_rate = (winning_periods / len(returns)) * 100 if returns else 0
                f.write(f"Win Rate:                  {win_rate:.2f}% ({winning_periods}/{len(returns)} periods)\n")

                # Volatility (standard deviation)
                if len(returns) > 1:
                    mean_return = sum(returns) / len(returns)
                    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
                    volatility = variance ** 0.5 * 100
                    f.write(f"Return Volatility:         {volatility:.2f}%\n")

                    # Sharpe-like ratio (simplified)
                    if volatility > 0:
                        sharpe = (avg_return / volatility) * (len(returns) ** 0.5)
                        f.write(f"Risk-Adjusted Return:      {sharpe:.2f}\n")

            f.write("\n")

            # Footer
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
            f.write("\n")
            f.write("Note: This report summarizes the backtested portfolio strategy.\n")
            f.write("Past performance does not guarantee future results.\n")

        print(f"\n✓ Backtest summary logged to: {filepath}")
        return filepath

    def log_analytics_insights(self, insights: Dict, filename: Optional[str] = None) -> str:
        """
        Log analytics insights to a text file

        Args:
            insights: Dictionary containing analytics results
            filename: Optional custom filename

        Returns:
            Path to the created log file
        """

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analytics_insights_{timestamp}.txt"

        filepath = os.path.join(self.log_directory, filename)

        with open(filepath, 'w') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("ETF PORTFOLIO BACKTESTER - ANALYTICS INSIGHTS\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            # Insight 1: Volatility
            if 'volatility' in insights:
                f.write("INSIGHT #1: VOLATILITY ANALYSIS BY ASSET TYPE\n")
                f.write("-" * 80 + "\n")

                for item in insights['volatility']:
                    f.write(f"\nAsset Type: {item['Asset_Type']}\n")
                    f.write(f"  Number of ETFs:            {item['Num_ETFs']}\n")
                    f.write(f"  Annualized Volatility:     {item['Annualized_Volatility_Pct']:.2f}%\n")
                    f.write(f"  Average Daily Return:      {item['Avg_Daily_Return_Pct']:.4f}%\n")
                    f.write(f"  Risk-Adjusted Return:      {item.get('Risk_Adjusted_Return', 'N/A')}\n")

                f.write("\n")

            # Insight 2: Lookback Period Optimization
            if 'lookback' in insights:
                f.write("INSIGHT #2: LOOKBACK PERIOD OPTIMIZATION\n")
                f.write("-" * 80 + "\n")

                for item in insights['lookback']:
                    f.write(f"\nLookback Period: {item['Lookback_Period_Days']} days\n")
                    f.write(f"  Number of Runs:            {item['Num_Runs']}\n")
                    f.write(f"  Cumulative Return:         {item['Cumulative_Return_Pct']:.2f}%\n")
                    f.write(f"  CAGR:                      {item['CAGR_Pct']:.2f}%\n")
                    f.write(f"  Average Rebalances:        {item['Avg_Rebalances']:.1f}\n")

                f.write("\n")

            # Insight 3: Drawdown Analysis
            if 'drawdown' in insights:
                f.write("INSIGHT #3: ASSET TYPE EXPOSURE DURING DRAWDOWNS\n")
                f.write("-" * 80 + "\n")

                for item in insights['drawdown']:
                    f.write(f"\nAsset Type: {item['Asset_Type']}\n")
                    f.write(f"  Times Held During Drawdown: {item['Num_Occurrences']}\n")
                    f.write(f"  Average Weight:             {item['Avg_Weight_Pct']:.2f}%\n")
                    f.write(f"  Contribution to Drawdown:   {item['Avg_Weighted_Contribution_Pct']:.4f}%\n")

                f.write("\n")

            # Footer
            f.write("=" * 80 + "\n")
            f.write("END OF ANALYTICS REPORT\n")
            f.write("=" * 80 + "\n")

        print(f"\n✓ Analytics insights logged to: {filepath}")
        return filepath

    def append_to_master_log(self, message: str, filename: str = "master_log.txt"):
        """
        Append a message to the master log file

        Args:
            message: Message to append
            filename: Master log filename
        """

        filepath = os.path.join(self.log_directory, filename)

        with open(filepath, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")

    def list_log_files(self) -> List[str]:
        """
        List all log files in the log directory

        Returns:
            List of log file names
        """

        if not os.path.exists(self.log_directory):
            return []

        files = [f for f in os.listdir(self.log_directory)
                if f.endswith('.txt')]

        return sorted(files, reverse=True)  # Most recent first

    def read_log_file(self, filename: str) -> Optional[str]:
        """
        Read contents of a log file

        Args:
            filename: Name of the log file

        Returns:
            File contents as string, or None if not found
        """

        filepath = os.path.join(self.log_directory, filename)

        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            return f.read()


# Example usage and testing
def main():
    """Test the text logger"""
    print("=" * 60)
    print("ETF Backtester - Testing Text Logger")
    print("=" * 60)

    # Initialize logger
    logger = TextLogger(log_directory="../logs")

    # Create sample backtest results
    sample_results = {
        'run_id': 'TEST_RUN_20250119_120000',
        'start_date': '2023-01-01',
        'end_date': '2024-01-01',
        'lookback_days': 90,
        'holding_period_days': 30,
        'rebalance_days': 30,
        'top_n': 5,
        'total_rebalances': 12,
        'cumulative_return': 0.15,
        'avg_return_per_period': 0.0125,
        'cagr': 0.148,
        'all_returns': [0.02, -0.01, 0.03, 0.015, -0.005, 0.025,
                       0.01, 0.02, -0.02, 0.03, 0.01, 0.015]
    }

    # Log the sample results
    log_file = logger.log_backtest_summary(sample_results)

    print(f"\nLog file created: {log_file}")

    # List all log files
    print("\nAll log files:")
    for f in logger.list_log_files():
        print(f"  - {f}")

    print("\n" + "=" * 60)
    print("Text logger test complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
