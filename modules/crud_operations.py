"""
CRUD Operations Module
Handles Create, Read, Update, Delete operations
"""

import pandas as pd
from IPython.display import display


class CRUDOperations:
    """
    CRUD Operations for ETF Backtester
    """

    def __init__(self, db_connector):
        self.db = db_connector

    # ========== READ OPERATIONS ==========

    def read_backtest_results(self, limit=50):
        """Read latest backtest results"""
        query = """
        SELECT
            sl.Backtest_Run_ID,
            sl.Run_Date,
            sl.Selection_Date,
            em.Ticker_Symbol,
            em.ETF_Name,
            sl.Asset_Type,
            sl.Momentum_Score,
            sl.Portfolio_Rank,
            sl.Holding_Return
        FROM Strategy_Log sl
        JOIN ETF_Master em ON sl.ETF_ID = em.ETF_ID
        WHERE sl.Backtest_Run_ID = (
            SELECT Backtest_Run_ID FROM Strategy_Log
            ORDER BY Run_Date DESC LIMIT 1
        )
        ORDER BY sl.Selection_Date DESC, sl.Portfolio_Rank
        LIMIT %s
        """

        results = self.db.execute_query_dict(query, (limit,))

        if results:
            df = pd.DataFrame(results)
            print(f"\n{'=' * 80}")
            print(f"LATEST BACKTEST RESULTS")
            print(f"{'=' * 80}\n")
            display(df)
            return results
        else:
            print("\n⚠️  No backtest results found. Run a backtest first.")
            return None

    def read_all_backtest_runs(self):
        """Read summary of all backtest runs"""
        query = """
        SELECT
            Backtest_Run_ID,
            MIN(Run_Date) as Run_Date,
            COUNT(*) as Total_Selections,
            COUNT(DISTINCT Selection_Date) as Rebalance_Count,
            AVG(Momentum_Score) as Avg_Momentum,
            MIN(Selection_Date) as Start_Date,
            MAX(Selection_Date) as End_Date
        FROM Strategy_Log
        GROUP BY Backtest_Run_ID
        ORDER BY Run_Date DESC
        """

        results = self.db.execute_query_dict(query)

        if results:
            df = pd.DataFrame(results)
            print(f"\n{'=' * 80}")
            print(f"ALL BACKTEST RUNS")
            print(f"{'=' * 80}\n")
            display(df)
        else:
            print("\n⚠️  No backtest runs found.")

    def read_etf_info(self):
        """Read ETF master information"""
        query = """
        SELECT
            ETF_ID,
            Ticker_Symbol,
            ETF_Name,
            Asset_Type,
            Created_At,
            Updated_At
        FROM ETF_Master
        ORDER BY Ticker_Symbol
        """

        results = self.db.execute_query_dict(query)

        if results:
            df = pd.DataFrame(results)
            print(f"\n{'=' * 80}")
            print(f"ETF MASTER INFORMATION")
            print(f"{'=' * 80}\n")
            print(f"Total ETFs: {len(df)}\n")
            display(df)
            return results
        else:
            print("\n⚠️  No ETF information found.")
            return None

    # ========== UPDATE OPERATIONS ==========

    def update_etf_info(self, etf_id, field_name, new_value):
        """
        Update specific field in ETF_Master table

        Args:
            etf_id: ETF ID to update
            field_name: Column name to update (Ticker_Symbol, ETF_Name, or Asset_Type)
            new_value: New value for the field
        """
        allowed_fields = ['Ticker_Symbol', 'ETF_Name', 'Asset_Type']

        if field_name not in allowed_fields:
            print(f"\n❌ Error: Invalid field name '{field_name}'")
            print(f"   Allowed fields: {', '.join(allowed_fields)}")
            return False

        query = f"""
        UPDATE ETF_Master
        SET {field_name} = %s, Updated_At = NOW()
        WHERE ETF_ID = %s
        """

        try:
            affected_rows = self.db.execute_update(query, (new_value, etf_id))

            if affected_rows > 0:
                print(f"\n✅ Successfully updated!")
                print(f"   ETF_ID: {etf_id}")
                print(f"   Field: {field_name}")
                print(f"   New Value: {new_value}")
                return True
            else:
                print(f"\n⚠️  No ETF found with ID: {etf_id}")
                return False

        except Exception as e:
            print(f"\n❌ Update failed: {e}")
            return False

    def update_etf_interactive(self):
        """
        Interactive ETF information update with live demo
        Allows users to select and update ETF information
        """
        print(f"\n{'=' * 80}")
        print("3.4 - UPDATE ETF INFORMATION (LIVE EDIT)")
        print(f"{'=' * 80}\n")

        # Step 1: Display current ETF information
        print("📋 Current ETF Information:\n")
        etf_list = self.read_etf_info()

        if not etf_list:
            print("\n⚠️  No ETFs available to update.")
            return

        # Step 2: Get user input for ETF selection
        print(f"\n{'-' * 80}")
        etf_id_input = input("👉 Enter ETF_ID to update (or 'cancel' to go back): ").strip()

        if etf_id_input.lower() == 'cancel':
            print("❌ Update cancelled.")
            return

        try:
            etf_id = int(etf_id_input)
        except ValueError:
            print("❌ Invalid ETF_ID. Must be a number.")
            return

        # Verify ETF exists and show current values
        etf_data = next((etf for etf in etf_list if etf['ETF_ID'] == etf_id), None)

        if not etf_data:
            print(f"❌ ETF_ID {etf_id} not found.")
            return

        print(f"\n📌 Selected ETF:")
        print(f"   ETF_ID: {etf_data['ETF_ID']}")
        print(f"   Ticker: {etf_data['Ticker_Symbol']}")
        print(f"   Name: {etf_data['ETF_Name']}")
        print(f"   Asset Type: {etf_data['Asset_Type']}")

        # Step 3: Select field to update
        print(f"\n{'-' * 80}")
        print("📝 Which field do you want to update?")
        print("   1 - Ticker Symbol")
        print("   2 - ETF Name")
        print("   3 - Asset Type")
        print("   0 - Cancel")

        field_choice = input("\n👉 Enter choice (1-3): ").strip()

        field_mapping = {
            '1': ('Ticker_Symbol', etf_data['Ticker_Symbol']),
            '2': ('ETF_Name', etf_data['ETF_Name']),
            '3': ('Asset_Type', etf_data['Asset_Type'])
        }

        if field_choice == '0':
            print("❌ Update cancelled.")
            return

        if field_choice not in field_mapping:
            print("❌ Invalid choice.")
            return

        field_name, current_value = field_mapping[field_choice]

        # Step 4: Get new value
        print(f"\n{'-' * 80}")
        print(f"Current value: {current_value}")

        if field_name == 'Asset_Type':
            print("\n💡 Available Asset Types: Equity, Fixed Income, Commodity, Real Estate, Currency")

        new_value = input(f"👉 Enter new value for {field_name}: ").strip()

        if not new_value:
            print("❌ Empty value not allowed.")
            return

        # Step 5: Confirm update
        print(f"\n{'-' * 80}")
        print("⚠️  CONFIRMATION")
        print(f"   ETF ID: {etf_id}")
        print(f"   Field: {field_name}")
        print(f"   Old Value: {current_value}")
        print(f"   New Value: {new_value}")

        confirm = input("\n👉 Proceed with update? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("❌ Update cancelled.")
            return

        # Step 6: Execute update
        success = self.update_etf_info(etf_id, field_name, new_value)

        # Step 7: Show updated information
        if success:
            print(f"\n{'-' * 80}")
            print("📊 Updated ETF Information:\n")

            query = """
            SELECT ETF_ID, Ticker_Symbol, ETF_Name, Asset_Type, Updated_At
            FROM ETF_Master
            WHERE ETF_ID = %s
            """

            updated_data = self.db.execute_query_dict(query, (etf_id,))

            if updated_data:
                df = pd.DataFrame(updated_data)
                display(df)

                print(f"\n✅ Update completed successfully!")
                print(f"   Last Updated: {updated_data[0]['Updated_At']}")

    def batch_update_asset_type(self, ticker_symbol, new_asset_type):
        """
        Batch update asset type for specific ticker
        Useful for correcting multiple records
        """
        query = """
        UPDATE ETF_Master
        SET Asset_Type = %s, Updated_At = NOW()
        WHERE Ticker_Symbol = %s
        """

        try:
            affected_rows = self.db.execute_update(query, (new_asset_type, ticker_symbol))
            print(f"✅ Updated {affected_rows} record(s) for {ticker_symbol}")
            return affected_rows
        except Exception as e:
            print(f"❌ Batch update failed: {e}")
            return 0

    # ========== DELETE OPERATIONS (Optional) ==========

    def delete_backtest_run(self, backtest_run_id):
        """Delete specific backtest run (use with caution)"""
        query = "DELETE FROM Strategy_Log WHERE Backtest_Run_ID = %s"

        confirm = input(f"\n⚠️  Delete backtest run '{backtest_run_id}'? (yes/no): ").strip().lower()

        if confirm == 'yes':
            try:
                affected_rows = self.db.execute_update(query, (backtest_run_id,))
                print(f"✅ Deleted {affected_rows} records from backtest run.")
                return True
            except Exception as e:
                print(f"❌ Delete failed: {e}")
                return False
        else:
            print("❌ Delete cancelled.")
            return False
