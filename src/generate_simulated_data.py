"""
generate_simulated_data.py — Generate realistic simulated trade data
for development/demonstration when the MOC API is inaccessible.

The data follows realistic patterns:
- Seasonal trade cycles
- COVID-19 impact (2020-2021)
- Russia-Ukraine war energy price shock (2022)
- 12-Day War brief disruption (June 2025)
- Iran War escalation (Feb 2026+)

NOTE: This generates SIMULATED data for pipeline demonstration.
      For the actual project, run 01_data_collection.py to fetch real API data.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

np.random.seed(42)

RAW_DIR = 'data/raw'
os.makedirs(RAW_DIR, exist_ok=True)

# ============================================================
# Country pools
# ============================================================

HORMUZ_COUNTRIES = [
    'Saudi Arabia', 'United Arab Emirates', 'Kuwait', 'Qatar',
    'Iran', 'Iraq', 'Bahrain', 'Oman'
]

NON_HORMUZ_ME = ['Israel', 'Jordan', 'Lebanon', 'Turkey', 'Egypt', 'Yemen']

ASEAN = ['Malaysia', 'Singapore', 'Indonesia', 'Vietnam', 'Philippines',
         'Myanmar', 'Cambodia', 'Brunei Darussalam']

EAST_ASIA = ['China', 'Japan', 'Korea, Republic of', 'Taiwan', 'Hong Kong']

SOUTH_ASIA = ['India', 'Bangladesh', 'Pakistan', 'Sri Lanka']

EUROPE = ['Germany', 'United Kingdom', 'France', 'Netherlands', 'Italy',
          'Spain', 'Belgium', 'Switzerland', 'Sweden', 'Poland',
          'Russian Federation']

AMERICAS = ['United States of America', 'Canada', 'Brazil', 'Mexico',
            'Argentina', 'Chile']

AFRICA = ['South Africa', 'Nigeria', 'Kenya', 'Ghana', 'Morocco',
          'Algeria', 'Libya', 'Tanzania']

OCEANIA = ['Australia', 'New Zealand']

ALL_COUNTRIES = (HORMUZ_COUNTRIES + NON_HORMUZ_ME + ASEAN + EAST_ASIA +
                 SOUTH_ASIA + EUROPE + AMERICAS + AFRICA + OCEANIA)


def get_crisis_multiplier(year, month, data_type='import', commodity='general'):
    """Return a multiplier reflecting crisis effects on trade values."""
    # Base = 1.0
    m = 1.0
    date_val = year * 100 + month

    # COVID-19 (Mar 2020 - Dec 2021): trade drops
    if 202003 <= date_val <= 202012:
        m *= 0.75 if data_type == 'export' else 0.80
    elif 202101 <= date_val <= 202112:
        m *= 0.90

    # Russia-Ukraine (Feb 2022 - Sep 2023): energy price spike
    if 202202 <= date_val <= 202309:
        if commodity in ('27', '29', '31'):  # energy/petrochem/fertilizer
            m *= 1.45  # price spike
        elif commodity in ('10', '16', '17'):  # agri-food
            m *= 1.15  # food demand up
        elif commodity == '40':  # rubber
            m *= 1.10

    # Post-RU stabilization
    if 202310 <= date_val <= 202505:
        if commodity in ('27', '29'):
            m *= 1.05

    # 12-Day War (June 2025)
    if date_val == 202506:
        if commodity in ('27', '29', '31'):
            m *= 1.20
        m *= 0.95

    # Post-12-Day recovery
    if 202507 <= date_val <= 202601:
        m *= 1.0

    # Iran War (Feb 2026+)
    if date_val >= 202602:
        if commodity in ('27', '29'):
            m *= 1.55  # major energy price shock
        elif commodity == '31':
            m *= 1.35  # fertilizer spike
        elif commodity in ('10', '16', '17'):
            m *= 1.20  # food demand surge
        elif commodity == '40':
            m *= 1.15  # rubber benefits from oil price
        elif commodity in ('85', '87'):
            m *= 0.90  # indirect supply chain disruption
        elif commodity == '39':
            m *= 0.92

    return m


def seasonal_factor(month):
    """Seasonal trade pattern: higher Q4, lower Q1."""
    factors = {1: 0.88, 2: 0.85, 3: 0.95, 4: 0.98, 5: 1.00, 6: 1.02,
               7: 1.00, 8: 1.03, 9: 1.05, 10: 1.08, 11: 1.06, 12: 0.92}
    return factors.get(month, 1.0)


def generate_trade_overview():
    """Dataset 1: Trade Overview by country."""
    print("Generating Dataset 1: Trade Overview...")
    rows = []

    # Base trade values (annual, million USD) for top partners
    country_base_import = {
        'China': 50000, 'Japan': 30000, 'United States of America': 12000,
        'Malaysia': 10000, 'Korea, Republic of': 8000, 'Singapore': 8000,
        'Saudi Arabia': 15000, 'United Arab Emirates': 12000,
        'Indonesia': 7000, 'Germany': 5000, 'India': 5500,
        'Taiwan': 7000, 'Australia': 6000, 'Vietnam': 5000,
        'Kuwait': 6000, 'Qatar': 5000, 'Russian Federation': 3000,
        'Iran': 1500, 'Iraq': 3500, 'Oman': 3000, 'Bahrain': 800,
        'Switzerland': 4000, 'Brazil': 2500, 'South Africa': 1500,
        'United Kingdom': 2500, 'France': 2000, 'Netherlands': 2000,
        'Hong Kong': 3000, 'Philippines': 3000, 'Myanmar': 2500,
    }

    country_base_export = {
        'United States of America': 32000, 'China': 30000, 'Japan': 24000,
        'Vietnam': 12000, 'Hong Kong': 10000, 'Malaysia': 8000,
        'Australia': 8000, 'Indonesia': 7500, 'India': 7000,
        'Singapore': 6500, 'Philippines': 6000, 'Korea, Republic of': 5000,
        'Germany': 4000, 'United Kingdom': 3500, 'Netherlands': 3500,
        'Myanmar': 3000, 'Cambodia': 3000, 'Saudi Arabia': 2500,
        'United Arab Emirates': 2000, 'South Africa': 1800,
        'Nigeria': 1200, 'Brazil': 1500, 'Mexico': 1500,
        'France': 2000, 'Canada': 2000, 'Taiwan': 3500,
        'Iran': 400, 'Iraq': 300, 'Israel': 600, 'Turkey': 1200,
    }

    for year in range(2019, 2027):
        for month in range(1, 13):
            if year == 2026 and month > 3:
                continue

            # Growth trend ~3% per year from 2019
            growth = 1.0 + 0.03 * (year - 2019)
            sf = seasonal_factor(month)

            for country in ALL_COUNTRIES:
                base_imp = country_base_import.get(country, 500)
                base_exp = country_base_export.get(country, 300)

                crisis_imp = get_crisis_multiplier(year, month, 'import', 'general')
                crisis_exp = get_crisis_multiplier(year, month, 'export', 'general')

                # Iran-specific: trade collapses during war
                if country == 'Iran' and year * 100 + month >= 202602:
                    crisis_imp *= 0.15
                    crisis_exp *= 0.10

                monthly_imp = (base_imp / 12) * growth * sf * crisis_imp
                monthly_exp = (base_exp / 12) * growth * sf * crisis_exp

                # Add noise
                monthly_imp *= np.random.normal(1.0, 0.08)
                monthly_exp *= np.random.normal(1.0, 0.08)
                monthly_imp = max(0, monthly_imp)
                monthly_exp = max(0, monthly_exp)

                baht_rate = 33.0 + np.random.normal(0, 1.5)

                rows.append({
                    'country_eng': country,
                    'import_value_usd': round(monthly_imp * 1e6, 2),
                    'import_value_baht': round(monthly_imp * 1e6 * baht_rate, 2),
                    'export_value_usd': round(monthly_exp * 1e6, 2),
                    'export_value_baht': round(monthly_exp * 1e6 * baht_rate, 2),
                    'trade_value_usd': round((monthly_imp + monthly_exp) * 1e6, 2),
                    'trade_balance_usd': round((monthly_exp - monthly_imp) * 1e6, 2),
                    'year': year,
                    'month': month,
                    'data_type': 'overview',
                })

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, 'trade_overview.csv'), index=False, encoding='utf-8-sig')
    print(f"  Trade Overview: {len(df):,} rows")
    return df


def generate_harmonize_data(api_type, hs_codes, dataset_name, base_values):
    """Generate import/export harmonize data for given HS codes."""
    print(f"Generating {dataset_name}...")
    rows = []

    hs_descriptions = {
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

    for hs_code in hs_codes:
        for year in range(2019, 2027):
            for month in range(1, 13):
                if year == 2026 and month > 3:
                    continue

                growth = 1.0 + 0.03 * (year - 2019)
                sf = seasonal_factor(month)
                crisis_m = get_crisis_multiplier(year, month, api_type, hs_code)

                country_pool = base_values.get(hs_code, {})
                for country, base_val in country_pool.items():
                    monthly_val = (base_val / 12) * growth * sf * crisis_m

                    # Iran trade collapse during Iran War
                    if country == 'Iran' and year * 100 + month >= 202602:
                        monthly_val *= 0.10

                    # Volume: inverse relationship during price spikes
                    base_qty = monthly_val * 0.8  # rough proxy
                    if hs_code in ('27', '29', '31') and crisis_m > 1.2:
                        # Price up but volume down
                        qty_factor = 1.0 / (crisis_m * 0.7)
                    else:
                        qty_factor = 1.0

                    monthly_val *= np.random.normal(1.0, 0.10)
                    monthly_val = max(0, monthly_val)
                    quantity = max(0, base_qty * qty_factor * np.random.normal(1.0, 0.12))

                    baht_rate = 33.0 + np.random.normal(0, 1.5)

                    rows.append({
                        'country_eng': country,
                        'value_usd': round(monthly_val * 1e6, 2),
                        'value_baht': round(monthly_val * 1e6 * baht_rate, 2),
                        'quantity': round(quantity * 1000, 2),
                        'quantity_unit': 'KGM',
                        'year': year,
                        'month': month,
                        'hs_code': hs_code,
                        'hs_description': hs_descriptions.get(hs_code, f'HS {hs_code}'),
                        'data_type': api_type,
                    })

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, f'{dataset_name}.csv'), index=False, encoding='utf-8-sig')
    print(f"  {dataset_name}: {len(df):,} rows")
    return df


def main():
    print("="*60)
    print("Generating Simulated Thailand Trade Data")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("NOTE: Simulated data for pipeline demonstration")
    print("      Run 01_data_collection.py for real API data")
    print("="*60)

    datasets = {}

    # Dataset 1: Trade Overview
    datasets['trade_overview'] = generate_trade_overview()

    # Dataset 2: Energy Imports (HS 27)
    energy_base = {
        '27': {
            'Saudi Arabia': 8000, 'United Arab Emirates': 5000,
            'Kuwait': 4000, 'Qatar': 3500, 'Oman': 2000,
            'Iran': 1200, 'Iraq': 2500, 'Bahrain': 500,
            'Russian Federation': 1500, 'Malaysia': 1200,
            'Indonesia': 800, 'Australia': 1500, 'India': 600,
            'United States of America': 400, 'Nigeria': 300,
            'Angola': 200, 'Brazil': 250,
        }
    }
    datasets['energy_imports'] = generate_harmonize_data(
        'import', ['27'], 'energy_imports', energy_base)

    # Dataset 3: Fertilizer Imports (HS 31)
    fert_base = {
        '31': {
            'Saudi Arabia': 800, 'Qatar': 400, 'Oman': 300,
            'China': 600, 'Russian Federation': 500, 'Canada': 300,
            'Japan': 200, 'Malaysia': 250, 'Indonesia': 200,
            'India': 150, 'Germany': 100, 'United States of America': 150,
            'Belarus': 100, 'Morocco': 120, 'Israel': 180,
            'Jordan': 150, 'Vietnam': 80,
        }
    }
    datasets['fertilizer_imports'] = generate_harmonize_data(
        'import', ['31'], 'fertilizer_imports', fert_base)

    # Dataset 4: Agri-Food Exports (HS 10, 16, 40, 17)
    agri_base = {
        '10': {  # Rice
            'China': 1500, 'Nigeria': 600, 'Indonesia': 500,
            'South Africa': 400, 'Iraq': 350, 'United States of America': 300,
            'Japan': 250, 'Saudi Arabia': 200, 'Philippines': 180,
            'Malaysia': 150, 'Hong Kong': 200, 'Singapore': 120,
            'Cameroon': 100, 'Mozambique': 90, 'Senegal': 80,
            'Iran': 250, 'India': 100, 'Yemen': 80,
        },
        '16': {  # Canned food
            'Japan': 1200, 'United States of America': 800,
            'United Kingdom': 400, 'Australia': 350,
            'Canada': 250, 'Germany': 200, 'Netherlands': 180,
            'Saudi Arabia': 150, 'United Arab Emirates': 120,
            'Singapore': 100, 'Malaysia': 90, 'Korea, Republic of': 150,
            'France': 100, 'Libya': 50, 'Egypt': 60,
        },
        '40': {  # Rubber
            'China': 3500, 'Japan': 1200, 'United States of America': 1000,
            'Malaysia': 800, 'Korea, Republic of': 600,
            'Germany': 500, 'India': 400, 'Brazil': 350,
            'Turkey': 300, 'Indonesia': 250, 'France': 200,
            'Spain': 150, 'Italy': 180, 'Taiwan': 200,
            'Vietnam': 150, 'United Kingdom': 130,
        },
        '17': {  # Sugar
            'Indonesia': 800, 'Cambodia': 400, 'China': 350,
            'Korea, Republic of': 250, 'Japan': 200,
            'Taiwan': 150, 'Philippines': 120, 'Singapore': 100,
            'Malaysia': 80, 'India': 60, 'Vietnam': 50,
            'Laos': 40, 'Myanmar': 30,
        },
    }
    datasets['agrifood_exports'] = generate_harmonize_data(
        'export', ['10', '16', '40', '17'], 'agrifood_exports', agri_base)

    # Dataset 5: Industrial Exports (HS 85, 87, 39)
    industrial_base = {
        '85': {  # Electronics
            'United States of America': 6000, 'China': 4000,
            'Japan': 3500, 'Hong Kong': 3000, 'Singapore': 2000,
            'Vietnam': 1500, 'Malaysia': 1200, 'Germany': 1000,
            'India': 800, 'Korea, Republic of': 900,
            'Indonesia': 700, 'Netherlands': 600,
            'Philippines': 500, 'United Kingdom': 450,
            'Australia': 400, 'Taiwan': 500, 'Mexico': 350,
        },
        '87': {  # Vehicles
            'Australia': 3000, 'Philippines': 2000,
            'Indonesia': 1800, 'Japan': 1500, 'Malaysia': 1200,
            'Vietnam': 1000, 'Saudi Arabia': 800,
            'United Arab Emirates': 600, 'New Zealand': 500,
            'Mexico': 400, 'South Africa': 350,
            'Chile': 300, 'Argentina': 250,
            'United Kingdom': 300, 'Germany': 200,
        },
        '39': {  # Plastics
            'China': 2000, 'Japan': 1200, 'Vietnam': 1000,
            'Indonesia': 800, 'India': 700, 'Malaysia': 600,
            'Australia': 500, 'Philippines': 400,
            'United States of America': 500, 'Korea, Republic of': 350,
            'Myanmar': 300, 'Cambodia': 250, 'Bangladesh': 200,
            'Hong Kong': 200, 'Singapore': 250,
        },
    }
    datasets['industrial_exports'] = generate_harmonize_data(
        'export', ['85', '87', '39'], 'industrial_exports', industrial_base)

    # Dataset 6: Petrochemical Imports (HS 29)
    petrochem_base = {
        '29': {
            'China': 1500, 'Japan': 1200, 'Korea, Republic of': 1000,
            'Singapore': 800, 'Saudi Arabia': 700,
            'United States of America': 600, 'Germany': 500,
            'Taiwan': 400, 'India': 350, 'Malaysia': 300,
            'Indonesia': 250, 'United Arab Emirates': 200,
            'Iran': 180, 'Qatar': 150, 'Netherlands': 120,
            'Thailand': 100, 'Belgium': 80,
        }
    }
    datasets['petrochemical_imports'] = generate_harmonize_data(
        'import', ['29'], 'petrochemical_imports', petrochem_base)

    # Create combined Excel
    print("\nCreating combined Excel file...")
    excel_path = os.path.join(RAW_DIR, 'thailand_trade_raw_data.xlsx')
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for name, df in datasets.items():
            df.to_excel(writer, sheet_name=name, index=False)

        # Metadata
        meta_rows = []
        for name, df in datasets.items():
            meta_rows.append({
                'dataset': name,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': ', '.join(df.columns.tolist()),
                'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source': 'SIMULATED (for pipeline demonstration)',
                'note': 'Run 01_data_collection.py for real API data from dataapi.moc.go.th',
            })
        pd.DataFrame(meta_rows).to_excel(writer, sheet_name='metadata', index=False)

    print(f"  Saved: {excel_path}")

    # Summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    total = 0
    for name, df in datasets.items():
        print(f"  {name}: {len(df):,} rows")
        total += len(df)
    print(f"\n  TOTAL: {total:,} rows")
    print("="*60)


if __name__ == '__main__':
    main()
