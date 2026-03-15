"""
03_eda_analysis.py — Exploratory Data Analysis: 10 Key Insights
DADS 5001 Mini-Project | Thailand Trade Impact Analysis
Author: DADS, NIDA

Generates 10 publication-quality visualizations following
Cole Nussbaumer Knaflic's Storytelling with Data principles.
Each figure follows ALL 10 visualization rules:
  1. Figure number  2. Title  3. Subtitle  4. Axis labels with units
  5. Legend  6. Caption  7. Source  8. White background
  9. Abbreviation explanations  10. Semantic colors
"""

import sys
import os
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Import shared utilities
# ---------------------------------------------------------------------------
sys.path.insert(0, 'src')
from utils import (COLORS, CRISIS_COLORS, HS_DESCRIPTIONS,
                   create_figure, create_multi_figure, add_caption, save_figure,
                   add_crisis_shading, format_value_millions)

# Convenience lists
HORMUZ_COUNTRIES = [
    'Iran', 'Iraq', 'Kuwait', 'Qatar', 'United Arab Emirates',
    'Bahrain', 'Saudi Arabia', 'Oman',
]

MAJOR_CRISIS_PERIODS = ['Pre-COVID', 'COVID-19', 'Russia-Ukraine',
                        '12-Day War', 'Iran War']


# ===================================================================
# HELPER FUNCTIONS
# ===================================================================

def _safe_date(df):
    """Ensure the date column is datetime."""
    if 'date' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df


def _get_crisis_order():
    """Return ordered list of crisis periods for categorical axes."""
    return ['Pre-COVID', 'COVID-19', 'Post-COVID', 'Russia-Ukraine',
            'Post-RU War', '12-Day War', 'Post-12-Day', 'Iran War']


def _filter_dataset(df, name):
    """Filter rows for a given dataset name."""
    return df[df['dataset'] == name].copy()


def _millions(ax, axis='y'):
    """Format axis tick labels as millions (M)."""
    fmt = mticker.FuncFormatter(lambda x, _: f'{x / 1e6:,.0f}M')
    if axis == 'y':
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)


# ===================================================================
# INSIGHT 1: "Risk Map" — Import Structure by Shipping Route
# ===================================================================

def insight_1(df):
    """Figure 1 — Stacked bar of import share by shipping route + pie for
    energy dependency on Hormuz."""
    print("\n" + "=" * 60)
    print("INSIGHT 1: Risk Map — Import Structure by Shipping Route")
    print("=" * 60)

    # --- data prep ---
    energy = _filter_dataset(df, 'energy_imports')
    overview = _filter_dataset(df, 'trade_overview')

    # For overview rows, use import_value_usd; for energy rows, use value_usd
    # Build import value per shipping route from both datasets
    parts = []

    if not overview.empty and 'import_value_usd' in overview.columns:
        ov = overview[['shipping_route', 'import_value_usd', 'crisis_period']].copy()
        ov = ov.rename(columns={'import_value_usd': 'value'})
        ov['source'] = 'Overview'
        parts.append(ov)

    if not energy.empty and 'value_usd' in energy.columns:
        en = energy[['shipping_route', 'value_usd', 'crisis_period']].copy()
        en = en.rename(columns={'value_usd': 'value'})
        en['source'] = 'Energy'
        parts.append(en)

    if not parts:
        print("  [SKIP] No data available for Insight 1.")
        return

    combined = pd.concat(parts, ignore_index=True)
    combined = combined.dropna(subset=['value', 'shipping_route'])

    # --- Panel A: Stacked bar by crisis period ---
    route_crisis = (combined.groupby(['crisis_period', 'shipping_route'])['value']
                    .sum().unstack(fill_value=0))
    # Filter to major periods and reorder
    available = [p for p in _get_crisis_order() if p in route_crisis.index]
    route_crisis = route_crisis.loc[available]
    # Normalise to shares
    route_pct = route_crisis.div(route_crisis.sum(axis=1), axis=0) * 100

    route_colors = {
        'Via Hormuz': COLORS['highlight'],
        'Via Suez/Red Sea': COLORS['crisis_ru'],
        'Pacific/Direct': COLORS['primary'],
        'Via Cape of Good Hope': COLORS['neutral'],
    }

    fig, axes = create_multi_figure(
        1,
        '"Risk Map" — Thailand Import Structure by Shipping Route',
        'Import share (%) by route across crisis periods  |  Energy dependency on Strait of Hormuz',
        nrows=1, ncols=2, width=16, height=7,
    )

    ax1, ax2 = axes

    route_pct.plot.bar(
        stacked=True, ax=ax1,
        color=[route_colors.get(c, '#CCCCCC') for c in route_pct.columns],
        edgecolor='white', linewidth=0.5,
    )
    ax1.set_ylabel('Share of Total Import Value (%)')
    ax1.set_xlabel('Crisis Period')
    ax1.set_ylim(0, 100)
    ax1.legend(title='Shipping Route', fontsize=8, title_fontsize=9,
               loc='upper left', bbox_to_anchor=(0, 1))
    ax1.tick_params(axis='x', rotation=30)
    ax1.set_title('A) Import Share by Shipping Route', fontsize=11, fontweight='bold')

    # --- Panel B: Pie chart — energy imports via Hormuz vs rest ---
    if not energy.empty:
        hormuz_val = energy.loc[
            energy['shipping_route'] == 'Via Hormuz', 'value_usd'
        ].sum()
        other_val = energy.loc[
            energy['shipping_route'] != 'Via Hormuz', 'value_usd'
        ].sum()
    else:
        hormuz_val, other_val = 0, 0

    sizes = [hormuz_val, other_val]
    labels = [f'Via Hormuz\n({hormuz_val / (hormuz_val + other_val) * 100:.1f}%)'
              if (hormuz_val + other_val) > 0 else 'Via Hormuz',
              f'Other Routes\n({other_val / (hormuz_val + other_val) * 100:.1f}%)'
              if (hormuz_val + other_val) > 0 else 'Other Routes']
    pie_colors = [COLORS['highlight'], COLORS['secondary']]

    ax2.pie(sizes, labels=labels, colors=pie_colors,
            startangle=90, textprops={'fontsize': 10},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax2.set_title('B) Energy Import Dependency on Hormuz', fontsize=11, fontweight='bold')

    add_caption(
        fig,
        'Hormuz = Strait of Hormuz (Iran, Iraq, Kuwait, Qatar, UAE, Bahrain, Saudi Arabia, Oman). '
        'GCC = Gulf Cooperation Council.',
        source_text='Source: tradereport.moc.go.th (Ministry of Commerce, Thailand)',
    )

    save_figure(fig, 'risk_map_shipping_route', 1)

    pct_hormuz = hormuz_val / (hormuz_val + other_val) * 100 if (hormuz_val + other_val) > 0 else 0
    print(f"  Finding: {pct_hormuz:.1f}% of Thailand's energy imports transit the Strait of Hormuz.")
    print("  Implication: Hormuz disruptions pose a critical supply-chain risk.\n")


# ===================================================================
# INSIGHT 2: Trade Balance Comparison Across 4 Crises
# ===================================================================

def insight_2(df):
    """Figure 2 — Monthly trade balance with crisis-period shading."""
    print("\n" + "=" * 60)
    print("INSIGHT 2: Trade Balance Comparison Across 4 Crises")
    print("=" * 60)

    overview = _filter_dataset(df, 'trade_overview')
    if overview.empty:
        print("  [SKIP] No trade_overview data.")
        return

    overview = _safe_date(overview)

    # Compute monthly trade balance
    if 'export_value_usd' in overview.columns and 'import_value_usd' in overview.columns:
        monthly = (overview.groupby('date')
                   .agg(exports=('export_value_usd', 'sum'),
                        imports=('import_value_usd', 'sum'))
                   .reset_index())
    else:
        print("  [SKIP] Missing export/import value columns.")
        return

    monthly['trade_balance'] = monthly['exports'] - monthly['imports']
    monthly = monthly.sort_values('date')

    fig, ax = create_figure(
        2,
        'Thailand Monthly Trade Balance Across 4 Crises',
        'Trade balance = Exports − Imports (USD)  |  Shaded areas indicate crisis periods',
        width=14, height=6,
    )

    ax.plot(monthly['date'], monthly['trade_balance'],
            color=COLORS['primary'], linewidth=1.5, label='Trade Balance')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='-')

    # Fill positive / negative areas
    ax.fill_between(monthly['date'], monthly['trade_balance'], 0,
                     where=monthly['trade_balance'] >= 0,
                     color=COLORS['positive'], alpha=0.15, label='Surplus')
    ax.fill_between(monthly['date'], monthly['trade_balance'], 0,
                     where=monthly['trade_balance'] < 0,
                     color=COLORS['negative'], alpha=0.15, label='Deficit')

    add_crisis_shading(ax, monthly['date'].min(), monthly['date'].max())

    _millions(ax)
    ax.set_ylabel('Trade Balance (USD, millions)')
    ax.set_xlabel('Date')
    ax.legend(loc='lower left', fontsize=8, ncol=3)

    add_caption(
        fig,
        'Trade balance deteriorates during energy price shocks (Russia-Ukraine, Iran War) '
        'as import costs surge while exports remain relatively stable.',
    )

    save_figure(fig, 'trade_balance_crises', 2)

    avg_bal = monthly['trade_balance'].mean()
    print(f"  Finding: Average monthly trade balance = {format_value_millions(avg_bal)} USD.")
    min_row = monthly.loc[monthly['trade_balance'].idxmin()]
    print(f"  Worst month: {min_row['date'].strftime('%Y-%m')} "
          f"({format_value_millions(min_row['trade_balance'])} USD).\n")


# ===================================================================
# INSIGHT 3: "Energy Crisis" — Price Effect vs Volume Effect
# ===================================================================

def insight_3(df):
    """Figure 3 — Dual-axis: value (bars) vs quantity (line) for energy imports."""
    print("\n" + "=" * 60)
    print("INSIGHT 3: Energy Crisis — Price Effect vs Volume Effect")
    print("=" * 60)

    energy = _filter_dataset(df, 'energy_imports')
    if energy.empty:
        print("  [SKIP] No energy_imports data.")
        return

    energy = _safe_date(energy)

    monthly = (energy.groupby('date')
               .agg(total_value=('value_usd', 'sum'),
                    total_qty=('quantity', 'sum'))
               .reset_index()
               .sort_values('date'))

    fig, ax1 = create_figure(
        3,
        '"Energy Crisis" — Price Effect vs Volume Effect',
        'When value rises but volume falls, it signals a price shock, not increased consumption',
        width=14, height=6,
    )

    # Bars for value
    ax1.bar(monthly['date'], monthly['total_value'],
            width=25, color=COLORS['highlight'], alpha=0.6, label='Import Value (USD)')
    _millions(ax1)
    ax1.set_ylabel('Total Import Value (USD, millions)', color=COLORS['highlight'])
    ax1.set_xlabel('Date')

    # Secondary axis for quantity
    ax2 = ax1.twinx()
    ax2.plot(monthly['date'], monthly['total_qty'],
             color=COLORS['primary'], linewidth=2, label='Import Volume (Quantity)')
    ax2.set_ylabel('Import Volume (quantity units)', color=COLORS['primary'])
    ax2.spines['right'].set_visible(True)

    add_crisis_shading(ax1, monthly['date'].min(), monthly['date'].max())

    # Merged legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

    add_caption(
        fig,
        'Price effect = rising import cost per unit; Volume effect = change in physical quantity imported. '
        'A divergence between the two curves indicates a price-driven cost increase.',
    )

    save_figure(fig, 'energy_price_vs_volume', 3)

    # Correlation
    corr = monthly[['total_value', 'total_qty']].corr().iloc[0, 1]
    print(f"  Finding: Value–Volume correlation = {corr:.2f}.")
    print("  A low or negative correlation during crises confirms price shocks.\n")


# ===================================================================
# INSIGHT 4: "Domino Effect" — Fertilizer → Agriculture Supply Chain
# ===================================================================

def insight_4(df):
    """Figure 4 — Dual line chart + lag-correlation heatmap."""
    print("\n" + "=" * 60)
    print("INSIGHT 4: Domino Effect — Fertilizer → Agriculture Supply Chain")
    print("=" * 60)

    fert = _filter_dataset(df, 'fertilizer_imports')
    agri = _filter_dataset(df, 'agrifood_exports')

    if fert.empty or agri.empty:
        print("  [SKIP] Missing fertilizer or agrifood data.")
        return

    fert = _safe_date(fert)
    agri = _safe_date(agri)

    fert_m = (fert.groupby('date')['value_usd'].sum()
              .reset_index().rename(columns={'value_usd': 'fert_value'})
              .sort_values('date'))
    agri_m = (agri.groupby('date')['value_usd'].sum()
              .reset_index().rename(columns={'value_usd': 'agri_value'})
              .sort_values('date'))

    merged = pd.merge(fert_m, agri_m, on='date', how='inner')

    fig, axes = create_multi_figure(
        4,
        '"Domino Effect" — Fertilizer Import Cost → Agri-Food Export Value',
        'Rising fertilizer costs propagate through Thailand\'s agricultural supply chain with a lag',
        nrows=1, ncols=2, width=16, height=6,
    )

    ax1, ax2 = axes

    # Panel A — dual line
    ax1.plot(merged['date'], merged['fert_value'],
             color=COLORS['negative'], linewidth=1.5, label='Fertilizer Imports (USD)')
    ax1_b = ax1.twinx()
    ax1_b.plot(merged['date'], merged['agri_value'],
               color=COLORS['positive'], linewidth=1.5, label='Agri-Food Exports (USD)')
    ax1.set_ylabel('Fertilizer Import Value (USD)', color=COLORS['negative'])
    ax1_b.set_ylabel('Agri-Food Export Value (USD)', color=COLORS['positive'])
    ax1.set_xlabel('Date')
    _millions(ax1)
    _millions(ax1_b)

    lines_a, lab_a = ax1.get_legend_handles_labels()
    lines_b, lab_b = ax1_b.get_legend_handles_labels()
    ax1.legend(lines_a + lines_b, lab_a + lab_b, fontsize=8, loc='upper left')
    ax1.set_title('A) Monthly Trends', fontsize=11, fontweight='bold')
    ax1_b.spines['right'].set_visible(True)

    # Panel B — lag correlation heatmap
    lags = range(0, 7)
    corrs = []
    for lag in lags:
        shifted = merged['fert_value'].shift(lag)
        valid = pd.concat([shifted, merged['agri_value']], axis=1).dropna()
        if len(valid) > 3:
            c = valid.iloc[:, 0].corr(valid.iloc[:, 1])
        else:
            c = np.nan
        corrs.append(c)

    corr_df = pd.DataFrame({'Lag (months)': list(lags), 'Correlation': corrs})
    sns.heatmap(corr_df.set_index('Lag (months)').T, annot=True, fmt='.2f',
                cmap='RdYlGn_r', center=0, ax=ax2, cbar_kws={'shrink': 0.8})
    ax2.set_title('B) Lag Correlation: Fertilizer → Agri-Food', fontsize=11, fontweight='bold')
    ax2.set_ylabel('')

    add_caption(
        fig,
        'HS 31 = Fertilizers | HS 10 = Cereals (Rice) | HS 16 = Canned Food | HS 17 = Sugars. '
        'Lag N means fertilizer cost leads agri-food export by N months.',
    )

    save_figure(fig, 'domino_effect_fertilizer_agri', 4)

    best_lag = corr_df.loc[corr_df['Correlation'].abs().idxmax()]
    print(f"  Finding: Strongest correlation at lag = {int(best_lag['Lag (months)'])} months "
          f"(r = {best_lag['Correlation']:.2f}).")
    print("  Implication: Fertilizer price shocks propagate to food exports with a delay.\n")


# ===================================================================
# INSIGHT 5: Trade with Conflict Countries (Iran + GCC)
# ===================================================================

def insight_5(df):
    """Figure 5 — Grouped bar chart of trade with Hormuz countries by crisis."""
    print("\n" + "=" * 60)
    print("INSIGHT 5: Trade with Conflict Countries (Iran + GCC)")
    print("=" * 60)

    overview = _filter_dataset(df, 'trade_overview')
    if overview.empty:
        print("  [SKIP] No trade_overview data.")
        return

    # Filter for Hormuz countries
    hormuz = overview[overview['country_eng'].isin(HORMUZ_COUNTRIES)].copy()
    if hormuz.empty:
        print("  [SKIP] No Hormuz-country data found in trade_overview.")
        return

    # Use import_value_usd
    val_col = 'import_value_usd' if 'import_value_usd' in hormuz.columns else 'value_usd'
    grp = (hormuz.groupby(['crisis_period', 'country_eng'])[val_col]
           .sum().reset_index())
    available_periods = [p for p in _get_crisis_order() if p in grp['crisis_period'].unique()]
    grp = grp[grp['crisis_period'].isin(available_periods)]

    pivot = grp.pivot_table(index='country_eng', columns='crisis_period',
                            values=val_col, aggfunc='sum', fill_value=0)
    pivot = pivot[[p for p in available_periods if p in pivot.columns]]

    fig, ax = create_figure(
        5,
        'Thailand Trade with Strait of Hormuz Countries Across Crises',
        'Import value (USD) comparison for GCC + Iran by crisis period',
        width=14, height=7,
    )

    crisis_color_list = [CRISIS_COLORS.get(p, '#999999') for p in pivot.columns]
    pivot.plot.bar(ax=ax, color=crisis_color_list, edgecolor='white', width=0.8)

    _millions(ax)
    ax.set_ylabel('Import Value (USD, millions)')
    ax.set_xlabel('Country')
    ax.legend(title='Crisis Period', fontsize=8, title_fontsize=9)
    ax.tick_params(axis='x', rotation=30)

    add_caption(
        fig,
        'GCC = Gulf Cooperation Council (Saudi Arabia, UAE, Kuwait, Qatar, Bahrain, Oman). '
        'Hormuz = Strait of Hormuz, through which ~20% of global oil transits.',
    )

    save_figure(fig, 'trade_hormuz_countries', 5)

    top_country = grp.groupby('country_eng')[val_col].sum().idxmax()
    print(f"  Finding: Top Hormuz-region trade partner = {top_country}.")
    print("  Iran War crisis may sever or disrupt trade with all Hormuz partners.\n")


# ===================================================================
# INSIGHT 6: Impact on Vehicles & Electronics Exports
# ===================================================================

def insight_6(df):
    """Figure 6 — Growth-rate comparison: HS 85 vs HS 87 across crises."""
    print("\n" + "=" * 60)
    print("INSIGHT 6: Impact on Vehicles & Electronics Exports")
    print("=" * 60)

    ind = _filter_dataset(df, 'industrial_exports')
    if ind.empty:
        print("  [SKIP] No industrial_exports data.")
        return

    ind = _safe_date(ind)
    # Ensure hs_code is string for matching
    ind['hs_code'] = ind['hs_code'].astype(str).str[:2]

    hs85 = ind[ind['hs_code'] == '85'].copy()
    hs87 = ind[ind['hs_code'] == '87'].copy()

    def _crisis_growth(sub, label):
        grp = sub.groupby('crisis_period')['value_usd'].sum()
        return grp.rename(label)

    g85 = _crisis_growth(hs85, 'HS 85 — Electronics')
    g87 = _crisis_growth(hs87, 'HS 87 — Vehicles')

    combined = pd.DataFrame({'HS 85 — Electronics': g85, 'HS 87 — Vehicles': g87}).fillna(0)
    available = [p for p in _get_crisis_order() if p in combined.index]
    combined = combined.loc[available]

    # Compute growth rate relative to Pre-COVID (baseline)
    baseline = combined.iloc[0] if not combined.empty else combined.mean()
    baseline = baseline.replace(0, np.nan)
    growth = ((combined - baseline) / baseline * 100)

    fig, axes = create_multi_figure(
        6,
        'Impact on Vehicles & Electronics Exports',
        'HS 85 = Electrical Machinery & Electronics  |  HS 87 = Vehicles & Parts',
        nrows=1, ncols=2, width=16, height=7,
    )

    ax1, ax2 = axes

    # Panel A — Total value per crisis period (waterfall-style grouped bar)
    combined_m = combined / 1e6  # millions
    combined_m.plot.bar(ax=ax1,
                        color=[COLORS['primary'], COLORS['highlight']],
                        edgecolor='white', width=0.7)
    ax1.set_ylabel('Export Value (USD, millions)')
    ax1.set_xlabel('Crisis Period')
    ax1.set_title('A) Total Export Value by Period', fontsize=11, fontweight='bold')
    ax1.tick_params(axis='x', rotation=30)
    ax1.legend(fontsize=8)

    # Panel B — Growth rate relative to first period
    growth.plot.bar(ax=ax2,
                    color=[COLORS['primary'], COLORS['highlight']],
                    edgecolor='white', width=0.7)
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_ylabel('Growth Rate vs Baseline (%)')
    ax2.set_xlabel('Crisis Period')
    ax2.set_title('B) Growth Rate vs Pre-COVID Baseline', fontsize=11, fontweight='bold')
    ax2.tick_params(axis='x', rotation=30)
    ax2.legend(fontsize=8)

    add_caption(
        fig,
        'HS 85 includes semiconductors, circuit boards, hard-disk drives. '
        'HS 87 includes passenger cars, pick-up trucks, auto parts. '
        'Baseline = first available crisis period.',
    )

    save_figure(fig, 'vehicles_electronics_exports', 6)

    print("  Finding: Electronics and vehicles — Thailand's top industrial exports —")
    print("  are sensitive to energy cost shocks via input-price inflation.\n")


# ===================================================================
# INSIGHT 7: "Food is Gold" — Agri-Food Winners
# ===================================================================

def insight_7(df):
    """Figure 7 — Agri-food (HS 10, 16, 17) export performance across crises."""
    print("\n" + "=" * 60)
    print('INSIGHT 7: "Food is Gold" — Agri-Food Export Winners')
    print("=" * 60)

    agri = _filter_dataset(df, 'agrifood_exports')
    if agri.empty:
        print("  [SKIP] No agrifood_exports data.")
        return

    agri = _safe_date(agri)
    agri['hs2'] = agri['hs_code'].astype(str).str[:2]

    target_hs = ['10', '16', '17']
    agri_f = agri[agri['hs2'].isin(target_hs)].copy()

    if agri_f.empty:
        print("  [SKIP] No HS 10/16/17 data in agrifood_exports.")
        return

    # Map descriptions
    agri_f['hs_label'] = agri_f['hs2'].map(HS_DESCRIPTIONS).fillna(agri_f['hs2'])

    fig, axes = create_multi_figure(
        7,
        '"Food is Gold" — Agri-Food Export Winners During Crises',
        'HS 10 = Rice | HS 16 = Canned Food | HS 17 = Sugars  —  Thailand\'s food exports thrive in crises',
        nrows=1, ncols=2, width=16, height=7,
    )

    ax1, ax2 = axes

    # Panel A — Grouped bar by crisis period
    crisis_hs = (agri_f.groupby(['crisis_period', 'hs_label'])['value_usd']
                 .sum().reset_index())
    available = [p for p in _get_crisis_order() if p in crisis_hs['crisis_period'].unique()]
    crisis_hs = crisis_hs[crisis_hs['crisis_period'].isin(available)]

    pivot = crisis_hs.pivot_table(index='crisis_period', columns='hs_label',
                                  values='value_usd', aggfunc='sum', fill_value=0)
    pivot = pivot.loc[[p for p in available if p in pivot.index]]

    hs_colors = [COLORS['positive'], COLORS['primary'], COLORS['secondary']]
    (pivot / 1e6).plot.bar(ax=ax1, color=hs_colors[:len(pivot.columns)],
                           edgecolor='white', width=0.75)
    ax1.set_ylabel('Export Value (USD, millions)')
    ax1.set_xlabel('Crisis Period')
    ax1.set_title('A) Exports by Product & Crisis', fontsize=11, fontweight='bold')
    ax1.tick_params(axis='x', rotation=30)
    ax1.legend(fontsize=8)

    # Panel B — Top growing destination markets (horizontal bar)
    market_growth = (agri_f.groupby(['country_eng', 'crisis_period'])['value_usd']
                     .sum().reset_index())
    # Compute latest vs earliest period growth
    if len(available) >= 2:
        early = market_growth[market_growth['crisis_period'] == available[0]]
        late = market_growth[market_growth['crisis_period'] == available[-1]]
        comp = pd.merge(early[['country_eng', 'value_usd']],
                        late[['country_eng', 'value_usd']],
                        on='country_eng', suffixes=('_early', '_late'), how='outer').fillna(0)
        comp['growth'] = comp['value_usd_late'] - comp['value_usd_early']
        comp = comp.sort_values('growth', ascending=True).tail(10)
    else:
        comp = (agri_f.groupby('country_eng')['value_usd'].sum()
                .nlargest(10).reset_index())
        comp['growth'] = comp['value_usd']

    bar_colors = [COLORS['positive'] if g >= 0 else COLORS['negative'] for g in comp['growth']]
    ax2.barh(comp['country_eng'], comp['growth'] / 1e6, color=bar_colors, edgecolor='white')
    ax2.set_xlabel('Growth in Export Value (USD, millions)')
    ax2.set_ylabel('Destination Country')
    ax2.set_title('B) Top Growing Export Markets', fontsize=11, fontweight='bold')
    ax2.axvline(0, color='black', linewidth=0.8)

    add_caption(
        fig,
        'Thailand is a global leader in rice, canned tuna, and sugar exports. '
        f'Comparison: {available[0]} vs {available[-1]}.' if len(available) >= 2
        else 'Thailand is a global leader in rice, canned tuna, and sugar exports.',
    )

    save_figure(fig, 'agrifood_winners', 7)

    total_agri = agri_f['value_usd'].sum()
    print(f"  Finding: Total agri-food (HS 10/16/17) exports = {format_value_millions(total_agri)} USD.")
    print("  Food exports often increase during geopolitical crises as global prices rise.\n")


# ===================================================================
# INSIGHT 8: "Natural Rubber vs Synthetic" — Substitution Effect
# ===================================================================

def insight_8(df):
    """Figure 8 — Scatter + regression: oil proxy vs rubber exports; area trend."""
    print("\n" + "=" * 60)
    print('INSIGHT 8: Natural Rubber vs Synthetic — Substitution Effect')
    print("=" * 60)

    energy = _filter_dataset(df, 'energy_imports')
    agri = _filter_dataset(df, 'agrifood_exports')

    if energy.empty or agri.empty:
        print("  [SKIP] Missing energy or agrifood data.")
        return

    energy = _safe_date(energy)
    agri = _safe_date(agri)

    agri['hs2'] = agri['hs_code'].astype(str).str[:2]
    rubber = agri[agri['hs2'] == '40'].copy()
    if rubber.empty:
        print("  [SKIP] No HS 40 (rubber) data.")
        return

    # Monthly aggregates
    oil_price = (energy.groupby('date')
                 .agg(avg_unit_price=('unit_price_usd', 'mean'))
                 .reset_index())
    rubber_m = (rubber.groupby('date')['value_usd'].sum()
                .reset_index().rename(columns={'value_usd': 'rubber_value'}))

    merged = pd.merge(oil_price, rubber_m, on='date', how='inner').dropna()

    fig, axes = create_multi_figure(
        8,
        '"Natural Rubber vs Synthetic" — Oil Price Drives Rubber Export Value',
        'When oil prices rise, synthetic rubber costs more, boosting demand for Thailand\'s natural rubber',
        nrows=1, ncols=2, width=16, height=6,
    )

    ax1, ax2 = axes

    # Panel A — Scatter with regression
    x = merged['avg_unit_price'].values
    y = merged['rubber_value'].values / 1e6  # millions

    ax1.scatter(x, y, color=COLORS['primary'], alpha=0.6, edgecolors='white', s=50)

    # Regression line
    if len(x) > 2:
        slope, intercept, r_value, p_value, _ = stats.linregress(x, y)
        x_line = np.linspace(x.min(), x.max(), 100)
        ax1.plot(x_line, slope * x_line + intercept,
                 color=COLORS['highlight'], linewidth=2, linestyle='--',
                 label=f'Regression (R² = {r_value ** 2:.2f})')

    ax1.set_xlabel('Energy Import Unit Price (USD, proxy for oil price)')
    ax1.set_ylabel('Rubber Export Value (USD, millions)')
    ax1.set_title('A) Oil Price vs Rubber Exports', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=8)

    # Panel B — Area chart of rubber export trend
    rubber_m_sorted = rubber_m.sort_values('date')
    ax2.fill_between(rubber_m_sorted['date'],
                     rubber_m_sorted['rubber_value'] / 1e6,
                     color=COLORS['positive'], alpha=0.3)
    ax2.plot(rubber_m_sorted['date'],
             rubber_m_sorted['rubber_value'] / 1e6,
             color=COLORS['positive'], linewidth=1.5)
    add_crisis_shading(ax2, rubber_m_sorted['date'].min(), rubber_m_sorted['date'].max())
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Rubber Export Value (USD, millions)')
    ax2.set_title('B) Rubber Export Trend Over Time', fontsize=11, fontweight='bold')

    add_caption(
        fig,
        'HS 40 = Natural Rubber & Articles. When crude oil prices rise, synthetic rubber (petroleum-derived) '
        'becomes expensive, increasing demand for natural rubber — Thailand is the world\'s #1 producer.',
    )

    save_figure(fig, 'rubber_substitution_effect', 8)

    if len(x) > 2:
        print(f"  Finding: R² = {r_value ** 2:.2f} between energy unit price and rubber exports.")
    print("  Implication: Oil price surges benefit Thailand's natural rubber sector.\n")


# ===================================================================
# INSIGHT 9: "Dependency Scorecard" — Risk Ranking
# ===================================================================

def insight_9(df):
    """Figure 9 — Bubble chart: Hormuz dependency vs import value."""
    print("\n" + "=" * 60)
    print('INSIGHT 9: Dependency Scorecard — Risk Ranking')
    print("=" * 60)

    import_datasets = ['energy_imports', 'fertilizer_imports', 'petrochemical_imports']
    imp = df[df['dataset'].isin(import_datasets)].copy()

    if imp.empty:
        print("  [SKIP] No import dataset data.")
        return

    imp['hs2'] = imp['hs_code'].astype(str).str[:2]

    # Per HS category: total value and Hormuz share
    cat_total = imp.groupby('hs2')['value_usd'].sum()
    cat_hormuz = (imp[imp['shipping_route'] == 'Via Hormuz']
                  .groupby('hs2')['value_usd'].sum())

    scorecard = pd.DataFrame({
        'total_value': cat_total,
        'hormuz_value': cat_hormuz,
    }).fillna(0)
    scorecard['hormuz_pct'] = (scorecard['hormuz_value'] / scorecard['total_value'] * 100).fillna(0)
    scorecard['label'] = scorecard.index.map(
        lambda x: HS_DESCRIPTIONS.get(x, f'HS {x}')
    )
    scorecard = scorecard[scorecard['total_value'] > 0]

    if scorecard.empty:
        print("  [SKIP] No valid scorecard data.")
        return

    fig, ax = create_figure(
        9,
        '"Dependency Scorecard" — Thailand Import Risk Ranking',
        'Bubble size = total import value  |  Higher Hormuz dependency = higher risk of supply disruption',
        width=12, height=8,
    )

    # Normalise bubble size
    max_val = scorecard['total_value'].max()
    sizes = (scorecard['total_value'] / max_val) * 2000 + 100

    # Color by risk
    colors = []
    for pct in scorecard['hormuz_pct']:
        if pct >= 50:
            colors.append(COLORS['negative'])
        elif pct >= 20:
            colors.append(COLORS['crisis_covid'])
        else:
            colors.append(COLORS['positive'])

    scatter = ax.scatter(
        scorecard['hormuz_pct'],
        scorecard['total_value'] / 1e9,
        s=sizes,
        c=colors,
        alpha=0.7,
        edgecolors='white',
        linewidth=1.5,
    )

    # Risk zones
    ax.axvspan(50, 100, alpha=0.05, color=COLORS['negative'])
    ax.axvspan(20, 50, alpha=0.05, color=COLORS['crisis_covid'])
    ax.axvspan(0, 20, alpha=0.05, color=COLORS['positive'])
    ax.text(75, ax.get_ylim()[1] * 0.95, 'HIGH RISK', fontsize=9,
            color=COLORS['negative'], fontweight='bold', ha='center')
    ax.text(35, ax.get_ylim()[1] * 0.95, 'MEDIUM', fontsize=9,
            color=COLORS['crisis_covid'], fontweight='bold', ha='center')
    ax.text(10, ax.get_ylim()[1] * 0.95, 'LOW RISK', fontsize=9,
            color=COLORS['positive'], fontweight='bold', ha='center')

    # Labels
    for _, row in scorecard.iterrows():
        ax.annotate(row['label'], (row['hormuz_pct'], row['total_value'] / 1e9),
                    textcoords='offset points', xytext=(8, 5),
                    fontsize=8, fontweight='bold')

    ax.set_xlabel('Hormuz Dependency (% of import value via Strait of Hormuz)')
    ax.set_ylabel('Total Import Value (USD, billions)')
    ax.set_xlim(-5, 105)

    add_caption(
        fig,
        'Hormuz dependency = share of each commodity\'s imports that transit the Strait of Hormuz. '
        'Red zone (≥50%) = critical vulnerability. Products in red zone require immediate diversification.',
    )

    save_figure(fig, 'dependency_scorecard', 9)

    high_risk = scorecard[scorecard['hormuz_pct'] >= 50]
    print(f"  Finding: {len(high_risk)} product categories have ≥50% Hormuz dependency.")
    if not high_risk.empty:
        print(f"  High-risk items: {', '.join(high_risk['label'].tolist())}.")
    print()


# ===================================================================
# INSIGHT 10: "Diversification Roadmap"
# ===================================================================

def insight_10(df):
    """Figure 10 — Before/after energy import portfolio + scenario comparison."""
    print("\n" + "=" * 60)
    print('INSIGHT 10: Diversification Roadmap')
    print("=" * 60)

    energy = _filter_dataset(df, 'energy_imports')
    if energy.empty:
        print("  [SKIP] No energy_imports data.")
        return

    # Current portfolio by country (top 8 + Others)
    by_country = energy.groupby('country_eng')['value_usd'].sum().sort_values(ascending=False)
    top_n = 7
    top_countries = by_country.head(top_n)
    others = pd.Series({'Others': by_country.iloc[top_n:].sum()})
    current = pd.concat([top_countries, others])
    current_pct = current / current.sum() * 100

    # Simulated target diversification: reduce Hormuz countries by 40%, allocate to ASEAN/Oceania
    target = current.copy()
    hormuz_reduction = 0.4
    freed = 0
    for c in target.index:
        if c in HORMUZ_COUNTRIES:
            cut = target[c] * hormuz_reduction
            target[c] -= cut
            freed += cut
    # Allocate freed capacity
    non_hormuz = [c for c in target.index if c not in HORMUZ_COUNTRIES]
    if non_hormuz:
        alloc_per = freed / len(non_hormuz)
        for c in non_hormuz:
            target[c] += alloc_per
    target_pct = target / target.sum() * 100

    fig, axes = create_multi_figure(
        10,
        '"Diversification Roadmap" — Thailand Energy Import Strategy',
        'Reducing Hormuz dependency through supply-source diversification',
        nrows=1, ncols=2, width=16, height=7,
    )

    ax1, ax2 = axes

    # Color: Hormuz countries in red, others in blue-spectrum
    def _get_colors(idx):
        palette = sns.color_palette('Blues_r', n_colors=len(idx))
        return [COLORS['highlight'] if c in HORMUZ_COUNTRIES else palette[i]
                for i, c in enumerate(idx)]

    # Panel A — Current pie
    c_colors = _get_colors(current.index)
    wedges1, texts1, autotexts1 = ax1.pie(
        current_pct, labels=current.index, autopct='%1.1f%%',
        colors=c_colors, startangle=90,
        textprops={'fontsize': 8},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        pctdistance=0.8,
    )
    ax1.set_title('A) Current Energy Import Portfolio', fontsize=11, fontweight='bold')

    # Panel B — Scenario comparison bar chart
    scenario_df = pd.DataFrame({
        'Current (%)': current_pct,
        'Target (%)': target_pct,
    }).sort_values('Current (%)', ascending=True)

    y_pos = np.arange(len(scenario_df))
    bar_h = 0.35

    ax2.barh(y_pos - bar_h / 2, scenario_df['Current (%)'],
             height=bar_h, color=COLORS['highlight'], alpha=0.7, label='Current')
    ax2.barh(y_pos + bar_h / 2, scenario_df['Target (%)'],
             height=bar_h, color=COLORS['positive'], alpha=0.7, label='Target (-40% Hormuz)')

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(scenario_df.index, fontsize=9)
    ax2.set_xlabel('Share of Energy Imports (%)')
    ax2.set_title('B) Current vs Target Import Mix', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.axvline(0, color='black', linewidth=0.5)

    add_caption(
        fig,
        'Target scenario reduces Hormuz-dependent imports by 40% and reallocates to diversified sources '
        '(ASEAN, Oceania, Americas). Red = Hormuz-dependent source country.',
    )

    save_figure(fig, 'diversification_roadmap', 10)

    hormuz_current = current_pct[[c for c in current_pct.index if c in HORMUZ_COUNTRIES]].sum()
    hormuz_target = target_pct[[c for c in target_pct.index if c in HORMUZ_COUNTRIES]].sum()
    print(f"  Finding: Hormuz share — Current: {hormuz_current:.1f}% → Target: {hormuz_target:.1f}%.")
    print("  Recommendation: Accelerate energy imports from ASEAN/Oceania partners.\n")


# ===================================================================
# MAIN
# ===================================================================

def main():
    """Load data, run all 10 insights, print summary."""
    print("=" * 70)
    print("  THAILAND TRADE IMPACT ANALYSIS — EDA (10 Insights)")
    print("  DADS 5001 Mini-Project | NIDA")
    print("=" * 70)

    # --- Load data ---
    data_path = 'data/clean/thailand_trade_clean.csv'
    if not os.path.exists(data_path):
        print(f"\n[ERROR] Data file not found: {data_path}")
        print("Please run 01_data_collection.py and 02_data_cleaning.py first.")
        sys.exit(1)

    print(f"\nLoading data from {data_path} ...")
    df = pd.read_csv(data_path, low_memory=False)
    df = _safe_date(df)

    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Datasets: {df['dataset'].unique().tolist()}")
    print(f"  Date range: {df['date'].min()} — {df['date'].max()}")

    os.makedirs('outputs/figures', exist_ok=True)

    # --- Run all insights ---
    insights = [
        insight_1, insight_2, insight_3, insight_4, insight_5,
        insight_6, insight_7, insight_8, insight_9, insight_10,
    ]

    success, failed = 0, 0
    for fn in insights:
        try:
            fn(df)
            success += 1
        except Exception as e:
            failed += 1
            print(f"\n  [ERROR in {fn.__name__}] {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

    # --- Summary ---
    print("\n" + "=" * 70)
    print("  EDA SUMMARY")
    print("=" * 70)
    print(f"  Insights completed: {success}/{len(insights)}")
    if failed:
        print(f"  Insights failed:    {failed}/{len(insights)}")
    print(f"  Figures saved to:   outputs/figures/")
    print("=" * 70)


if __name__ == '__main__':
    main()
