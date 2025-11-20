"""
Backtesting Engine Module for ETF Backtester
Implements SQL-focused momentum strategy for ETF selection
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.db_connector import DatabaseConnector


class MomentumBacktester:
    """
    Momentum-based ETF selection strategy using SQL for calculations
    """

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize backtester

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector

    def get_top_etfs_by_momentum(self, selection_date: str, lookback_days: int,
                                 top_n: int = 5) -> List[Dict]:
        """
        Select top N ETFs based on momentum using a complex SQL query
        This is the CORE SQL-FOCUSED function as required

        Args:
            selection_date: Date for selection (YYYY-MM-DD)
            lookback_days: Number of days to look back for momentum calculation
            top_n: Number of top ETFs to select (default 5)

        Returns:
            List of dictionaries containing top ETFs with momentum scores
        """

        # Complex SQL query that calculates momentum entirely in SQL
        query = """
        WITH DateRange AS (
            -- Calculate the lookback date range
            SELECT
                %s as selection_date,
                DATE_SUB(%s, INTERVAL %s DAY) as lookback_date
        ),
        StartPrices AS (
            -- Get the starting price for each ETF at the beginning of lookback period
            SELECT
                pd.ETF_ID,
                pd.Close_Price as Start_Price,
                pd.Price_Date as Start_Date
            FROM Price_Data pd
            INNER JOIN (
                SELECT
                    ETF_ID,
                    MIN(ABS(DATEDIFF(Price_Date, (SELECT lookback_date FROM DateRange)))) as min_diff
                FROM Price_Data
                WHERE Price_Date <= (SELECT selection_date FROM DateRange)
                GROUP BY ETF_ID
            ) closest ON pd.ETF_ID = closest.ETF_ID
                AND ABS(DATEDIFF(pd.Price_Date, (SELECT lookback_date FROM DateRange))) = closest.min_diff
            WHERE pd.Price_Date <= (SELECT selection_date FROM DateRange)
        ),
        EndPrices AS (
            -- Get the ending price for each ETF at the selection date
            SELECT
                pd.ETF_ID,
                pd.Close_Price as End_Price,
                pd.Price_Date as End_Date
            FROM Price_Data pd
            INNER JOIN (
                SELECT
                    ETF_ID,
                    MIN(ABS(DATEDIFF(Price_Date, (SELECT selection_date FROM DateRange)))) as min_diff
                FROM Price_Data
                WHERE Price_Date <= (SELECT selection_date FROM DateRange)
                GROUP BY ETF_ID
            ) closest ON pd.ETF_ID = closest.ETF_ID
                AND ABS(DATEDIFF(pd.Price_Date, (SELECT selection_date FROM DateRange))) = closest.min_diff
            WHERE pd.Price_Date <= (SELECT selection_date FROM DateRange)
        ),
        MomentumScores AS (
            -- Calculate momentum score as percentage return
            SELECT
                em.ETF_ID,
                em.Ticker_Symbol,
                em.ETF_Name,
                em.Asset_Type,
                sp.Start_Price,
                sp.Start_Date,
                ep.End_Price,
                ep.End_Date,
                -- Momentum Score = (End_Price - Start_Price) / Start_Price * 100
                ((ep.End_Price - sp.Start_Price) / sp.Start_Price * 100) as Momentum_Score,
                DATEDIFF(ep.End_Date, sp.Start_Date) as Actual_Days
            FROM ETF_Master em
            INNER JOIN StartPrices sp ON em.ETF_ID = sp.ETF_ID
            INNER JOIN EndPrices ep ON em.ETF_ID = ep.ETF_ID
            WHERE sp.Start_Price > 0  -- Avoid division by zero
        )
        -- Select top N ETFs by momentum score
        SELECT
            ETF_ID,
            Ticker_Symbol,
            ETF_Name,
            Asset_Type,
            Start_Price,
            End_Price,
            Momentum_Score,
            Actual_Days,
            Start_Date,
            End_Date
        FROM MomentumScores
        ORDER BY Momentum_Score DESC
        LIMIT %s
        """

        # Execute the complex SQL query
        results = self.db.execute_query_dict(
            query,
            (selection_date, selection_date, lookback_days, top_n)
        )

        return results

    def log_strategy_selection(self, backtest_run_id: str, selection_date: str,
                              lookback_days: int, selected_etfs: List[Dict]) -> int:
        """
        Log the selected ETFs to Strategy_Log table

        Args:
            backtest_run_id: Unique ID for this backtest run
            selection_date: Date of selection
            lookback_days: Lookback period used
            selected_etfs: List of selected ETFs from get_top_etfs_by_momentum

        Returns:
            Number of records inserted
        """

        if not selected_etfs:
            return 0

        insert_query = """
            INSERT INTO Strategy_Log
            (Backtest_Run_ID, Selection_Date, Lookback_Period_Days,
             ETF_ID, Ticker_Symbol, Asset_Type, Momentum_Score,
             Portfolio_Rank, Portfolio_Weight, Entry_Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Prepare data for batch insert
        num_etfs = len(selected_etfs)
        weight = round(1.0 / num_etfs, 4)  # Equal weight

        data = []
        for rank, etf in enumerate(selected_etfs, start=1):
            data.append((
                backtest_run_id,
                selection_date,
                lookback_days,
                etf['ETF_ID'],
                etf['Ticker_Symbol'],
                etf['Asset_Type'],
                etf['Momentum_Score'],
                rank,
                weight,
                etf['End_Price']  # Entry price is the price at selection date
            ))

        affected = self.db.execute_many(insert_query, data)
        return affected

    def calculate_portfolio_return(self, backtest_run_id: str,
                                   holding_period_days: int) -> Dict:
        """
        Calculate portfolio return for a backtest run using SQL

        Args:
            backtest_run_id: Unique ID for the backtest run
            holding_period_days: Number of days to hold the portfolio

        Returns:
            Dictionary with portfolio performance metrics
        """

        # SQL query to calculate returns for each held ETF
        query = """
        WITH HoldingPeriod AS (
            SELECT
                sl.Log_ID,
                sl.ETF_ID,
                sl.Ticker_Symbol,
                sl.Selection_Date,
                sl.Entry_Price,
                sl.Portfolio_Weight,
                DATE_ADD(sl.Selection_Date, INTERVAL %s DAY) as Target_Exit_Date
            FROM Strategy_Log sl
            WHERE sl.Backtest_Run_ID = %s
                AND sl.Portfolio_Rank IS NOT NULL
        ),
        ExitPrices AS (
            SELECT
                hp.Log_ID,
                hp.ETF_ID,
                hp.Entry_Price,
                hp.Portfolio_Weight,
                pd.Close_Price as Exit_Price,
                pd.Price_Date as Actual_Exit_Date,
                -- Calculate return for this ETF
                ((pd.Close_Price - hp.Entry_Price) / hp.Entry_Price) as ETF_Return
            FROM HoldingPeriod hp
            INNER JOIN Price_Data pd ON hp.ETF_ID = pd.ETF_ID
            INNER JOIN (
                -- Get the closest price date to target exit date
                SELECT
                    hp2.ETF_ID,
                    MIN(ABS(DATEDIFF(pd2.Price_Date, hp2.Target_Exit_Date))) as min_diff
                FROM HoldingPeriod hp2
                INNER JOIN Price_Data pd2 ON hp2.ETF_ID = pd2.ETF_ID
                WHERE pd2.Price_Date >= hp2.Selection_Date
                GROUP BY hp2.ETF_ID
            ) closest ON pd.ETF_ID = closest.ETF_ID
                AND ABS(DATEDIFF(pd.Price_Date, hp.Target_Exit_Date)) = closest.min_diff
            WHERE pd.Price_Date >= hp.Selection_Date
        )
        SELECT
            Log_ID,
            ETF_ID,
            Entry_Price,
            Exit_Price,
            Portfolio_Weight,
            ETF_Return,
            Actual_Exit_Date,
            -- Weighted return contribution
            (ETF_Return * Portfolio_Weight) as Weighted_Return
        FROM ExitPrices
        """

        results = self.db.execute_query_dict(query, (holding_period_days, backtest_run_id))

        if not results:
            return {
                'total_return': 0.0,
                'num_positions': 0,
                'avg_return': 0.0
            }

        # Update Strategy_Log with exit prices and returns
        update_query = """
            UPDATE Strategy_Log
            SET Exit_Price = %s,
                Holding_Return = %s
            WHERE Log_ID = %s
        """

        update_data = [
            (row['Exit_Price'], row['ETF_Return'], row['Log_ID'])
            for row in results
        ]

        self.db.execute_many(update_query, update_data)

        # Calculate portfolio metrics (convert Decimal to float)
        total_return = float(sum(row['Weighted_Return'] for row in results))
        num_positions = len(results)
        avg_return = float(sum(row['ETF_Return'] for row in results)) / num_positions if num_positions > 0 else 0

        return {
            'total_return': total_return,
            'num_positions': num_positions,
            'avg_return': avg_return,
            'positions': results
        }

    def run_backtest(self, start_date: str, end_date: str,
                    lookback_days: int = 90,
                    holding_period_days: int = 30,
                    rebalance_days: int = 30,
                    top_n: int = 5) -> Dict:
        """
        Run a complete backtest over a date range

        Args:
            start_date: Start date for backtest (YYYY-MM-DD)
            end_date: End date for backtest (YYYY-MM-DD)
            lookback_days: Lookback period for momentum calculation
            holding_period_days: How long to hold positions
            rebalance_days: How often to rebalance (select new portfolio)
            top_n: Number of ETFs to select

        Returns:
            Dictionary with backtest results
        """

        print("\n" + "=" * 60)
        print("Running Momentum Strategy Backtest")
        print("=" * 60)

        # Generate unique run ID
        run_id = f"RUN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        print(f"Backtest Run ID: {run_id}")
        print(f"Date Range: {start_date} to {end_date}")
        print(f"Lookback Period: {lookback_days} days")
        print(f"Holding Period: {holding_period_days} days")
        print(f"Rebalance Frequency: {rebalance_days} days")
        print(f"Portfolio Size: Top {top_n} ETFs")
        print("\n" + "-" * 60)

        # Convert dates
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        all_selections = []
        all_returns = []

        while current_date <= end_dt:
            selection_date_str = current_date.strftime('%Y-%m-%d')

            print(f"\nRebalance Date: {selection_date_str}")

            # Select top ETFs using SQL
            top_etfs = self.get_top_etfs_by_momentum(
                selection_date_str,
                lookback_days,
                top_n
            )

            if not top_etfs:
                print(f"  ⚠ No ETFs found for date {selection_date_str}, skipping...")
                current_date += timedelta(days=rebalance_days)
                continue

            print(f"  ✓ Selected {len(top_etfs)} ETFs")

            # Display selected ETFs
            for i, etf in enumerate(top_etfs, 1):
                print(f"    {i}. {etf['Ticker_Symbol']:6s} ({etf['Asset_Type']:10s}) "
                      f"| Momentum: {etf['Momentum_Score']:6.2f}% "
                      f"| Price: ${etf['End_Price']:.2f}")

            # Log selection
            logged = self.log_strategy_selection(
                run_id,
                selection_date_str,
                lookback_days,
                top_etfs
            )

            print(f"  ✓ Logged {logged} selections to database")

            # Calculate returns for this holding period
            returns = self.calculate_portfolio_return(run_id, holding_period_days)

            if returns['num_positions'] > 0:
                print(f"  ✓ Portfolio Return: {returns['total_return']*100:.2f}%")
                all_returns.append(returns['total_return'])

            all_selections.extend(top_etfs)

            # Move to next rebalance date
            current_date += timedelta(days=rebalance_days)

        # Calculate overall statistics
        print("\n" + "=" * 60)
        print("Backtest Complete!")
        print("=" * 60)

        total_rebalances = len(all_returns)
        cumulative_return = float(sum(all_returns))
        avg_return_per_period = cumulative_return / total_rebalances if total_rebalances > 0 else 0

        # Calculate CAGR (approximate) - convert to float for power operation
        days_elapsed = (end_dt - datetime.strptime(start_date, '%Y-%m-%d')).days
        years = days_elapsed / 365.25
        cagr = ((1 + cumulative_return) ** (1 / years) - 1) if years > 0 else 0

        results = {
            'run_id': run_id,
            'start_date': start_date,
            'end_date': end_date,
            'lookback_days': lookback_days,
            'holding_period_days': holding_period_days,
            'rebalance_days': rebalance_days,
            'top_n': top_n,
            'total_rebalances': total_rebalances,
            'cumulative_return': cumulative_return,
            'avg_return_per_period': avg_return_per_period,
            'cagr': cagr,
            'all_returns': all_returns
        }

        print(f"\nTotal Rebalances: {total_rebalances}")
        print(f"Cumulative Return: {cumulative_return*100:.2f}%")
        print(f"Avg Return per Period: {avg_return_per_period*100:.2f}%")
        print(f"Approximate CAGR: {cagr*100:.2f}%")

        return results

    def get_available_date_range(self) -> Dict:
        """
        Get the available date range from Price_Data

        Returns:
            Dictionary with min_date and max_date
        """
        query = """
            SELECT
                MIN(Price_Date) as min_date,
                MAX(Price_Date) as max_date
            FROM Price_Data
        """
        result = self.db.execute_query_dict(query)

        if result:
            return {
                'min_date': result[0]['min_date'],
                'max_date': result[0]['max_date']
            }
        return {'min_date': None, 'max_date': None}


# Example usage and testing
def main():
    """Test the backtest engine"""
    print("=" * 60)
    print("ETF Backtester - Testing Backtest Engine")
    print("=" * 60)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database.")
        return

    # Initialize backtester
    backtester = MomentumBacktester(db)

    # Get available date range
    date_range = backtester.get_available_date_range()
    print(f"\nAvailable data range: {date_range['min_date']} to {date_range['max_date']}")

    if date_range['min_date'] and date_range['max_date']:
        # Run a sample backtest (6 months)
        start = datetime.strptime(str(date_range['min_date']), '%Y-%m-%d') + timedelta(days=180)
        end = datetime.strptime(str(date_range['max_date']), '%Y-%m-%d') - timedelta(days=30)

        results = backtester.run_backtest(
            start_date=start.strftime('%Y-%m-%d'),
            end_date=end.strftime('%Y-%m-%d'),
            lookback_days=90,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

        print("\n" + "=" * 60)
        print("Test Complete!")
        print("=" * 60)

    # Close connection
    db.close_pool()


if __name__ == "__main__":
    main()
