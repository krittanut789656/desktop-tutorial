"""
01_data_collection.py — Data Collection from MOC Open Data API
DADS 5001 Mini-Project: Thailand Trade Impact Analysis
Data Source: dataapi.moc.go.th (Ministry of Commerce, Thailand)
"""

import requests
import pandas as pd
import time
import os
import json
import logging
from datetime import datetime

# ============================================================
# Configuration
# ============================================================

BASE_URLS = {
    'summary': 'https://dataapi.moc.go.th/summary-countries',
    'import': 'https://dataapi.moc.go.th/import-harmonize-countries',
    'export': 'https://dataapi.moc.go.th/export-harmonize-countries',
}

RAW_DIR = 'data/raw'
os.makedirs(RAW_DIR, exist_ok=True)

# Setup error logging
logging.basicConfig(
    filename=os.path.join(RAW_DIR, 'api_errors.log'),
    level=logging.ERROR,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# Year range
YEARS = range(2019, 2027)  # 2019-2026
MONTHS = range(1, 13)


def fetch_api(url, params, max_retries=3):
    """Fetch data from MOC API with retry logic and error handling."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'data' in data:
                    return data['data']
                else:
                    return [data] if data else []
            else:
                logging.error(f"HTTP {response.status_code} | URL: {url} | Params: {params}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error | URL: {url} | Params: {params} | Error: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return []


def collect_trade_overview():
    """Dataset 1: Trade Overview by country (summary-countries)."""
    print("\n" + "="*60)
    print("Dataset 1: Trade Overview (summary-countries)")
    print("="*60)

    all_data = []
    total_calls = 0

    for year in YEARS:
        for month in MONTHS:
            # Skip future months
            if year == 2026 and month > 3:
                continue

            params = {'year': year, 'month': month, 'limit': 500}
            data = fetch_api(BASE_URLS['summary'], params)

            if data:
                for row in data:
                    row['year'] = year
                    row['month'] = month
                    row['data_type'] = 'overview'
                all_data.extend(data)

            total_calls += 1
            print(f"  [{total_calls}] {year}-{month:02d}: {len(data)} records")
            time.sleep(0.5)

    df = pd.DataFrame(all_data)
    csv_path = os.path.join(RAW_DIR, 'trade_overview.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n  Total records: {len(df):,}")
    print(f"  Saved: {csv_path}")
    return df


def collect_harmonize_data(api_type, hs_codes, dataset_name, description):
    """Generic function to collect import/export data by HS code."""
    print("\n" + "="*60)
    print(f"Dataset: {description}")
    print(f"  HS Codes: {hs_codes}")
    print("="*60)

    url = BASE_URLS[api_type]
    all_data = []
    total_calls = 0

    for hs_code in hs_codes:
        for year in YEARS:
            for month in MONTHS:
                if year == 2026 and month > 3:
                    continue

                params = {
                    'year': year,
                    'month': month,
                    'hs_code': hs_code,
                    'limit': 500
                }
                data = fetch_api(url, params)

                if data:
                    for row in data:
                        row['year'] = year
                        row['month'] = month
                        row['hs_code'] = hs_code
                        row['hs_description'] = get_hs_description(hs_code)
                        row['data_type'] = api_type
                    all_data.extend(data)

                total_calls += 1
                print(f"  [{total_calls}] HS {hs_code} | {year}-{month:02d}: {len(data)} records")
                time.sleep(0.5)

    df = pd.DataFrame(all_data)
    csv_path = os.path.join(RAW_DIR, f'{dataset_name}.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n  Total records: {len(df):,}")
    print(f"  Saved: {csv_path}")
    return df


def get_hs_description(hs_code):
    """Return description for HS code."""
    descriptions = {
        '27': 'Mineral Fuels (Oil, Gas, Coal)',
        '29': 'Organic Chemicals (Naphtha)',
        '31': 'Fertilizers',
        '10': 'Cereals (Rice)',
        '16': 'Prepared Meat/Fish (Canned Food)',
        '17': 'Sugars',
        '40': 'Rubber & Articles',
        '85': 'Electrical Machinery & Electronics',
        '87': 'Vehicles & Parts',
        '39': 'Plastics & Articles',
    }
    return descriptions.get(hs_code, f'HS {hs_code}')


def create_metadata(datasets):
    """Create metadata sheet for the Excel file."""
    metadata = []
    for name, df in datasets.items():
        metadata.append({
            'dataset': name,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': ', '.join(df.columns.tolist()),
            'date_collected': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'api_source': 'dataapi.moc.go.th',
        })
    return pd.DataFrame(metadata)


def main():
    """Main execution: collect all 6 datasets."""
    print("="*60)
    print("Thailand Trade Data Collection")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Source: dataapi.moc.go.th (Ministry of Commerce)")
    print("="*60)

    datasets = {}

    # Dataset 1: Trade Overview
    datasets['trade_overview'] = collect_trade_overview()

    # Dataset 2: Energy Imports (HS 27)
    datasets['energy_imports'] = collect_harmonize_data(
        'import', ['27'], 'energy_imports',
        'Energy Imports (HS 27 - Mineral Fuels)'
    )

    # Dataset 3: Fertilizer Imports (HS 31)
    datasets['fertilizer_imports'] = collect_harmonize_data(
        'import', ['31'], 'fertilizer_imports',
        'Fertilizer Imports (HS 31 - Fertilizers)'
    )

    # Dataset 4: Agri-Food Exports (HS 10, 16, 40, 17)
    datasets['agrifood_exports'] = collect_harmonize_data(
        'export', ['10', '16', '40', '17'], 'agrifood_exports',
        'Agri-Food Exports (HS 10, 16, 40, 17)'
    )

    # Dataset 5: Industrial Exports (HS 85, 87, 39)
    datasets['industrial_exports'] = collect_harmonize_data(
        'export', ['85', '87', '39'], 'industrial_exports',
        'Industrial Exports (HS 85, 87, 39)'
    )

    # Dataset 6: Petrochemical Imports (HS 29)
    datasets['petrochemical_imports'] = collect_harmonize_data(
        'import', ['29'], 'petrochemical_imports',
        'Petrochemical Imports (HS 29 - Organic Chemicals)'
    )

    # Create Excel with all sheets
    print("\n" + "="*60)
    print("Creating combined Excel file...")
    print("="*60)

    excel_path = os.path.join(RAW_DIR, 'thailand_trade_raw_data.xlsx')
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for sheet_name, df in datasets.items():
            if len(df) > 0:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Metadata sheet
        metadata_df = create_metadata(datasets)
        metadata_df.to_excel(writer, sheet_name='metadata', index=False)

    print(f"  Saved: {excel_path}")

    # Summary
    print("\n" + "="*60)
    print("COLLECTION SUMMARY")
    print("="*60)
    total_rows = 0
    for name, df in datasets.items():
        print(f"  {name}: {len(df):,} rows")
        total_rows += len(df)
    print(f"\n  TOTAL: {total_rows:,} rows")
    print(f"  End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return datasets


if __name__ == '__main__':
    main()
