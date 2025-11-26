"""
Analytics Module
Provides portfolio analysis and insights
"""

import pandas as pd
import matplotlib.pyplot as plt


class PortfolioAnalytics:
    """
    Portfolio Analytics and Insights Generator
    """

    def __init__(self, db_connector):
        self.db = db_connector

    def analyze_volatility_by_asset_type(self):
        """Calculate volatility metrics by asset type"""
        query = """
        SELECT
            em.Asset_Type,
            STDDEV(pd.Daily_Return) * 100 as Daily_Vol,
            STDDEV(pd.Daily_Return) * SQRT(5) * 100 as Weekly_Vol,
            STDDEV(pd.Daily_Return) * SQRT(252) * 100 as Annual_Vol
        FROM Price_Data pd
        JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
        WHERE pd.Daily_Return IS NOT NULL
        GROUP BY em.Asset_Type
        ORDER BY Annual_Vol DESC
        """

        results = self.db.execute_query_dict(query)

        print(f"\n{'=' * 80}")
        print("VOLATILITY ANALYSIS BY ASSET TYPE")
        print(f"{'=' * 80}\n")

        if results:
            df = pd.DataFrame(results)
            df.columns = ['Asset_Type', 'Daily_Volatility_Pct',
                         'Weekly_Volatility_Pct', 'Annualized_Volatility_Pct']

            print(df.to_string(index=False))
            return results
        return None

    def compare_lookback_periods(self, lookback_periods=[90, 180]):
        """Compare different lookback periods"""
        print(f"\n{'=' * 80}")
        print(f"LOOKBACK PERIOD COMPARISON")
        print(f"{'=' * 80}\n")

        for period in lookback_periods:
            query = """
            SELECT AVG(Momentum_Score) as Avg_Momentum
            FROM Strategy_Log
            WHERE Backtest_Run_ID LIKE %s
            """

            results = self.db.execute_query_dict(query, (f'%{period}%',))
            if results:
                print(f"  {period}-day lookback: Avg Momentum = {results[0]['Avg_Momentum']:.2f}%")

    def analyze_drawdown_exposure(self):
        """Analyze drawdown patterns"""
        query = """
        SELECT
            em.Ticker_Symbol,
            em.Asset_Type,
            MIN(pd.Daily_Return) * 100 as Max_Single_Day_Loss,
            AVG(CASE WHEN pd.Daily_Return < 0
                THEN pd.Daily_Return ELSE NULL END) * 100 as Avg_Down_Day
        FROM Price_Data pd
        JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
        WHERE pd.Daily_Return IS NOT NULL
        GROUP BY em.Ticker_Symbol, em.Asset_Type
        ORDER BY Max_Single_Day_Loss
        LIMIT 10
        """

        results = self.db.execute_query_dict(query)

        print(f"\n{'=' * 80}")
        print("TOP 10 WORST SINGLE-DAY LOSSES")
        print(f"{'=' * 80}\n")

        if results:
            df = pd.DataFrame(results)
            print(df.to_string(index=False))

    def generate_all_insights(self):
        """Generate all analytics insights"""
        print(f"\n{'=' * 80}")
        print("GENERATING ALL ANALYTICS INSIGHTS")
        print(f"{'=' * 80}")

        self.analyze_volatility_by_asset_type()
        self.analyze_drawdown_exposure()
        self.compare_lookback_periods()

        print(f"\n{'=' * 80}")
        print("✓ All insights generated successfully!")
        print(f"{'=' * 80}")
