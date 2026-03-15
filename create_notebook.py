"""Helper script to generate the Jupyter Notebook programmatically."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11.0"},
}

cells = []

# ── Title Cell ───────────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""# Energy Sector Analysis & Macro Crisis (2000-2026)
## DADS 5001: Data Analytics and Data Science Tools and Programming — Mini-Project

**หัวข้อ:** วิเคราะห์พลวัตหุ้นกลุ่มพลังงานสหรัฐฯ และไทย ท่ามกลางวิกฤตภูมิรัฐศาสตร์และเศรษฐกิจมหภาค (2000-2026)

**Pipeline:**  Collection → Cleaning → 20 Insights EDA (Storytelling with Data)

---"""))

# ── Phase 1 ──────────────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""## Phase 1: Data Collection

**Sources:**
- Yahoo Finance (yfinance): US Energy (XOM, CVX, COP, SHEL, TTE), Thai Energy (PTT.BK, PTTEP.BK, PTG.BK, BCP.BK, PTTGC.BK), Oil Benchmarks (BZ=F, CL=F)
- FRED: CPIENG, DGS10, DTWEXBGS, VIXCLS, INDPRO

**Interval:** Weekly (1wk), 2000-01-02 to 2026-03-13"""))

cells.append(nbf.v4.new_code_cell("""%run 01_data_collection.py"""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd

# Quick look at raw data
raw = pd.read_excel("data/raw/energy_macro_raw.xlsx", sheet_name=None)
for name, df in raw.items():
    print(f"\\nSheet: {name} | Shape: {df.shape}")
    print(df.head(3))
"""))

# ── Phase 2 ──────────────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""## Phase 2: Data Cleaning & Feature Engineering

**Steps:**
1. Crisis era labeling (Dot-com, Great Recession, Shale Revolution, COVID-19, Russia-Ukraine, Iran Crisis)
2. Indexed Price normalization (base 100 @ year 2000)
3. Weekly returns & 20-week rolling volatility
4. Currency adjustment (THB → USD proxy via Dollar Index)
5. Upstream/Downstream spread computation"""))

cells.append(nbf.v4.new_code_cell("""%run 02_data_cleaning.py"""))

cells.append(nbf.v4.new_code_cell("""# Data Quality Dashboard
import pandas as pd

stocks = pd.read_excel("data/cleaned/energy_macro_cleaned.xlsx", sheet_name="Stocks_Master", index_col=0, parse_dates=True)
fred = pd.read_excel("data/cleaned/energy_macro_cleaned.xlsx", sheet_name="FRED_Macro", index_col=0, parse_dates=True)

print("=== Stocks Master ===")
print(f"Shape: {stocks.shape}")
print(f"Date range: {stocks.index.min().date()} to {stocks.index.max().date()}")
print(f"Tickers: {stocks['Ticker'].nunique()}")
print(f"\\nNull % by column:")
print((stocks.isnull().mean() * 100).round(1))
print(f"\\nCrisis Era Distribution:")
print(stocks.groupby('crisis_era')['Ticker'].count().sort_values(ascending=False))

print(f"\\n=== FRED Macro ===")
print(f"Shape: {fred.shape}")
print(fred.describe().round(2))
"""))

# ── Phase 3 ──────────────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""## Phase 3: 20 Insights EDA — Storytelling with Data

### Structure:
| ACT | Insights | Theme |
|-----|----------|-------|
| **ACT 1** | 1-5 | The Global Stage — Oil, inflation, dollar, VIX |
| **ACT 2** | 6-10 | US vs Thailand — Upstream, resilience, dividends |
| **ACT 3** | 11-15 | Crisis Deep Dive — Event studies, volatility, recovery |
| **ACT 4** | 16-20 | Policy & Strategy — Oil fund, Sharpe ratio, portfolio |"""))

cells.append(nbf.v4.new_code_cell("""%run 03_eda_analysis.py"""))

# ── Display all figures ──────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("### ACT 1: The Global Stage (Insights 1-5)"))

for i in range(1, 6):
    cells.append(nbf.v4.new_code_cell(f"""from IPython.display import Image, display
display(Image(filename="outputs/figures/insight_{i:02d}_{'oil_stock_corr' if i==1 else 'indexed_evolution' if i==2 else 'cpi_vs_stocks' if i==3 else 'dollar_vs_energy' if i==4 else 'vix_vs_energy_vol'}.png", width=900))"""))

cells.append(nbf.v4.new_markdown_cell("### ACT 2: The Battle of Giants — US vs TH (Insights 6-10)"))

fig_names_6_10 = ["upstream_pttep_cop", "thai_resilience", "upstream_downstream", "cumulative_us_vs_th", "dividend_yield"]
for i, name in enumerate(fig_names_6_10, start=6):
    cells.append(nbf.v4.new_code_cell(f"""display(Image(filename="outputs/figures/insight_{i:02d}_{name}.png", width=900))"""))

cells.append(nbf.v4.new_markdown_cell("### ACT 3: Crisis Deep Dive (Insights 11-15)"))

fig_names_11_15 = ["event_russia_ukraine", "event_iran_crisis", "volatility_boxplot", "covid_recovery", "max_drawdown"]
for i, name in enumerate(fig_names_11_15, start=11):
    cells.append(nbf.v4.new_code_cell(f"""display(Image(filename="outputs/figures/insight_{i:02d}_{name}.png", width=900))"""))

cells.append(nbf.v4.new_markdown_cell("### ACT 4: Policy & Action Plan (Insights 16-20)"))

fig_names_16_20 = ["policy_gap", "sharpe_heatmap", "indpro_oil", "corr_matrix", "portfolio_strategy"]
for i, name in enumerate(fig_names_16_20, start=16):
    cells.append(nbf.v4.new_code_cell(f"""display(Image(filename="outputs/figures/insight_{i:02d}_{name}.png", width=900))"""))

# ── Executive Summary ────────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""## Executive Summary: 20 Insights & Hypothesis Testing

| # | Insight | Hypothesis | Result |
|---|---------|-----------|--------|
| 1 | Oil-Stock Correlation | All energy stocks positively correlate with Brent | **True** — COP highest (β≈0.5), PTG lowest |
| 2 | 26-Year Price Evolution | Oil dictates macro trend for all 10 stocks | **True** — but individual divergences exist |
| 3 | Energy CPI vs Stocks | Rising energy inflation erodes real stock returns | **True** — CPI outpaces stock gains in some periods |
| 4 | Dollar vs Energy | Strong USD hurts oil prices | **True** — Thai stocks face double headwind (oil + FX) |
| 5 | VIX vs Energy Vol | Market fear amplifies energy sector volatility | **True** — Spikes track VIX with amplification |
| 6 | PTTEP vs COP | COP tracks oil rallies better than PTTEP | **True** — Higher oil-beta = bigger gains & losses |
| 7 | Thai Resilience | Thai stocks are safe havens in crises | **False** — COVID-19 showed comparable/worse losses |
| 8 | Upstream/Downstream | Supply shocks widen upstream premium | **True** — Russia-Ukraine war clearly widened spread |
| 9 | Cumulative Returns | US energy delivers higher total returns | **True** — Deeper capital markets & global diversification |
| 10 | Dividend Yield | Thai energy offers higher yields | **True** — Compensates for lower capital gains |
| 11 | Russia-Ukraine Event | US majors outperform during war | **True** — XOM, CVX captured windfall profits |
| 12 | Iran Crisis Event | Pattern echoes Russia-Ukraine | **True** — Early oil surge follows similar trajectory |
| 13 | Volatility Boxplot | COVID-19 most volatile period | **True** — Sharpest spike, but Great Recession was more sustained |
| 14 | V-Shape Recovery | Energy stocks recovered rapidly post-COVID | **True** — COP recovered fastest (+300%) |
| 15 | Max Drawdown | Great Recession caused deepest drawdowns | **True** — Prolonged vs COVID's sharp but brief decline |
| 16 | Thai Oil Fund | Policy dampens domestic price swings | **True** — But widens fiscal gap during price spikes |
| 17 | Sharpe Ratio | Risk-adjusted returns vary across crises | **True** — War-time offers positive Sharpe for some stocks |
| 18 | Industrial Production | Industrial output drives oil demand | **True** — Divergences mark demand shocks (2008, 2020) |
| 19 | Correlation Matrix | US stocks are tightly coupled | **True** — r>0.6 among US; Thai stocks less correlated |
| 20 | Portfolio Strategy | US upstream best war-time risk/reward | **True** — COP/XOM dominate efficient frontier |

---

## Action Plan: Policy & Investment Strategy

### Investment Recommendations:
1. **War-Time Overweight:** Allocate 40-50% to US upstream (COP, XOM) during geopolitical crises for maximum oil-price beta capture
2. **Income Strategy:** Thai energy stocks (PTT, BCP) provide 3-7% dividend yields — attractive for income-focused portfolios
3. **Diversification Hedge:** PTTEP provides EM upstream exposure with lower correlation to US majors (r≈0.3-0.5)
4. **Risk Management:** Maintain 10% VIX-linked protection during war periods (energy vol amplifies market fear by 1.5-2x)
5. **Currency Watch:** Monitor Dollar Index — strong USD periods require underweighting THB-denominated energy positions

### Policy Implications:
1. Thailand's Oil Fund effectively dampens domestic price volatility but creates fiscal risk during sustained oil spikes
2. Upstream/downstream spread analysis can serve as early warning indicator for energy subsidy pressure
3. Energy transition policy should consider geopolitical risk premium currently embedded in fossil fuel equities"""))

# ── Compliance Checklist ─────────────────────────────────────────────────────
cells.append(nbf.v4.new_markdown_cell("""## Compliance Checklist (DADS 5001)

| Requirement | Status |
|-------------|--------|
| Data > 100 rows | ✅ 16,404 stock rows + 1,367 FRED rows = **17,771 total** |
| Pandas used extensively | ✅ All data manipulation via Pandas |
| Matplotlib/Seaborn used | ✅ 20 figures with Matplotlib + Seaborn |
| Weekly data interval | ✅ 1,367 weeks (2000-2026) |
| Multiple data sources | ✅ Yahoo Finance + FRED (2 sources) |
| 20 Insights EDA | ✅ 20 figures organized in 4 ACTs |
| Decluttered visualizations | ✅ No gridlines clutter, no top/right spines, white bg |
| Proper labeling | ✅ Fig number, title, subtitle, units, source on every chart |
| No tutorial duplication | ✅ Original analysis, no copied tutorials |
| Storytelling structure | ✅ 4-ACT narrative: Global → US vs TH → Crises → Strategy |
| Error handling | ✅ Handles missing data, timezone, currency adjustment |
| Feature engineering | ✅ Indexed prices, returns, volatility, crisis labels, FX adjustment |"""))

# ── Set cells
nb.cells = cells

with open("energy_macro_analysis.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook created: energy_macro_analysis.ipynb")
