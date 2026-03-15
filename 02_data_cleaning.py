"""
=============================================================================
02_data_cleaning.py
DADS 5001 Mini-Project: Energy Sector Analysis & Macro Crisis (2000-2026)
Phase 2: Data Cleaning, Feature Engineering & Currency Adjustment
=============================================================================
"""

import os
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Configuration ────────────────────────────────────────────────────────────

RAW_FILE = "data/raw/energy_macro_raw.xlsx"
CLEANED_DIR = "data/cleaned"
CLEANED_FILE = os.path.join(CLEANED_DIR, "energy_macro_cleaned.xlsx")

BASE_YEAR = 2000  # Index base year for normalization (= 100)

CRISIS_MAP = [
    ("2000-03-01", "2003-03-01", "Dot-com/Oil Spike"),
    ("2003-03-02", "2007-09-30", "Pre-Crisis Boom"),
    ("2007-10-01", "2009-06-30", "Great Recession"),
    ("2009-07-01", "2014-05-31", "Recovery/QE Era"),
    ("2014-06-01", "2016-02-29", "Shale Revolution"),
    ("2016-03-01", "2019-12-31", "Stabilization"),
    ("2020-01-01", "2020-12-31", "COVID-19"),
    ("2021-01-01", "2022-02-23", "Post-COVID Recovery"),
    ("2022-02-24", "2023-12-31", "Russia-Ukraine War"),
    ("2024-01-01", "2025-05-31", "Normalization"),
    ("2025-06-01", "2026-12-31", "Iran Crisis 2025-26"),
]

ROLLING_WINDOW = 20  # weeks for rolling volatility


# ── Helper Functions ─────────────────────────────────────────────────────────

def load_raw_data():
    """Load all sheets from the raw Excel file."""
    print("  Loading raw data...")
    us = pd.read_excel(RAW_FILE, sheet_name="US_Energy_Stocks", index_col=0, parse_dates=True)
    th = pd.read_excel(RAW_FILE, sheet_name="TH_Energy_Stocks", index_col=0, parse_dates=True)
    oil = pd.read_excel(RAW_FILE, sheet_name="Oil_Benchmarks", index_col=0, parse_dates=True)
    fred = pd.read_excel(RAW_FILE, sheet_name="FRED_Macro", index_col=0, parse_dates=True)
    return us, th, oil, fred


def assign_crisis_era(dates):
    """Map each date to a crisis era label."""
    eras = pd.Series("Other", index=dates)
    for start, end, label in CRISIS_MAP:
        mask = (dates >= pd.Timestamp(start)) & (dates <= pd.Timestamp(end))
        eras[mask] = label
    return eras


def add_indexed_price(df, base_year=BASE_YEAR):
    """Add Indexed Price column (base 100 at first observation in base_year)."""
    result = []
    for ticker in df["Ticker"].unique():
        mask = df["Ticker"] == ticker
        sub = df[mask].copy()
        base_mask = sub.index.year == base_year
        if base_mask.any():
            base_price = sub.loc[base_mask, "Close"].iloc[0]
        else:
            base_price = sub["Close"].iloc[0]
        sub["Indexed_Price"] = (sub["Close"] / base_price) * 100
        result.append(sub)
    return pd.concat(result)


def add_weekly_return(df):
    """Calculate weekly return per ticker."""
    result = []
    for ticker in df["Ticker"].unique():
        sub = df[df["Ticker"] == ticker].copy()
        sub["Weekly_Return"] = sub["Close"].pct_change()
        result.append(sub)
    return pd.concat(result)


def add_rolling_volatility(df, window=ROLLING_WINDOW):
    """Calculate rolling volatility (std of weekly returns)."""
    result = []
    for ticker in df["Ticker"].unique():
        sub = df[df["Ticker"] == ticker].copy()
        sub[f"Rolling_Vol_{window}w"] = sub["Weekly_Return"].rolling(window).std()
        result.append(sub)
    return pd.concat(result)


def currency_adjust_thai(th_df, dollar_index):
    """
    Approximate USD conversion for Thai stocks using the Dollar Index as proxy.
    THB/USD ≈ normalized Dollar Index scaling. This allows cross-country comparison.
    """
    # Normalize dollar index to a THB/USD-like range (roughly 30-40 baht per dollar)
    di = dollar_index.reindex(th_df.index, method="ffill")
    di_norm = di / di.median() * 35  # Center around ~35 THB/USD

    th_df = th_df.copy()
    th_df["Close_THB"] = th_df["Close"]
    th_df["THB_USD_Proxy"] = di_norm.values
    th_df["Close_USD"] = th_df["Close"] / th_df["THB_USD_Proxy"]
    return th_df


def compute_upstream_downstream_spread(df):
    """
    Compute Upstream/Downstream price spread.
    Upstream = PTTEP.BK, COP  |  Downstream = PTG.BK, SHEL
    """
    spreads = []
    # Thai: PTTEP / PTG
    pttep = df[df["Ticker"] == "PTTEP.BK"][["Close"]].rename(columns={"Close": "PTTEP"})
    ptg = df[df["Ticker"] == "PTG.BK"][["Close"]].rename(columns={"Close": "PTG"})
    merged = pttep.join(ptg, how="inner")
    merged["Upstream_Downstream_TH"] = merged["PTTEP"] / merged["PTG"]

    # US: COP / SHEL
    cop = df[df["Ticker"] == "COP"][["Close"]].rename(columns={"Close": "COP"})
    shel = df[df["Ticker"] == "SHEL"][["Close"]].rename(columns={"Close": "SHEL"})
    merged_us = cop.join(shel, how="inner")
    merged_us["Upstream_Downstream_US"] = merged_us["COP"] / merged_us["SHEL"]

    spread_df = merged[["Upstream_Downstream_TH"]].join(
        merged_us[["Upstream_Downstream_US"]], how="outer"
    )
    return spread_df


# ── Quality Report ───────────────────────────────────────────────────────────

def print_quality_report(df, label):
    """Print data quality summary."""
    print(f"\n  ── {label} Quality Report ──")
    print(f"     Shape        : {df.shape}")
    print(f"     Date Range   : {df.index.min().date()} to {df.index.max().date()}")
    if "Ticker" in df.columns:
        print(f"     Tickers      : {df['Ticker'].nunique()}")
    null_pct = df.isnull().mean() * 100
    high_null = null_pct[null_pct > 5]
    if len(high_null) > 0:
        print(f"     High Null (>5%): {dict(high_null.round(1))}")
    else:
        print(f"     Max Null %   : {null_pct.max():.1f}%")


# ── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    os.makedirs(CLEANED_DIR, exist_ok=True)

    print("=" * 70)
    print("PHASE 2: DATA CLEANING & FEATURE ENGINEERING")
    print("=" * 70)

    # ── Load ─────────────────────────────────────────────────────────────
    us, th, oil, fred = load_raw_data()

    # ── Combine Stocks + Oil into one master DataFrame ───────────────────
    stocks = pd.concat([us, th, oil], axis=0).sort_index()

    # ── Step 1: Crisis Era Labeling ──────────────────────────────────────
    print("\n[Step 1] Assigning crisis_era labels...")
    stocks["crisis_era"] = assign_crisis_era(stocks.index)
    era_counts = stocks.groupby("crisis_era")["Ticker"].count()
    for era, cnt in era_counts.items():
        print(f"     {era:30s} : {cnt:>6,} rows")

    # ── Step 2: Indexed Price ────────────────────────────────────────────
    print("\n[Step 2] Computing Indexed Prices (base 100 @ year 2000)...")
    stocks = add_indexed_price(stocks)

    # ── Step 3: Weekly Returns ───────────────────────────────────────────
    print("[Step 3] Computing weekly returns...")
    stocks = add_weekly_return(stocks)

    # ── Step 4: Rolling Volatility ───────────────────────────────────────
    print(f"[Step 4] Computing {ROLLING_WINDOW}-week rolling volatility...")
    stocks = add_rolling_volatility(stocks)

    # ── Step 5: Currency Adjustment for Thai stocks ──────────────────────
    print("[Step 5] Currency-adjusting Thai stocks (THB -> USD proxy)...")
    th_mask = stocks["Ticker"].str.endswith(".BK")
    dollar_index = fred["DTWEXBGS"].dropna()
    th_adjusted = currency_adjust_thai(stocks[th_mask], dollar_index)
    stocks.loc[th_mask, "Close_THB"] = th_adjusted["Close_THB"].values
    stocks.loc[th_mask, "THB_USD_Proxy"] = th_adjusted["THB_USD_Proxy"].values
    stocks.loc[th_mask, "Close_USD"] = th_adjusted["Close_USD"].values

    # For non-Thai stocks, Close_USD = Close
    stocks.loc[~th_mask, "Close_USD"] = stocks.loc[~th_mask, "Close"]

    # ── Step 6: Upstream/Downstream Spread ───────────────────────────────
    print("[Step 6] Computing Upstream/Downstream spread...")
    spread_df = compute_upstream_downstream_spread(stocks)

    # ── Step 7: Clean FRED data ──────────────────────────────────────────
    print("[Step 7] Cleaning FRED macro data (forward-fill gaps)...")
    fred_clean = fred.ffill().bfill()
    fred_clean["crisis_era"] = assign_crisis_era(fred_clean.index)

    # ── Quality Reports ──────────────────────────────────────────────────
    print_quality_report(stocks, "Stocks + Oil (Master)")
    print_quality_report(fred_clean, "FRED Macro")

    # ── Save Cleaned Data ────────────────────────────────────────────────
    print(f"\nSaving cleaned data to {CLEANED_FILE}...")
    with pd.ExcelWriter(CLEANED_FILE, engine="xlsxwriter") as writer:
        stocks.to_excel(writer, sheet_name="Stocks_Master")
        fred_clean.to_excel(writer, sheet_name="FRED_Macro")
        spread_df.to_excel(writer, sheet_name="Upstream_Downstream")

    print("\n" + "=" * 70)
    print("PHASE 2 SUMMARY")
    print("=" * 70)
    print(f"  Stocks Master : {stocks.shape}")
    print(f"  FRED Macro    : {fred_clean.shape}")
    print(f"  Spreads       : {spread_df.shape}")
    print(f"  Columns added : crisis_era, Indexed_Price, Weekly_Return,")
    print(f"                  Rolling_Vol_{ROLLING_WINDOW}w, Close_USD, THB_USD_Proxy")
    print(f"  Output        : {CLEANED_FILE}")
    print("  Phase 2 COMPLETE.\n")


if __name__ == "__main__":
    main()
