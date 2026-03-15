"""
02_data_cleaning.py — Data Cleaning & Feature Engineering
DADS 5001 Mini-Project: Thailand Trade Impact Analysis
DADS, NIDA

Reads raw CSV data from data/raw/, performs cleaning and feature engineering,
and saves clean data to data/clean/.
"""

import sys
import os
import warnings
from datetime import datetime

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Import shared classification functions from utils.py
# ---------------------------------------------------------------------------
sys.path.insert(0, 'src')
from utils import classify_region, classify_shipping_route, classify_crisis_period, REGION_MAP

warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
RAW_DIR = 'data/raw'
CLEAN_DIR = 'data/clean'
os.makedirs(CLEAN_DIR, exist_ok=True)

# Dataset registry: filename -> (dataset_label, dataset_type)
DATASETS = {
    'trade_overview.csv':        ('trade_overview',        'overview'),
    'energy_imports.csv':        ('energy_imports',         'harmonized'),
    'fertilizer_imports.csv':    ('fertilizer_imports',     'harmonized'),
    'petrochemical_imports.csv': ('petrochemical_imports',  'harmonized'),
    'agrifood_exports.csv':      ('agrifood_exports',       'harmonized'),
    'industrial_exports.csv':    ('industrial_exports',     'harmonized'),
}


# ============================================================
# 1. LOAD RAW DATA
# ============================================================
def load_raw_data():
    """Load all raw CSV files into a dict of DataFrames."""
    print("=" * 70)
    print("STEP 1: Loading Raw Data")
    print("=" * 70)
    dataframes = {}
    for filename, (label, _) in DATASETS.items():
        filepath = os.path.join(RAW_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  [WARNING] File not found: {filepath} — skipping.")
            continue
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        print(f"  Loaded {label:30s} | {len(df):>7,} rows x {df.shape[1]} cols")
        dataframes[label] = df
    print(f"\n  Total datasets loaded: {len(dataframes)}")
    return dataframes


# ============================================================
# 2. DATA QUALITY CHECK
# ============================================================
def check_data_quality(dataframes):
    """Run data quality checks and return a quality report as a list of strings."""
    print("\n" + "=" * 70)
    print("STEP 2: Data Quality Check")
    print("=" * 70)

    report_lines = []
    report_lines.append("THAILAND TRADE DATA — DATA QUALITY REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 70)

    for name, df in dataframes.items():
        report_lines.append(f"\n{'─' * 50}")
        report_lines.append(f"Dataset: {name}  |  Shape: {df.shape}")
        report_lines.append(f"{'─' * 50}")

        # --- Missing values ---
        missing = df.isnull().sum()
        missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
        missing_df = pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct})
        missing_df = missing_df[missing_df['missing_count'] > 0]

        if missing_df.empty:
            msg = "  Missing values: None"
            print(msg)
            report_lines.append(msg)
        else:
            print(f"  Missing values in {name}:")
            report_lines.append("  Missing values:")
            for col, row in missing_df.iterrows():
                line = f"    {col:30s}  {int(row['missing_count']):>6}  ({row['missing_pct']:.2f}%)"
                print(line)
                report_lines.append(line)

        # --- Duplicates ---
        n_dup = df.duplicated().sum()
        msg = f"  Duplicates: {n_dup:,}"
        print(msg)
        report_lines.append(msg)

        # --- Data types ---
        report_lines.append("  Column dtypes:")
        for col in df.columns:
            report_lines.append(f"    {col:30s}  {str(df[col].dtype)}")

        # --- Basic stats for numeric columns ---
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            report_lines.append("  Numeric summary (min / max):")
            for col in numeric_cols:
                report_lines.append(
                    f"    {col:30s}  min={df[col].min():>15,.2f}  max={df[col].max():>15,.2f}"
                )

    report_lines.append("\n" + "=" * 70)
    report_lines.append("END OF DATA QUALITY REPORT")
    return report_lines


# ============================================================
# 3. CLEAN DATA
# ============================================================
def clean_dataframe(df, name):
    """Remove duplicates, convert types, flag outliers."""
    print(f"\n  Cleaning: {name}")
    original_len = len(df)

    # --- Remove duplicates ---
    df = df.drop_duplicates().reset_index(drop=True)
    n_removed = original_len - len(df)
    if n_removed > 0:
        print(f"    Removed {n_removed:,} duplicate rows")

    # --- Convert numeric columns ---
    # Identify value/quantity columns and coerce to numeric
    numeric_candidates = [c for c in df.columns if any(
        kw in c for kw in ['value_usd', 'value_baht', 'quantity',
                           'import_value', 'export_value', 'trade_value', 'trade_balance']
    )]
    for col in numeric_candidates:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Ensure year and month are integers
    for col in ['year', 'month']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # --- Flag outliers with IQR method (on USD value columns) ---
    usd_cols = [c for c in df.columns if 'value_usd' in c]
    df['is_outlier'] = False
    for col in usd_cols:
        if df[col].dropna().empty:
            continue
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outlier_mask = (df[col] < lower) | (df[col] > upper)
        n_outliers = outlier_mask.sum()
        df['is_outlier'] = df['is_outlier'] | outlier_mask
        print(f"    Outliers in {col}: {n_outliers:,} flagged (IQR method)")

    total_outliers = df['is_outlier'].sum()
    print(f"    Total rows flagged as outlier: {total_outliers:,} / {len(df):,}")

    return df


# ============================================================
# 4. FEATURE ENGINEERING
# ============================================================
def add_features(df, name, dataset_type):
    """Add engineered features to a DataFrame."""
    print(f"\n  Feature engineering: {name}")

    # --- date column (YYYY-MM-01) ---
    if 'year' in df.columns and 'month' in df.columns:
        df['date'] = pd.to_datetime(
            df['year'].astype(str) + '-' + df['month'].astype(str) + '-01',
            format='%Y-%m-%d',
            errors='coerce'
        )
        print(f"    Added 'date' column  |  range: {df['date'].min()} to {df['date'].max()}")

    # --- year_month string ---
    if 'date' in df.columns:
        df['year_month'] = df['date'].dt.strftime('%Y-%m')
        print("    Added 'year_month' column")

    # --- region ---
    if 'country_eng' in df.columns:
        df['region'] = df['country_eng'].apply(classify_region)
        n_others = (df['region'] == 'Others').sum()
        print(f"    Added 'region' column  |  'Others' count: {n_others:,}")

    # --- shipping_route ---
    if 'region' in df.columns:
        df['shipping_route'] = df['region'].apply(classify_shipping_route)
        print(f"    Added 'shipping_route' column  |  unique routes: {df['shipping_route'].nunique()}")

    # --- crisis_period ---
    if 'date' in df.columns:
        df['crisis_period'] = df['date'].apply(classify_crisis_period)
        print(f"    Added 'crisis_period' column  |  periods: {df['crisis_period'].nunique()}")

    # --- unit_price_usd (harmonized datasets only) ---
    if dataset_type == 'harmonized' and 'value_usd' in df.columns and 'quantity' in df.columns:
        mask = df['quantity'] > 0
        df['unit_price_usd'] = np.nan
        df.loc[mask, 'unit_price_usd'] = df.loc[mask, 'value_usd'] / df.loc[mask, 'quantity']
        valid = df['unit_price_usd'].notna().sum()
        print(f"    Added 'unit_price_usd' column  |  computed for {valid:,} rows")

    # --- YoY change % ---
    if dataset_type == 'harmonized' and 'value_usd' in df.columns:
        group_cols = ['country_eng']
        if 'hs_code' in df.columns:
            group_cols.append('hs_code')
        df = df.sort_values(group_cols + ['date']).reset_index(drop=True)

        # YoY: shift 12 months within group
        df['yoy_change_pct'] = (
            df.groupby(group_cols)['value_usd']
            .pct_change(periods=12) * 100
        )
        valid_yoy = df['yoy_change_pct'].notna().sum()
        print(f"    Added 'yoy_change_pct' column  |  computed for {valid_yoy:,} rows")

        # MoM: shift 1 month within group
        df['mom_change_pct'] = (
            df.groupby(group_cols)['value_usd']
            .pct_change(periods=1) * 100
        )
        valid_mom = df['mom_change_pct'].notna().sum()
        print(f"    Added 'mom_change_pct' column  |  computed for {valid_mom:,} rows")

    elif dataset_type == 'overview':
        # For overview data, use trade_value_usd (or import/export)
        value_col = 'trade_value_usd' if 'trade_value_usd' in df.columns else None
        if value_col and 'country_eng' in df.columns:
            group_cols = ['country_eng']
            df = df.sort_values(group_cols + ['date']).reset_index(drop=True)

            df['yoy_change_pct'] = (
                df.groupby(group_cols)[value_col]
                .pct_change(periods=12) * 100
            )
            df['mom_change_pct'] = (
                df.groupby(group_cols)[value_col]
                .pct_change(periods=1) * 100
            )
            print(f"    Added 'yoy_change_pct' and 'mom_change_pct' (based on {value_col})")

    return df


# ============================================================
# 5. SAVE CLEAN DATA
# ============================================================
def save_clean_data(dataframes, quality_report):
    """Save cleaned DataFrames to Excel (multi-sheet) and combined CSV."""
    print("\n" + "=" * 70)
    print("STEP 5: Saving Clean Data")
    print("=" * 70)

    # --- Excel with separate sheets ---
    excel_path = os.path.join(CLEAN_DIR, 'thailand_trade_clean.xlsx')
    try:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for name, df in dataframes.items():
                # Sheet names max 31 chars
                sheet_name = name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  Sheet '{sheet_name}' — {len(df):,} rows")
        print(f"  Saved Excel: {excel_path}")
    except Exception as e:
        print(f"  [ERROR] Could not save Excel: {e}")

    # --- Combined CSV with dataset column ---
    csv_path = os.path.join(CLEAN_DIR, 'thailand_trade_clean.csv')
    try:
        combined_parts = []
        for name, df in dataframes.items():
            temp = df.copy()
            temp['dataset'] = name
            combined_parts.append(temp)
        combined = pd.concat(combined_parts, ignore_index=True)
        combined.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"  Saved combined CSV: {csv_path}  |  {len(combined):,} total rows")
    except Exception as e:
        print(f"  [ERROR] Could not save CSV: {e}")

    # --- Data quality report ---
    report_path = os.path.join(CLEAN_DIR, 'data_quality_report.txt')
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(quality_report))
        print(f"  Saved quality report: {report_path}")
    except Exception as e:
        print(f"  [ERROR] Could not save quality report: {e}")


# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "#" * 70)
    print("#  THAILAND TRADE DATA — DATA CLEANING & FEATURE ENGINEERING")
    print(f"#  Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#" * 70)

    # 1. Load
    dataframes = load_raw_data()
    if not dataframes:
        print("[ERROR] No datasets loaded. Ensure CSV files exist in data/raw/.")
        sys.exit(1)

    # 2. Quality check (on raw data)
    quality_report = check_data_quality(dataframes)

    # 3 & 4. Clean + Feature engineering
    print("\n" + "=" * 70)
    print("STEPS 3-4: Cleaning & Feature Engineering")
    print("=" * 70)

    cleaned = {}
    for name, df in dataframes.items():
        # Look up dataset type
        dataset_type = None
        for filename, (label, dtype) in DATASETS.items():
            if label == name:
                dataset_type = dtype
                break
        dataset_type = dataset_type or 'harmonized'

        df_clean = clean_dataframe(df.copy(), name)
        df_clean = add_features(df_clean, name, dataset_type)
        cleaned[name] = df_clean

    # Summary
    print("\n" + "=" * 70)
    print("CLEANING SUMMARY")
    print("=" * 70)
    for name, df in cleaned.items():
        print(f"  {name:30s}  |  {len(df):>7,} rows  |  {df.shape[1]:>3} cols")
        if 'region' in df.columns:
            print(f"    Regions: {sorted(df['region'].unique())}")
        if 'crisis_period' in df.columns:
            print(f"    Crisis periods: {sorted(df['crisis_period'].unique())}")

    # 5. Save
    save_clean_data(cleaned, quality_report)

    print("\n" + "#" * 70)
    print("#  DATA CLEANING COMPLETE")
    print("#" * 70 + "\n")


if __name__ == '__main__':
    main()
