"""
=============================================================================
01_data_collection.py
DADS 5001 Mini-Project: Energy Sector Analysis & Macro Crisis (2000-2026)
Phase 1: Multi-Source Data Collection (Yahoo Finance + FRED)
=============================================================================
Uses REAL data from Yahoo Finance (yfinance) and FRED API.
Run this script on a machine with unrestricted internet access.
"""

import os
import time
import warnings
import json
import pandas as pd
import yfinance as yf
from urllib.request import urlopen, Request
from urllib.error import URLError

warnings.filterwarnings("ignore")

# ── Configuration ────────────────────────────────────────────────────────────

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "energy_macro_raw.xlsx")

START_DATE = "2000-01-01"
END_DATE = "2026-03-15"

FRED_API_KEY = "e3376b3f1ddabcb9fd5d56eb51da4224"

# US Energy Giants
US_TICKERS = ["XOM", "CVX", "COP", "SHEL", "TTE"]

# Thai Energy Giants
TH_TICKERS = ["PTT.BK", "PTTEP.BK", "PTG.BK", "BCP.BK", "PTTGC.BK"]

# Energy Benchmarks
BENCHMARK_TICKERS = ["BZ=F", "CL=F"]

# FRED Macro Indicators
FRED_SERIES = {
    "CPIENG": "Energy CPI (Inflation)",
    "DGS10": "10-Year Treasury Yield",
    "DTWEXBGS": "Trade-Weighted Dollar Index",
    "VIXCLS": "VIX Volatility Index",
    "INDPRO": "Industrial Production Index",
}


# ── Yahoo Finance: Fetch Weekly Stock Data ───────────────────────────────────

def fetch_yfinance_data(tickers, label, start=START_DATE, end=END_DATE,
                        max_retries=3):
    """
    Fetch weekly OHLCV data from Yahoo Finance with retry logic.
    Handles Thai stocks that may have different start dates.
    """
    all_data = {}
    failed = []

    for ticker in tickers:
        print(f"  [{label}] Downloading {ticker}...", end=" ")
        success = False

        for attempt in range(1, max_retries + 1):
            try:
                obj = yf.Ticker(ticker)
                df = obj.history(start=start, end=end, interval="1wk",
                                 auto_adjust=True)

                if df.empty:
                    # Thai stocks may not have data from 2000; try shorter range
                    if ".BK" in ticker:
                        for fallback_year in [2003, 2005, 2010]:
                            df = obj.history(
                                start=f"{fallback_year}-01-01", end=end,
                                interval="1wk", auto_adjust=True,
                            )
                            if not df.empty:
                                print(f"(data from {fallback_year}) ", end="")
                                break

                if df.empty:
                    print(f"WARNING: No data returned (attempt {attempt}).")
                    if attempt < max_retries:
                        time.sleep(2 ** attempt)
                    continue

                # Keep key OHLCV columns
                cols = [c for c in ["Open", "High", "Low", "Close", "Volume"]
                        if c in df.columns]
                df = df[cols].copy()

                # Normalize timezone
                if df.index.tz is not None:
                    df.index = df.index.tz_localize(None)

                df["Ticker"] = ticker
                df.index.name = "Date"

                all_data[ticker] = df
                print(f"OK ({len(df)} rows, "
                      f"{df.index.min().date()} to {df.index.max().date()})")
                success = True
                break

            except Exception as e:
                print(f"ERROR (attempt {attempt}): {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)

        if not success:
            failed.append(ticker)

        time.sleep(0.5)  # Polite delay between tickers

    if failed:
        print(f"  [!] Failed tickers: {failed}")

    if not all_data:
        return pd.DataFrame()

    combined = pd.concat(all_data.values(), axis=0)
    return combined


# ── FRED API: Fetch Macro Indicators ─────────────────────────────────────────

def fetch_fred_series(series_id, api_key=FRED_API_KEY,
                      start=START_DATE, end=END_DATE, max_retries=3):
    """
    Fetch a single FRED series via the official JSON API.
    Returns a DataFrame with Date index and one column.
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    all_obs = []
    offset = 0
    limit = 10000  # FRED max per request

    while True:
        params = (
            f"?series_id={series_id}"
            f"&api_key={api_key}"
            f"&file_type=json"
            f"&observation_start={start}"
            f"&observation_end={end}"
            f"&limit={limit}"
            f"&offset={offset}"
        )
        url = base_url + params

        for attempt in range(1, max_retries + 1):
            try:
                req = Request(url, headers={"User-Agent": "DADS5001-Project/1.0"})
                with urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode())

                observations = data.get("observations", [])
                all_obs.extend(observations)

                # Check if there are more pages
                if len(observations) < limit:
                    break  # No more data
                offset += limit
                break

            except URLError as e:
                print(f"    Retry {attempt}: {e}")
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                else:
                    return pd.DataFrame()
            except Exception as e:
                print(f"    Error: {e}")
                return pd.DataFrame()

        if len(observations) < limit:
            break

    if not all_obs:
        return pd.DataFrame()

    # Parse observations
    records = []
    for obs in all_obs:
        date = obs["date"]
        value = obs["value"]
        if value == ".":  # FRED missing value marker
            value = None
        else:
            try:
                value = float(value)
            except (ValueError, TypeError):
                value = None
        records.append({"Date": pd.Timestamp(date), series_id: value})

    df = pd.DataFrame(records).set_index("Date")

    # Resample to weekly (Friday) to align with stock data
    df = df.resample("W-FRI").last()

    return df


def fetch_all_fred(series_dict):
    """Fetch all FRED series and combine into one DataFrame."""
    frames = []

    for code, name in series_dict.items():
        print(f"  [FRED] Downloading {code} ({name})...", end=" ")
        df = fetch_fred_series(code)
        if df.empty:
            print("FAILED")
        else:
            print(f"OK ({len(df)} rows)")
            frames.append(df)
        time.sleep(0.3)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, axis=1)
    combined.index.name = "Date"
    return combined


# ── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 70)
    print("PHASE 1: DATA COLLECTION (Real API)")
    print("Energy Sector Analysis & Macro Crisis (2000-2026)")
    print("=" * 70)
    print(f"  Period   : {START_DATE} to {END_DATE}")
    print(f"  Interval : Weekly (1wk)")
    print(f"  FRED Key : {FRED_API_KEY[:8]}...{FRED_API_KEY[-4:]}")

    # ── 1) US Energy Stocks ──────────────────────────────────────────────
    print("\n[1/4] Fetching US Energy Giants (Yahoo Finance)...")
    us_stocks = fetch_yfinance_data(US_TICKERS, "US")

    # ── 2) Thai Energy Stocks ────────────────────────────────────────────
    print("\n[2/4] Fetching Thai Energy Giants (Yahoo Finance)...")
    th_stocks = fetch_yfinance_data(TH_TICKERS, "TH")

    # ── 3) Oil Benchmarks ────────────────────────────────────────────────
    print("\n[3/4] Fetching Energy Benchmarks — Brent & WTI (Yahoo Finance)...")
    benchmarks = fetch_yfinance_data(BENCHMARK_TICKERS, "OIL")

    # ── 4) FRED Macro Indicators ─────────────────────────────────────────
    print("\n[4/4] Fetching FRED Macro Indicators (FRED API)...")
    fred_data = fetch_all_fred(FRED_SERIES)

    # ── Validate: at least some data collected ───────────────────────────
    datasets = {
        "US_Energy_Stocks": us_stocks,
        "TH_Energy_Stocks": th_stocks,
        "Oil_Benchmarks": benchmarks,
        "FRED_Macro": fred_data,
    }

    non_empty = {k: v for k, v in datasets.items() if not v.empty}
    if not non_empty:
        print("\n  [ERROR] No data collected from any source!")
        print("  Please check your internet connection and API access.")
        print("  Yahoo Finance: https://finance.yahoo.com")
        print("  FRED API: https://fred.stlouisfed.org/docs/api/api_key.html")
        return

    # ── Save to Excel (multiple sheets) ──────────────────────────────────
    print(f"\nSaving to {OUTPUT_FILE}...")
    with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
        for sheet_name, df in datasets.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name)
                print(f"  Sheet '{sheet_name}': {len(df):,} rows")

    # ── Summary ──────────────────────────────────────────────────────────
    total = sum(len(v) for v in datasets.values() if not v.empty)

    print("\n" + "=" * 70)
    print("DATA COLLECTION SUMMARY")
    print("=" * 70)
    print(f"  Total data points : {total:,}")

    for name, df in datasets.items():
        if not df.empty:
            n_tickers = df["Ticker"].nunique() if "Ticker" in df.columns else len(df.columns)
            label = "tickers" if "Ticker" in df.columns else "series"
            print(f"  {name:20s}: {len(df):>6,} rows  ({n_tickers} {label})")
        else:
            print(f"  {name:20s}: EMPTY (API unreachable)")

    print(f"\n  Output: {OUTPUT_FILE}")
    print("  Phase 1 COMPLETE.\n")


if __name__ == "__main__":
    main()
