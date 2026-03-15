"""
utils.py — Shared utility functions for Thailand Trade Impact Analysis
DADS 5001 Mini-Project | DADS, NIDA
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np
import os

# ============================================================
# VISUALIZATION CONFIG — Cole Nussbaumer Knaflic Standards
# ============================================================

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'axes.grid.axis': 'y',
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.pad_inches': 0.3,
})

COLORS = {
    'primary': '#2C5F8A',
    'secondary': '#7FAACC',
    'highlight': '#E74C3C',
    'positive': '#27AE60',
    'negative': '#C0392B',
    'neutral': '#95A5A6',
    'crisis_covid': '#F39C12',
    'crisis_ru': '#8E44AD',
    'crisis_12day': '#E67E22',
    'crisis_iran': '#C0392B',
}

CRISIS_COLORS = {
    'Pre-COVID': '#95A5A6',
    'COVID-19': '#F39C12',
    'Post-COVID': '#7FAACC',
    'Russia-Ukraine': '#8E44AD',
    'Post-RU War': '#2C5F8A',
    '12-Day War': '#E67E22',
    'Post-12-Day': '#3498DB',
    'Iran War': '#C0392B',
}

HS_DESCRIPTIONS = {
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

# Region classification
REGION_MAP = {
    # Middle East - Hormuz
    'Iran': 'Middle East - Hormuz',
    'Iraq': 'Middle East - Hormuz',
    'Kuwait': 'Middle East - Hormuz',
    'Qatar': 'Middle East - Hormuz',
    'United Arab Emirates': 'Middle East - Hormuz',
    'Bahrain': 'Middle East - Hormuz',
    'Saudi Arabia': 'Middle East - Hormuz',
    'Oman': 'Middle East - Hormuz',
    # Middle East - Non-Hormuz
    'Israel': 'Middle East - Non-Hormuz',
    'Jordan': 'Middle East - Non-Hormuz',
    'Lebanon': 'Middle East - Non-Hormuz',
    'Yemen': 'Middle East - Non-Hormuz',
    'Syria': 'Middle East - Non-Hormuz',
    'Turkey': 'Middle East - Non-Hormuz',
    'Egypt': 'Middle East - Non-Hormuz',
    # ASEAN
    'Malaysia': 'ASEAN',
    'Singapore': 'ASEAN',
    'Indonesia': 'ASEAN',
    'Vietnam': 'ASEAN',
    'Viet Nam': 'ASEAN',
    'Philippines': 'ASEAN',
    'Myanmar': 'ASEAN',
    'Cambodia': 'ASEAN',
    'Laos': 'ASEAN',
    "Lao People's Democratic Republic": 'ASEAN',
    'Brunei': 'ASEAN',
    'Brunei Darussalam': 'ASEAN',
    # East Asia
    'China': 'East Asia',
    "China, People's Republic of": 'East Asia',
    'Japan': 'East Asia',
    'South Korea': 'East Asia',
    'Korea, Republic of': 'East Asia',
    'Taiwan': 'East Asia',
    'Hong Kong': 'East Asia',
    'Hong Kong, China': 'East Asia',
    # South Asia
    'India': 'South Asia',
    'Bangladesh': 'South Asia',
    'Pakistan': 'South Asia',
    'Sri Lanka': 'South Asia',
    # Americas
    'United States': 'Americas',
    'United States of America': 'Americas',
    'Canada': 'Americas',
    'Brazil': 'Americas',
    'Mexico': 'Americas',
    'Argentina': 'Americas',
    'Chile': 'Americas',
    'Colombia': 'Americas',
    'Peru': 'Americas',
    # Oceania
    'Australia': 'Oceania',
    'New Zealand': 'Oceania',
    # Europe (common ones)
    'Germany': 'Europe',
    'United Kingdom': 'Europe',
    'France': 'Europe',
    'Italy': 'Europe',
    'Netherlands': 'Europe',
    'Spain': 'Europe',
    'Belgium': 'Europe',
    'Switzerland': 'Europe',
    'Sweden': 'Europe',
    'Poland': 'Europe',
    'Russia': 'Europe',
    'Russian Federation': 'Europe',
    # Africa
    'South Africa': 'Africa',
    'Nigeria': 'Africa',
    'Kenya': 'Africa',
    'Ghana': 'Africa',
    'Ethiopia': 'Africa',
    'Tanzania': 'Africa',
    'Libya': 'Africa',
    'Sudan': 'Africa',
    'Morocco': 'Africa',
    'Algeria': 'Africa',
    'Tunisia': 'Africa',
}

SHIPPING_ROUTE_MAP = {
    'Middle East - Hormuz': 'Via Hormuz',
    'Middle East - Non-Hormuz': 'Via Suez/Red Sea',
    'Europe': 'Via Suez/Red Sea',
    'Africa': 'Via Cape of Good Hope',
    'Americas': 'Via Cape of Good Hope',
    'ASEAN': 'Pacific/Direct',
    'East Asia': 'Pacific/Direct',
    'South Asia': 'Pacific/Direct',
    'Oceania': 'Pacific/Direct',
    'Others': 'Pacific/Direct',
}


def create_figure(fig_number, title, subtitle, width=12, height=6):
    """Create a figure with standardized title, subtitle, and figure number."""
    fig, ax = plt.subplots(figsize=(width, height))
    fig.suptitle(f'Figure {fig_number}: {title}',
                 fontsize=14, fontweight='bold', y=1.02)
    ax.set_title(subtitle, fontsize=10, color='gray', pad=10)
    return fig, ax


def create_multi_figure(fig_number, title, subtitle, nrows=1, ncols=2, width=14, height=6):
    """Create a multi-subplot figure with standardized formatting."""
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(width, height))
    fig.suptitle(f'Figure {fig_number}: {title}',
                 fontsize=14, fontweight='bold', y=1.05)
    fig.text(0.5, 0.98, subtitle, ha='center', fontsize=10, color='gray')
    return fig, axes


def add_caption(fig, caption_text,
                source_text="Source: tradereport.moc.go.th (Ministry of Commerce, Thailand)"):
    """Add caption and source credit below every figure."""
    fig.text(0.5, -0.05, caption_text, ha='center', fontsize=9,
             style='italic', wrap=True)
    fig.text(0.5, -0.10, source_text, ha='center', fontsize=8, color='gray')


def save_figure(fig, filename, fig_number):
    """Save figure as white-background PNG."""
    os.makedirs('outputs/figures', exist_ok=True)
    filepath = f'outputs/figures/{fig_number:02d}_{filename}.png'
    fig.savefig(filepath, facecolor='white', edgecolor='none',
                bbox_inches='tight', dpi=150, pad_inches=0.3)
    plt.close(fig)
    print(f"  Saved: {filepath}")
    return filepath


def classify_region(country_name):
    """Classify a country into a region group."""
    return REGION_MAP.get(country_name, 'Others')


def classify_shipping_route(region):
    """Classify shipping route based on region."""
    return SHIPPING_ROUTE_MAP.get(region, 'Pacific/Direct')


def classify_crisis_period(date):
    """Classify a date into a crisis period."""
    if pd.isna(date):
        return 'Unknown'
    if date < pd.Timestamp('2020-03-01'):
        return 'Pre-COVID'
    elif date < pd.Timestamp('2022-01-01'):
        return 'COVID-19'
    elif date < pd.Timestamp('2022-02-01'):
        return 'Post-COVID'
    elif date < pd.Timestamp('2023-10-01'):
        return 'Russia-Ukraine'
    elif date < pd.Timestamp('2025-06-01'):
        return 'Post-RU War'
    elif date < pd.Timestamp('2025-07-01'):
        return '12-Day War'
    elif date < pd.Timestamp('2026-02-01'):
        return 'Post-12-Day'
    else:
        return 'Iran War'


def format_value_millions(value):
    """Format value in millions USD with comma separator."""
    return f"{value / 1e6:,.1f}M"


def format_value_billions(value):
    """Format value in billions USD."""
    return f"{value / 1e9:,.2f}B"


def add_crisis_shading(ax, date_min, date_max):
    """Add shaded regions for crisis periods on a time-series chart."""
    crisis_periods = [
        ('COVID-19', '2020-03-01', '2021-12-31', CRISIS_COLORS['COVID-19'], 0.1),
        ('Russia-Ukraine', '2022-02-01', '2023-09-30', CRISIS_COLORS['Russia-Ukraine'], 0.1),
        ('12-Day War', '2025-06-01', '2025-06-30', CRISIS_COLORS['12-Day War'], 0.15),
        ('Iran War', '2026-02-01', '2026-12-31', CRISIS_COLORS['Iran War'], 0.15),
    ]
    for label, start, end, color, alpha in crisis_periods:
        start_dt = pd.Timestamp(start)
        end_dt = pd.Timestamp(end)
        if start_dt <= date_max and end_dt >= date_min:
            ax.axvspan(max(start_dt, date_min), min(end_dt, date_max),
                       alpha=alpha, color=color, label=label)
