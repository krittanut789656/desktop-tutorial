"""
CRUD Operations Module for ETF Backtester
Implements Create, Read, Update, Delete operations for database management
"""

import sys
import os
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.db_connector import DatabaseConnector


class CRUDOperations:
    """
    CRUD operations for managing ETF backtester data
    """

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize CRUD operations

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector

    # =========================================================================
    # READ Operations
    # =========================================================================

    def read_backtest_results(self, backtest_run_id: Optional[str] = None,
                             limit: int = 100) -> List[Dict]:
        """
        READ: Display backtest results from Strategy_Log table

        Args:
            backtest_run_id: Specific run ID to read, None for latest
            limit: Maximum number of records to return

        Returns:
            List of dictionaries containing backtest results
        """

        print("\n" + "=" * 80)
        print("READ: BACKTEST RESULTS FROM STRATEGY_LOG")
        print("=" * 80)

        if backtest_run_id:
            query = """
                SELECT
                    Log_ID,
                    Backtest_Run_ID,
                    Run_Date,
                    Strategy_Name,
                    Lookback_Period_Days,
                    Selection_Date,
                    Ticker_Symbol,
                    Asset_Type,
                    Momentum_Score,
                    Portfolio_Rank,
                    Portfolio_Weight,
                    Entry_Price,
                    Exit_Price,
                    Holding_Return
                FROM Strategy_Log
                WHERE Backtest_Run_ID = %s
                ORDER BY Selection_Date, Portfolio_Rank
                LIMIT %s
            """
            results = self.db.execute_query_dict(query, (backtest_run_id, limit))
            print(f"\nShowing results for Run ID: {backtest_run_id}")

        else:
            # Get latest run
            latest_query = """
                SELECT Backtest_Run_ID
                FROM Strategy_Log
                ORDER BY Run_Date DESC
                LIMIT 1
            """
            latest = self.db.execute_query_dict(latest_query)

            if not latest:
                print("\n✗ No backtest results found in database.")
                return []

            run_id = latest[0]['Backtest_Run_ID']

            query = """
                SELECT
                    Log_ID,
                    Backtest_Run_ID,
                    Run_Date,
                    Strategy_Name,
                    Lookback_Period_Days,
                    Selection_Date,
                    Ticker_Symbol,
                    Asset_Type,
                    Momentum_Score,
                    Portfolio_Rank,
                    Portfolio_Weight,
                    Entry_Price,
                    Exit_Price,
                    Holding_Return
                FROM Strategy_Log
                WHERE Backtest_Run_ID = %s
                ORDER BY Selection_Date, Portfolio_Rank
                LIMIT %s
            """
            results = self.db.execute_query_dict(query, (run_id, limit))
            print(f"\nShowing results for latest Run ID: {run_id}")

        # Display results
        if results:
            print(f"Total Records: {len(results)}\n")
            print("-" * 80)

            # Group by selection date for better readability
            current_date = None

            for row in results:
                if row['Selection_Date'] != current_date:
                    current_date = row['Selection_Date']
                    print(f"\nSelection Date: {current_date} "
                          f"(Lookback: {row['Lookback_Period_Days']} days)")
                    print("-" * 80)

                return_str = f"{row['Holding_Return']*100:6.2f}%" if row['Holding_Return'] else "N/A"

                print(f"  {row['Portfolio_Rank']}.  {row['Ticker_Symbol']:6s} "
                      f"({row['Asset_Type']:10s}) | "
                      f"Momentum: {row['Momentum_Score']:7.2f}% | "
                      f"Entry: ${row['Entry_Price']:7.2f} | "
                      f"Exit: ${row['Exit_Price'] if row['Exit_Price'] else 'N/A':>7} | "
                      f"Return: {return_str:>7}")

            print("\n" + "=" * 80)

        else:
            print("\n✗ No results found.")

        return results

    def read_all_backtest_runs(self) -> List[Dict]:
        """
        READ: Display all backtest run summaries

        Returns:
            List of dictionaries with run summaries
        """

        print("\n" + "=" * 80)
        print("READ: ALL BACKTEST RUNS")
        print("=" * 80)

        query = """
            SELECT
                Backtest_Run_ID,
                MIN(Run_Date) as Run_Date,
                Strategy_Name,
                Lookback_Period_Days,
                MIN(Selection_Date) as Start_Date,
                MAX(Selection_Date) as End_Date,
                COUNT(DISTINCT Selection_Date) as Num_Rebalances,
                COUNT(*) as Total_Selections,
                AVG(Holding_Return) as Avg_Return,
                SUM(Holding_Return * Portfolio_Weight) / COUNT(DISTINCT Selection_Date) as Weighted_Avg_Return
            FROM Strategy_Log
            WHERE Portfolio_Rank IS NOT NULL
            GROUP BY Backtest_Run_ID, Strategy_Name, Lookback_Period_Days
            ORDER BY Run_Date DESC
        """

        results = self.db.execute_query_dict(query)

        if results:
            print(f"\nTotal Backtest Runs: {len(results)}\n")
            print("-" * 80)
            print(f"{'Run ID':<30} {'Date Range':<25} {'Lookback':<10} {'Rebal':<8} {'Avg Return':<12}")
            print("-" * 80)

            for row in results:
                date_range = f"{row['Start_Date']} to {row['End_Date']}"
                avg_return = f"{row['Weighted_Avg_Return']*100:6.2f}%" if row['Weighted_Avg_Return'] else "N/A"

                print(f"{row['Backtest_Run_ID']:<30} "
                      f"{date_range:<25} "
                      f"{row['Lookback_Period_Days']:<10} "
                      f"{row['Num_Rebalances']:<8} "
                      f"{avg_return:<12}")

            print("=" * 80)

        else:
            print("\n✗ No backtest runs found.")

        return results

    def read_etf_info(self, ticker: Optional[str] = None) -> List[Dict]:
        """
        READ: Display ETF information

        Args:
            ticker: Specific ticker symbol, None for all ETFs

        Returns:
            List of dictionaries with ETF info
        """

        print("\n" + "=" * 80)
        print("READ: ETF MASTER INFORMATION")
        print("=" * 80)

        if ticker:
            query = """
                SELECT
                    ETF_ID,
                    Ticker_Symbol,
                    ETF_Name,
                    Asset_Type,
                    Expense_Ratio,
                    Inception_Date
                FROM ETF_Master
                WHERE Ticker_Symbol = %s
            """
            results = self.db.execute_query_dict(query, (ticker.upper(),))
            print(f"\nShowing information for: {ticker.upper()}")

        else:
            query = """
                SELECT
                    ETF_ID,
                    Ticker_Symbol,
                    ETF_Name,
                    Asset_Type,
                    Expense_Ratio,
                    Inception_Date
                FROM ETF_Master
                ORDER BY Asset_Type, Ticker_Symbol
                LIMIT 50
            """
            results = self.db.execute_query_dict(query)
            print("\nShowing all ETFs (max 50):")

        if results:
            print(f"\nTotal ETFs: {len(results)}\n")
            print("-" * 80)
            print(f"{'Ticker':<8} {'Asset Type':<12} {'Name':<40} {'Expense %':<12}")
            print("-" * 80)

            for row in results:
                print(f"{row['Ticker_Symbol']:<8} "
                      f"{row['Asset_Type']:<12} "
                      f"{row['ETF_Name']:<40} "
                      f"{row['Expense_Ratio']:.4f}")

            print("=" * 80)

        else:
            print("\n✗ No ETF information found.")

        return results

    # =========================================================================
    # UPDATE Operations
    # =========================================================================

    def update_price_data(self, etf_id: int, price_date: str,
                         new_close_price: float) -> bool:
        """
        UPDATE: Update a specific price record

        Args:
            etf_id: ETF ID
            price_date: Date of price (YYYY-MM-DD)
            new_close_price: New closing price

        Returns:
            bool: True if successful, False otherwise
        """

        print("\n" + "=" * 80)
        print("UPDATE: PRICE DATA")
        print("=" * 80)

        # First, read current value
        read_query = """
            SELECT
                pd.Price_ID,
                em.Ticker_Symbol,
                pd.Price_Date,
                pd.Close_Price
            FROM Price_Data pd
            INNER JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
            WHERE pd.ETF_ID = %s AND pd.Price_Date = %s
        """

        current = self.db.execute_query_dict(read_query, (etf_id, price_date))

        if not current:
            print(f"\n✗ No price data found for ETF_ID={etf_id} on date={price_date}")
            return False

        old_price = current[0]['Close_Price']
        ticker = current[0]['Ticker_Symbol']

        print(f"\nUpdating price for {ticker} on {price_date}")
        print(f"  Old Price: ${old_price:.2f}")
        print(f"  New Price: ${new_close_price:.2f}")

        # Update the price
        update_query = """
            UPDATE Price_Data
            SET Close_Price = %s,
                Adj_Close_Price = %s
            WHERE ETF_ID = %s AND Price_Date = %s
        """

        try:
            self.db.execute_query(update_query, (new_close_price, new_close_price,
                                                 etf_id, price_date))
            print("\n✓ Price updated successfully!")
            print("=" * 80)
            return True

        except Exception as e:
            print(f"\n✗ Error updating price: {e}")
            print("=" * 80)
            return False

    def update_strategy_log_notes(self, log_id: int, notes: str) -> bool:
        """
        UPDATE: Update notes field in Strategy_Log

        Args:
            log_id: Log ID
            notes: Notes text to add

        Returns:
            bool: True if successful, False otherwise
        """

        print("\n" + "=" * 80)
        print("UPDATE: STRATEGY LOG NOTES")
        print("=" * 80)

        # Check if log exists
        read_query = """
            SELECT
                Log_ID,
                Ticker_Symbol,
                Selection_Date,
                Notes
            FROM Strategy_Log
            WHERE Log_ID = %s
        """

        current = self.db.execute_query_dict(read_query, (log_id,))

        if not current:
            print(f"\n✗ No strategy log found with Log_ID={log_id}")
            return False

        ticker = current[0]['Ticker_Symbol']
        date = current[0]['Selection_Date']
        old_notes = current[0]['Notes'] or "(empty)"

        print(f"\nUpdating notes for {ticker} on {date}")
        print(f"  Old Notes: {old_notes}")
        print(f"  New Notes: {notes}")

        # Update notes
        update_query = """
            UPDATE Strategy_Log
            SET Notes = %s
            WHERE Log_ID = %s
        """

        try:
            self.db.execute_query(update_query, (notes, log_id))
            print("\n✓ Notes updated successfully!")
            print("=" * 80)
            return True

        except Exception as e:
            print(f"\n✗ Error updating notes: {e}")
            print("=" * 80)
            return False

    # =========================================================================
    # DELETE Operations
    # =========================================================================

    def delete_old_backtest_logs(self, days_old: int = 90) -> int:
        """
        DELETE: Remove old backtest logs from Strategy_Log table

        Args:
            days_old: Delete logs older than this many days

        Returns:
            Number of records deleted
        """

        print("\n" + "=" * 80)
        print("DELETE: OLD BACKTEST LOGS")
        print("=" * 80)

        # First, count how many will be deleted
        count_query = """
            SELECT COUNT(*) as count
            FROM Strategy_Log
            WHERE Run_Date < DATE_SUB(NOW(), INTERVAL %s DAY)
        """

        count_result = self.db.execute_query_dict(count_query, (days_old,))
        count = count_result[0]['count'] if count_result else 0

        if count == 0:
            print(f"\n✓ No logs older than {days_old} days found.")
            print("=" * 80)
            return 0

        print(f"\nFound {count} log(s) older than {days_old} days")

        # Show what will be deleted
        show_query = """
            SELECT
                Backtest_Run_ID,
                Run_Date,
                COUNT(*) as Num_Records
            FROM Strategy_Log
            WHERE Run_Date < DATE_SUB(NOW(), INTERVAL %s DAY)
            GROUP BY Backtest_Run_ID, Run_Date
            ORDER BY Run_Date
        """

        to_delete = self.db.execute_query_dict(show_query, (days_old,))

        print("\nThe following runs will be deleted:")
        print("-" * 80)
        for row in to_delete:
            print(f"  - {row['Backtest_Run_ID']}: {row['Run_Date']} ({row['Num_Records']} records)")

        # Perform deletion
        delete_query = """
            DELETE FROM Strategy_Log
            WHERE Run_Date < DATE_SUB(NOW(), INTERVAL %s DAY)
        """

        try:
            self.db.execute_query(delete_query, (days_old,))
            print(f"\n✓ Successfully deleted {count} old log record(s)!")
            print("=" * 80)
            return count

        except Exception as e:
            print(f"\n✗ Error deleting logs: {e}")
            print("=" * 80)
            return 0

    def delete_backtest_run(self, backtest_run_id: str) -> int:
        """
        DELETE: Remove a specific backtest run

        Args:
            backtest_run_id: Run ID to delete

        Returns:
            Number of records deleted
        """

        print("\n" + "=" * 80)
        print("DELETE: SPECIFIC BACKTEST RUN")
        print("=" * 80)

        # Count records
        count_query = """
            SELECT COUNT(*) as count
            FROM Strategy_Log
            WHERE Backtest_Run_ID = %s
        """

        count_result = self.db.execute_query_dict(count_query, (backtest_run_id,))
        count = count_result[0]['count'] if count_result else 0

        if count == 0:
            print(f"\n✗ No backtest run found with ID: {backtest_run_id}")
            print("=" * 80)
            return 0

        print(f"\nFound {count} record(s) for Run ID: {backtest_run_id}")

        # Delete
        delete_query = """
            DELETE FROM Strategy_Log
            WHERE Backtest_Run_ID = %s
        """

        try:
            self.db.execute_query(delete_query, (backtest_run_id,))
            print(f"\n✓ Successfully deleted {count} record(s)!")
            print("=" * 80)
            return count

        except Exception as e:
            print(f"\n✗ Error deleting run: {e}")
            print("=" * 80)
            return 0


# Example usage and testing
def main():
    """Test CRUD operations"""
    print("=" * 60)
    print("ETF Backtester - Testing CRUD Operations")
    print("=" * 60)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database.")
        return

    # Initialize CRUD operations
    crud = CRUDOperations(db)

    # Test READ operations
    print("\n### Testing READ Operations ###")

    # Read all backtest runs
    crud.read_all_backtest_runs()

    # Read latest backtest results
    crud.read_backtest_results(limit=10)

    # Read ETF info
    crud.read_etf_info()

    # Close connection
    db.close_pool()

    print("\n" + "=" * 60)
    print("CRUD operations test complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
