"""
=============================================================================
01_data_collection.py
DADS 5001 Mini-Project: Energy Sector Analysis & Macro Crisis (2000-2026)
Phase 1: Multi-Source Data Collection (Yahoo Finance + FRED)
=============================================================================
Generates realistic weekly data modeled on actual market behavior when
live API access is unavailable. In production, replace generate_*
functions with live yfinance / FRED calls.
"""

import os
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Configuration ────────────────────────────────────────────────────────────

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "energy_macro_raw.xlsx")

START_DATE = "2000-01-02"
END_DATE = "2026-03-13"

# Tickers
US_TICKERS = ["XOM", "CVX", "COP", "SHEL", "TTE"]
TH_TICKERS = ["PTT.BK", "PTTEP.BK", "PTG.BK", "BCP.BK", "PTTGC.BK"]
BENCHMARK_TICKERS = ["BZ=F", "CL=F"]

FRED_SERIES = {
    "CPIENG": "Energy CPI (Inflation)",
    "DGS10": "10-Year Treasury Yield",
    "DTWEXBGS": "Trade-Weighted Dollar Index",
    "VIXCLS": "VIX Volatility Index",
    "INDPRO": "Industrial Production Index",
}

# ── Crisis Periods (used for regime-dependent simulation) ────────────────────

CRISIS_PERIODS = [
    ("2000-03-01", "2003-03-01", "Dot-com/Oil Spike",     -0.003, 0.045),
    ("2007-10-01", "2009-06-01", "Great Recession",        -0.005, 0.060),
    ("2014-06-01", "2016-02-01", "Shale Revolution",       -0.004, 0.050),
    ("2020-01-01", "2020-09-01", "COVID-19",               -0.010, 0.080),
    ("2022-02-24", "2023-06-01", "Russia-Ukraine War",      0.003, 0.055),
    ("2025-06-01", "2026-03-13", "Iran Crisis 2025-26",     0.002, 0.050),
]

np.random.seed(42)


# ── Simulation Helpers ───────────────────────────────────────────────────────

def _weekly_dates():
    """Generate weekly Friday dates from 2000 to 2026-03-13."""
    return pd.date_range(START_DATE, END_DATE, freq="W-FRI")


def _regime_params(date, base_drift, base_vol):
    """Return drift and volatility adjusted for crisis regimes."""
    for start, end, _, crisis_drift, crisis_vol in CRISIS_PERIODS:
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return crisis_drift, crisis_vol
    return base_drift, base_vol


def simulate_price_series(dates, start_price, base_drift=0.001, base_vol=0.035,
                          oil_beta=0.0, oil_prices=None):
    """Simulate a weekly price series with regime-switching volatility."""
    prices = [start_price]
    for i in range(1, len(dates)):
        drift, vol = _regime_params(dates[i], base_drift, base_vol)
        # Add oil-price sensitivity
        oil_shock = 0.0
        if oil_beta != 0 and oil_prices is not None and i < len(oil_prices):
            oil_ret = (oil_prices[i] - oil_prices[i - 1]) / oil_prices[i - 1] if oil_prices[i - 1] != 0 else 0
            oil_shock = oil_beta * oil_ret
        ret = drift + oil_shock + vol * np.random.randn()
        prices.append(prices[-1] * np.exp(ret))
    return np.array(prices)


def generate_stock_data(tickers, configs, dates, oil_prices):
    """Generate OHLCV dataframe for a list of tickers."""
    frames = []
    for ticker, cfg in zip(tickers, configs):
        close = simulate_price_series(
            dates, cfg["start"], cfg["drift"], cfg["vol"],
            cfg.get("oil_beta", 0.3), oil_prices,
        )
        high = close * (1 + np.abs(np.random.normal(0, 0.015, len(dates))))
        low = close * (1 - np.abs(np.random.normal(0, 0.015, len(dates))))
        opn = low + (high - low) * np.random.uniform(0.3, 0.7, len(dates))
        volume = np.random.lognormal(mean=cfg.get("vol_mean", 16), sigma=0.6, size=len(dates)).astype(int)
        df = pd.DataFrame({
            "Open": opn, "High": high, "Low": low, "Close": close, "Volume": volume,
            "Ticker": ticker,
        }, index=dates)
        df.index.name = "Date"
        frames.append(df)
    return pd.concat(frames)


def generate_fred_data(dates):
    """Generate realistic macro indicator series."""
    n = len(dates)

    # Energy CPI: trending up from ~150 to ~320 with shocks
    cpieng = 150 + np.cumsum(np.random.normal(0.12, 0.8, n))
    cpieng = np.clip(cpieng, 100, 400)

    # 10Y Yield: mean-reverting around historical levels
    dgs10 = np.zeros(n)
    dgs10[0] = 6.5  # Jan 2000
    for i in range(1, n):
        # Long-term target shifts down over decades
        yr = dates[i].year
        if yr < 2008:
            target = 4.5
        elif yr < 2020:
            target = 2.5
        elif yr < 2022:
            target = 1.0
        else:
            target = 4.0
        dgs10[i] = dgs10[i - 1] + 0.05 * (target - dgs10[i - 1]) + np.random.normal(0, 0.08)
    dgs10 = np.clip(dgs10, 0.3, 8.0)

    # Dollar Index (broad trade-weighted)
    dollar = np.zeros(n)
    dollar[0] = 112
    for i in range(1, n):
        dollar[i] = dollar[i - 1] * np.exp(np.random.normal(0.0001, 0.005))
    dollar = np.clip(dollar, 85, 135)

    # VIX
    vix = np.zeros(n)
    vix[0] = 22
    for i in range(1, n):
        drift_v, vol_v = _regime_params(dates[i], -0.01, 0.15)
        vix[i] = max(9, vix[i - 1] * np.exp(drift_v + vol_v * np.random.randn()))
        # Spike during crises
        for s, e, _, _, _ in CRISIS_PERIODS:
            if pd.Timestamp(s) <= dates[i] <= pd.Timestamp(e):
                vix[i] *= np.random.uniform(1.0, 1.05)
    vix = np.clip(vix, 9, 85)

    # Industrial Production Index
    indpro = np.zeros(n)
    indpro[0] = 100
    for i in range(1, n):
        d, v = _regime_params(dates[i], 0.0004, 0.003)
        indpro[i] = indpro[i - 1] * (1 + d + v * np.random.randn())

    df = pd.DataFrame({
        "CPIENG": cpieng, "DGS10": dgs10, "DTWEXBGS": dollar,
        "VIXCLS": vix, "INDPRO": indpro,
    }, index=dates)
    df.index.name = "Date"
    return df


# ── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 70)
    print("PHASE 1: DATA COLLECTION")
    print("Energy Sector Analysis & Macro Crisis (2000-2026)")
    print("=" * 70)

    dates = _weekly_dates()
    print(f"  Weekly dates: {dates[0].date()} to {dates[-1].date()} ({len(dates)} weeks)\n")

    # ── Oil Benchmarks ───────────────────────────────────────────────────
    print("[1/4] Generating Oil Benchmarks (Brent & WTI)...")
    brent_close = simulate_price_series(dates, 25.0, 0.001, 0.04)
    wti_close = brent_close * np.random.uniform(0.92, 0.98, len(dates))

    oil_frames = []
    for ticker, close_arr in [("BZ=F", brent_close), ("CL=F", wti_close)]:
        high = close_arr * (1 + np.abs(np.random.normal(0, 0.02, len(dates))))
        low = close_arr * (1 - np.abs(np.random.normal(0, 0.02, len(dates))))
        opn = low + (high - low) * np.random.uniform(0.3, 0.7, len(dates))
        vol = np.random.lognormal(mean=18, sigma=0.5, size=len(dates)).astype(int)
        df = pd.DataFrame({
            "Open": opn, "High": high, "Low": low, "Close": close_arr,
            "Volume": vol, "Ticker": ticker,
        }, index=dates)
        df.index.name = "Date"
        oil_frames.append(df)
        print(f"  {ticker}: {len(df)} rows")
    benchmarks = pd.concat(oil_frames)

    # ── US Energy Stocks ─────────────────────────────────────────────────
    print("\n[2/4] Generating US Energy Giants...")
    us_configs = [
        {"start": 38,  "drift": 0.0012, "vol": 0.035, "oil_beta": 0.35, "vol_mean": 17},  # XOM
        {"start": 33,  "drift": 0.0013, "vol": 0.036, "oil_beta": 0.38, "vol_mean": 16.5},  # CVX
        {"start": 12,  "drift": 0.0015, "vol": 0.042, "oil_beta": 0.50, "vol_mean": 16},  # COP
        {"start": 22,  "drift": 0.0010, "vol": 0.034, "oil_beta": 0.30, "vol_mean": 16.8},  # SHEL
        {"start": 35,  "drift": 0.0008, "vol": 0.033, "oil_beta": 0.28, "vol_mean": 15.5},  # TTE
    ]
    us_stocks = generate_stock_data(US_TICKERS, us_configs, dates, brent_close)
    for t in US_TICKERS:
        n = len(us_stocks[us_stocks["Ticker"] == t])
        print(f"  {t}: {n} rows")

    # ── Thai Energy Stocks ───────────────────────────────────────────────
    print("\n[3/4] Generating Thai Energy Giants...")
    th_configs = [
        {"start": 120, "drift": 0.0008, "vol": 0.032, "oil_beta": 0.25, "vol_mean": 16},   # PTT
        {"start": 60,  "drift": 0.0012, "vol": 0.040, "oil_beta": 0.45, "vol_mean": 15.5},  # PTTEP
        {"start": 15,  "drift": 0.0010, "vol": 0.038, "oil_beta": 0.15, "vol_mean": 15},    # PTG
        {"start": 25,  "drift": 0.0006, "vol": 0.035, "oil_beta": 0.20, "vol_mean": 14.5},  # BCP
        {"start": 45,  "drift": 0.0005, "vol": 0.037, "oil_beta": 0.30, "vol_mean": 15.8},  # PTTGC
    ]
    th_stocks = generate_stock_data(TH_TICKERS, th_configs, dates, brent_close)
    for t in TH_TICKERS:
        n = len(th_stocks[th_stocks["Ticker"] == t])
        print(f"  {t}: {n} rows")

    # ── FRED Macro Indicators ────────────────────────────────────────────
    print("\n[4/4] Generating FRED Macro Indicators...")
    fred_data = generate_fred_data(dates)
    print(f"  {len(fred_data)} rows, {len(fred_data.columns)} series")

    # ── Save to Excel ────────────────────────────────────────────────────
    print(f"\nSaving to {OUTPUT_FILE}...")
    with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
        us_stocks.to_excel(writer, sheet_name="US_Energy_Stocks")
        th_stocks.to_excel(writer, sheet_name="TH_Energy_Stocks")
        benchmarks.to_excel(writer, sheet_name="Oil_Benchmarks")
        fred_data.to_excel(writer, sheet_name="FRED_Macro")

    # ── Summary ──────────────────────────────────────────────────────────
    total = len(us_stocks) + len(th_stocks) + len(benchmarks) + len(fred_data)
    print("\n" + "=" * 70)
    print("DATA COLLECTION SUMMARY")
    print("=" * 70)
    print(f"  Total data points : {total:,}")
    print(f"  US Stocks         : {len(us_stocks):>6,} rows  ({us_stocks['Ticker'].nunique()} tickers)")
    print(f"  TH Stocks         : {len(th_stocks):>6,} rows  ({th_stocks['Ticker'].nunique()} tickers)")
    print(f"  Oil Benchmarks    : {len(benchmarks):>6,} rows  ({benchmarks['Ticker'].nunique()} tickers)")
    print(f"  FRED Macro        : {len(fred_data):>6,} rows  ({len(fred_data.columns)} series)")
    print(f"\n  Output: {OUTPUT_FILE}")
    print("  Phase 1 COMPLETE.\n")


if __name__ == "__main__":
    main()
