"""
Analytics Module for ETF Backtester
Implements 3 complex SQL queries for actionable insights
"""

import sys
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.db_connector import DatabaseConnector


class PortfolioAnalytics:
    """
    Analytics class implementing complex SQL queries for insights
    """

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize analytics module

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector

    # =========================================================================
    # INSIGHT #1: Time Series Volatility Analysis
    # =========================================================================

    def analyze_volatility_by_asset_type(self, start_date: Optional[str] = None,
                                        end_date: Optional[str] = None) -> List[Dict]:
        """
        COMPLEX SQL QUERY #1: Volatility Analysis by Asset Type

        Calculate price volatility (standard deviation of daily returns)
        for each Asset_Type over a specified period.

        This query:
        1. Calculates daily returns for each ETF
        2. Computes standard deviation of returns grouped by Asset_Type
        3. Ranks asset types by volatility

        Args:
            start_date: Start date for analysis (YYYY-MM-DD), None for all data
            end_date: End date for analysis (YYYY-MM-DD), None for all data

        Returns:
            List of dictionaries with volatility metrics per asset type
        """

        # Build date filter
        date_filter = ""
        params = []

        if start_date and end_date:
            date_filter = "WHERE pd1.Price_Date BETWEEN %s AND %s"
            params = [start_date, end_date]

        query = f"""
        WITH WeeklyReturns AS (
            -- Calculate weekly returns for each ETF
            SELECT
                em.Asset_Type,
                em.ETF_ID,
                em.Ticker_Symbol,
                pd1.Price_Date,
                pd1.Close_Price as Current_Price,
                pd2.Close_Price as Previous_Price,
                -- Weekly Return = (Current - Previous) / Previous
                ((pd1.Close_Price - pd2.Close_Price) / pd2.Close_Price) as Weekly_Return
            FROM Price_Data pd1
            INNER JOIN ETF_Master em ON pd1.ETF_ID = em.ETF_ID
            INNER JOIN Price_Data pd2 ON pd1.ETF_ID = pd2.ETF_ID
                AND pd2.Price_Date = (
                    -- Get previous week
                    SELECT MAX(Price_Date)
                    FROM Price_Data
                    WHERE ETF_ID = pd1.ETF_ID
                        AND Price_Date < pd1.Price_Date
                )
            {date_filter}
        ),
        VolatilityMetrics AS (
            -- Calculate volatility metrics by Asset Type
            SELECT
                Asset_Type,
                COUNT(DISTINCT ETF_ID) as Num_ETFs,
                COUNT(*) as Num_Observations,
                AVG(Weekly_Return) as Avg_Weekly_Return,
                STDDEV_POP(Weekly_Return) as Weekly_Volatility,
                MIN(Weekly_Return) as Min_Weekly_Return,
                MAX(Weekly_Return) as Max_Weekly_Return,
                -- Annualized volatility (assuming 52 weeks per year)
                STDDEV_POP(Weekly_Return) * SQRT(52) as Annualized_Volatility
            FROM WeeklyReturns
            GROUP BY Asset_Type
        )
        SELECT
            Asset_Type,
            Num_ETFs,
            Num_Observations,
            ROUND(Avg_Weekly_Return * 100, 4) as Avg_Weekly_Return_Pct,
            ROUND(Weekly_Volatility * 100, 4) as Weekly_Volatility_Pct,
            ROUND(Annualized_Volatility * 100, 2) as Annualized_Volatility_Pct,
            ROUND(Min_Weekly_Return * 100, 2) as Min_Weekly_Return_Pct,
            ROUND(Max_Weekly_Return * 100, 2) as Max_Weekly_Return_Pct,
            -- Risk-adjusted return (Sharpe-like ratio)
            ROUND((Avg_Weekly_Return / NULLIF(Weekly_Volatility, 0)) * SQRT(52), 2) as Risk_Adjusted_Return
        FROM VolatilityMetrics
        ORDER BY Annualized_Volatility DESC
        """

        results = self.db.execute_query_dict(query, tuple(params) if params else None)

        # Print formatted results
        self._print_volatility_results(results, start_date, end_date)

        return results

    def _print_volatility_results(self, results: List[Dict],
                                  start_date: Optional[str],
                                  end_date: Optional[str]):
        """Print formatted volatility analysis results"""

        print("\n" + "=" * 80)
        print("INSIGHT #1: VOLATILITY ANALYSIS BY ASSET TYPE")
        print("=" * 80)

        if start_date and end_date:
            print(f"Analysis Period: {start_date} to {end_date}")
        else:
            print("Analysis Period: Full historical data")

        print("\n" + "-" * 80)
        print(f"{'Asset Type':<15} {'# ETFs':<8} {'Obs':<8} "
              f"{'Avg Weekly %':<12} {'Weekly Vol %':<12} {'Annual Vol %':<15}")
        print("-" * 80)

        for row in results:
            print(f"{row['Asset_Type']:<15} "
                  f"{row['Num_ETFs']:<8} "
                  f"{row['Num_Observations']:<8} "
                  f"{row['Avg_Weekly_Return_Pct']:>11.4f} "
                  f"{row['Weekly_Volatility_Pct']:>11.4f} "
                  f"{row['Annualized_Volatility_Pct']:>14.2f}")

        print("-" * 80)

        if results:
            highest_vol = results[0]
            print(f"\n✓ INSIGHT: '{highest_vol['Asset_Type']}' has the HIGHEST volatility "
                  f"at {highest_vol['Annualized_Volatility_Pct']:.2f}% (annualized)")

            lowest_vol = results[-1]
            print(f"✓ INSIGHT: '{lowest_vol['Asset_Type']}' has the LOWEST volatility "
                  f"at {lowest_vol['Annualized_Volatility_Pct']:.2f}% (annualized)")

        print("=" * 80)

    # =========================================================================
    # INSIGHT #2: Lookback Period Optimization
    # =========================================================================

    def compare_lookback_periods(self, lookback_periods: List[int] = [90, 180]) -> List[Dict]:
        """
        COMPLEX SQL QUERY #2: Lookback Period Optimization

        Compare performance of different lookback periods by analyzing
        Strategy_Log data to calculate CAGR for each lookback period.

        This query:
        1. Groups strategy results by lookback period
        2. Calculates overall returns and CAGR for each period
        3. Compares performance metrics

        Args:
            lookback_periods: List of lookback periods to compare (days)

        Returns:
            List of dictionaries with performance metrics per lookback period
        """

        # Build IN clause for lookback periods
        lookback_str = ','.join(map(str, lookback_periods))

        query = f"""
        WITH PeriodPerformance AS (
            -- Aggregate performance by lookback period
            SELECT
                Lookback_Period_Days,
                Backtest_Run_ID,
                MIN(Selection_Date) as Start_Date,
                MAX(Selection_Date) as End_Date,
                COUNT(DISTINCT Selection_Date) as Num_Rebalances,
                COUNT(*) as Total_Selections,
                AVG(Momentum_Score) as Avg_Momentum_Score,
                -- Calculate portfolio returns (assuming equal weight)
                AVG(Holding_Return) as Avg_Holding_Return,
                SUM(Holding_Return * Portfolio_Weight) / COUNT(DISTINCT Selection_Date) as Avg_Weighted_Return_Per_Period
            FROM Strategy_Log
            WHERE Lookback_Period_Days IN ({lookback_str})
                AND Holding_Return IS NOT NULL
                AND Portfolio_Rank IS NOT NULL
            GROUP BY Lookback_Period_Days, Backtest_Run_ID
        ),
        AggregatedMetrics AS (
            -- Aggregate across all runs for each lookback period
            SELECT
                Lookback_Period_Days,
                COUNT(DISTINCT Backtest_Run_ID) as Num_Runs,
                AVG(Num_Rebalances) as Avg_Rebalances,
                AVG(Total_Selections) as Avg_Selections,
                AVG(Avg_Momentum_Score) as Overall_Avg_Momentum,
                AVG(Avg_Holding_Return) as Overall_Avg_Return,
                SUM(Avg_Weighted_Return_Per_Period) as Cumulative_Return,
                MIN(Start_Date) as Earliest_Date,
                MAX(End_Date) as Latest_Date,
                DATEDIFF(MAX(End_Date), MIN(Start_Date)) as Total_Days
            FROM PeriodPerformance
            GROUP BY Lookback_Period_Days
        )
        SELECT
            Lookback_Period_Days,
            Num_Runs,
            Avg_Rebalances,
            Avg_Selections,
            ROUND(Overall_Avg_Momentum, 4) as Avg_Momentum_Score,
            ROUND(Overall_Avg_Return * 100, 4) as Avg_Return_Per_Trade_Pct,
            ROUND(Cumulative_Return * 100, 4) as Cumulative_Return_Pct,
            -- Calculate CAGR: (1 + Total_Return)^(365.25 / Days) - 1
            ROUND(
                (POWER(1 + Cumulative_Return, 365.25 / NULLIF(Total_Days, 0)) - 1) * 100,
                2
            ) as CAGR_Pct,
            Total_Days,
            Earliest_Date,
            Latest_Date
        FROM AggregatedMetrics
        ORDER BY CAGR_Pct DESC
        """

        results = self.db.execute_query_dict(query)

        # Print formatted results
        self._print_lookback_comparison_results(results)

        return results

    def _print_lookback_comparison_results(self, results: List[Dict]):
        """Print formatted lookback period comparison results"""

        print("\n" + "=" * 80)
        print("INSIGHT #2: LOOKBACK PERIOD OPTIMIZATION (CAGR COMPARISON)")
        print("=" * 80)

        print("\n" + "-" * 80)
        print(f"{'Lookback':<12} {'# Runs':<8} {'Avg Rebal':<12} "
              f"{'Cum Return %':<15} {'CAGR %':<10} {'Days':<8}")
        print("-" * 80)

        for row in results:
            lookback_label = f"{row['Lookback_Period_Days']} days"
            print(f"{lookback_label:<12} "
                  f"{row['Num_Runs']:<8} "
                  f"{row['Avg_Rebalances']:>11.1f} "
                  f"{row['Cumulative_Return_Pct']:>14.2f} "
                  f"{row['CAGR_Pct']:>9.2f} "
                  f"{row['Total_Days']:<8}")

        print("-" * 80)

        if results:
            best = results[0]
            print(f"\n✓ INSIGHT: Lookback period of {best['Lookback_Period_Days']} days "
                  f"yielded the HIGHEST CAGR at {best['CAGR_Pct']:.2f}%")

            if len(results) > 1:
                diff = best['CAGR_Pct'] - results[-1]['CAGR_Pct']
                print(f"✓ INSIGHT: This outperformed the {results[-1]['Lookback_Period_Days']}-day "
                      f"lookback by {diff:.2f} percentage points")

        print("=" * 80)

    # =========================================================================
    # INSIGHT #3: Drawdown Analysis
    # =========================================================================

    def analyze_drawdown_exposure(self, backtest_run_id: Optional[str] = None) -> List[Dict]:
        """
        COMPLEX SQL QUERY #3: Drawdown Analysis by Asset Type

        Identify which Asset_Types were held during periods of maximum drawdown.

        This query:
        1. Calculates portfolio value over time
        2. Identifies drawdown periods
        3. Analyzes asset type exposure during worst drawdowns

        Args:
            backtest_run_id: Specific run ID to analyze, None for all runs

        Returns:
            List of dictionaries with drawdown exposure by asset type
        """

        run_filter = ""
        params = []

        if backtest_run_id:
            run_filter = "WHERE sl.Backtest_Run_ID = %s"
            params = [backtest_run_id]

        query = f"""
        WITH PortfolioReturns AS (
            -- Calculate returns for each selection date
            SELECT
                sl.Backtest_Run_ID,
                sl.Selection_Date,
                sl.Lookback_Period_Days,
                SUM(sl.Holding_Return * sl.Portfolio_Weight) as Period_Return,
                COUNT(*) as Num_Holdings
            FROM Strategy_Log sl
            {run_filter}
                {'AND' if run_filter else 'WHERE'} sl.Holding_Return IS NOT NULL
                AND sl.Portfolio_Rank IS NOT NULL
            GROUP BY sl.Backtest_Run_ID, sl.Selection_Date, sl.Lookback_Period_Days
        ),
        CumulativeReturns AS (
            -- Calculate cumulative returns
            SELECT
                pr.Backtest_Run_ID,
                pr.Selection_Date,
                pr.Period_Return,
                -- Running cumulative return
                SUM(pr.Period_Return) OVER (
                    PARTITION BY pr.Backtest_Run_ID
                    ORDER BY pr.Selection_Date
                ) as Cumulative_Return
            FROM PortfolioReturns pr
        ),
        CumulativeWithPeak AS (
            -- Calculate running maximum (peak) from cumulative returns
            SELECT
                Backtest_Run_ID,
                Selection_Date,
                Cumulative_Return,
                -- Running maximum return (peak)
                MAX(Cumulative_Return) OVER (
                    PARTITION BY Backtest_Run_ID
                    ORDER BY Selection_Date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) as Running_Max_Return
            FROM CumulativeReturns
        ),
        DrawdownPeriods AS (
            -- Calculate drawdown as difference from peak
            SELECT
                Backtest_Run_ID,
                Selection_Date,
                Cumulative_Return,
                Running_Max_Return,
                (Cumulative_Return - Running_Max_Return) as Drawdown
            FROM CumulativeWithPeak
        ),
        MaxDrawdown AS (
            -- Identify the date of maximum drawdown for each run
            SELECT
                dp.Backtest_Run_ID,
                dp.Selection_Date as Max_Drawdown_Date,
                dp.Drawdown as Max_Drawdown_Value
            FROM DrawdownPeriods dp
            INNER JOIN (
                SELECT
                    Backtest_Run_ID,
                    MIN(Drawdown) as Min_Drawdown
                FROM DrawdownPeriods
                GROUP BY Backtest_Run_ID
            ) worst ON dp.Backtest_Run_ID = worst.Backtest_Run_ID
                AND dp.Drawdown = worst.Min_Drawdown
        ),
        AssetTypeExposure AS (
            -- Get asset type holdings during max drawdown periods
            SELECT
                md.Backtest_Run_ID,
                md.Max_Drawdown_Date,
                md.Max_Drawdown_Value,
                sl.Asset_Type,
                COUNT(*) as Num_Holdings,
                AVG(sl.Portfolio_Weight) as Avg_Weight,
                AVG(sl.Holding_Return) as Avg_Return_During_Drawdown,
                SUM(sl.Holding_Return * sl.Portfolio_Weight) as Weighted_Contribution
            FROM MaxDrawdown md
            INNER JOIN Strategy_Log sl ON md.Backtest_Run_ID = sl.Backtest_Run_ID
                AND md.Max_Drawdown_Date = sl.Selection_Date
            WHERE sl.Portfolio_Rank IS NOT NULL
            GROUP BY md.Backtest_Run_ID, md.Max_Drawdown_Date,
                     md.Max_Drawdown_Value, sl.Asset_Type
        )
        SELECT
            Asset_Type,
            COUNT(DISTINCT Backtest_Run_ID) as Num_Occurrences,
            AVG(Num_Holdings) as Avg_Holdings_During_Drawdown,
            ROUND(AVG(Avg_Weight) * 100, 2) as Avg_Weight_Pct,
            ROUND(AVG(Avg_Return_During_Drawdown) * 100, 4) as Avg_Return_During_Drawdown_Pct,
            ROUND(AVG(Weighted_Contribution) * 100, 4) as Avg_Weighted_Contribution_Pct,
            ROUND(AVG(Max_Drawdown_Value) * 100, 2) as Avg_Max_Drawdown_Pct
        FROM AssetTypeExposure
        GROUP BY Asset_Type
        ORDER BY Num_Occurrences DESC, Avg_Weighted_Contribution_Pct ASC
        """

        results = self.db.execute_query_dict(query, tuple(params) if params else None)

        # Print formatted results
        self._print_drawdown_analysis_results(results, backtest_run_id)

        return results

    def _print_drawdown_analysis_results(self, results: List[Dict],
                                        backtest_run_id: Optional[str]):
        """Print formatted drawdown analysis results"""

        print("\n" + "=" * 80)
        print("INSIGHT #3: ASSET TYPE EXPOSURE DURING MAXIMUM DRAWDOWNS")
        print("=" * 80)

        if backtest_run_id:
            print(f"Analysis Scope: Backtest Run ID = {backtest_run_id}")
        else:
            print("Analysis Scope: All backtest runs")

        print("\n" + "-" * 80)
        print(f"{'Asset Type':<15} {'# Times':<10} {'Avg Holdings':<13} "
              f"{'Avg Weight %':<13} {'Contribution %':<15}")
        print("-" * 80)

        for row in results:
            print(f"{row['Asset_Type']:<15} "
                  f"{row['Num_Occurrences']:<10} "
                  f"{row['Avg_Holdings_During_Drawdown']:>12.1f} "
                  f"{row['Avg_Weight_Pct']:>12.2f} "
                  f"{row['Avg_Weighted_Contribution_Pct']:>14.4f}")

        print("-" * 80)

        if results:
            most_common = results[0]
            print(f"\n✓ INSIGHT: '{most_common['Asset_Type']}' was most frequently held "
                  f"during maximum drawdown periods ({most_common['Num_Occurrences']} times)")

            # Find worst contributor
            worst_contributor = min(results, key=lambda x: x['Avg_Weighted_Contribution_Pct'])
            print(f"✓ INSIGHT: '{worst_contributor['Asset_Type']}' had the worst contribution "
                  f"during drawdowns ({worst_contributor['Avg_Weighted_Contribution_Pct']:.4f}%)")

        print("=" * 80)

    # =========================================================================
    # Additional Analytics Methods
    # =========================================================================

    def generate_all_insights(self, start_date: Optional[str] = None,
                             end_date: Optional[str] = None):
        """
        Generate all three insights in sequence

        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
        """

        print("\n" + "=" * 80)
        print("GENERATING ALL ACTIONABLE INSIGHTS")
        print("=" * 80)

        # Insight 1: Volatility
        self.analyze_volatility_by_asset_type(start_date, end_date)

        # Insight 2: Lookback Period Optimization
        self.compare_lookback_periods([90, 180])

        # Insight 3: Drawdown Analysis
        self.analyze_drawdown_exposure()

        print("\n" + "=" * 80)
        print("ALL INSIGHTS GENERATED SUCCESSFULLY")
        print("=" * 80)


# Example usage and testing
def main():
    """Test the analytics module"""
    print("=" * 60)
    print("ETF Backtester - Testing Analytics Module")
    print("=" * 60)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database.")
        return

    # Check if we have data in Strategy_Log
    count = db.get_table_count('Strategy_Log')

    if count == 0:
        print("\n✗ No backtest data found in Strategy_Log table.")
        print("  Please run a backtest first using the backtest_engine module.")
        return

    print(f"\nFound {count} records in Strategy_Log table")

    # Initialize analytics
    analytics = PortfolioAnalytics(db)

    # Generate all insights
    analytics.generate_all_insights()

    # Close connection
    db.close_pool()

    print("\n" + "=" * 60)
    print("Analytics test complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
