# Energy Sector Analysis & Macro Crisis (2000-2026)

**DADS 5001: Data Analytics and Data Science Tools and Programming — Mini-Project**

วิเคราะห์พลวัตหุ้นกลุ่มพลังงานสหรัฐฯ และไทย ท่ามกลางวิกฤตภูมิรัฐศาสตร์และเศรษฐกิจมหภาค (2000-2026)

## Project Overview

End-to-End data pipeline analyzing 10 energy stocks (5 US + 5 Thai) across 26 years of geopolitical crises, with 20 EDA insights structured as a 4-ACT data story.

### Data Sources
| Source | Data | Frequency |
|--------|------|-----------|
| Yahoo Finance | XOM, CVX, COP, SHEL, TTE, PTT.BK, PTTEP.BK, PTG.BK, BCP.BK, PTTGC.BK, BZ=F, CL=F | Weekly |
| FRED | CPIENG, DGS10, DTWEXBGS, VIXCLS, INDPRO | Weekly (resampled) |

### Pipeline
```
01_data_collection.py  →  data/raw/energy_macro_raw.xlsx
02_data_cleaning.py    →  data/cleaned/energy_macro_cleaned.xlsx
03_eda_analysis.py     →  outputs/figures/ (20 PNG charts)
energy_macro_analysis.ipynb  →  Full notebook with results
```

## 20 Insights (4-ACT Structure)

| ACT | Insights | Theme |
|-----|----------|-------|
| **ACT 1: The Global Stage** | 1-5 | Oil correlation, indexed prices, inflation, dollar effect, VIX |
| **ACT 2: US vs Thailand** | 6-10 | Upstream battle, crisis resilience, dividends, cumulative returns |
| **ACT 3: Crisis Deep Dive** | 11-15 | Russia-Ukraine event study, Iran 2025, volatility, COVID recovery |
| **ACT 4: Policy & Strategy** | 16-20 | Oil fund gap, Sharpe ratios, industrial production, portfolio allocation |

## Key Findings

1. **COP has highest oil-beta** among all 10 stocks — best for oil-price momentum plays
2. **Thai stocks are NOT safe havens** during crises — COVID-19 showed comparable/worse losses
3. **COVID-19 produced the sharpest volatility** spike, but Great Recession was more sustained
4. **Thailand's Oil Fund** effectively dampens domestic prices but creates fiscal risk
5. **War-time portfolio:** Overweight US upstream (COP, XOM) for best risk-adjusted returns

## How to Run

```bash
pip install yfinance pandas-datareader openpyxl matplotlib seaborn scipy xlsxwriter nbformat

python 01_data_collection.py   # Phase 1: Collect data
python 02_data_cleaning.py     # Phase 2: Clean & engineer features
python 03_eda_analysis.py      # Phase 3: Generate 20 insight charts
```

Or run the complete notebook:
```bash
jupyter notebook energy_macro_analysis.ipynb
```

## Project Structure
```
.
├── 01_data_collection.py          # Phase 1: Multi-source data collection
├── 02_data_cleaning.py            # Phase 2: Cleaning & feature engineering
├── 03_eda_analysis.py             # Phase 3: 20 Insights EDA
├── create_notebook.py             # Notebook generator
├── energy_macro_analysis.ipynb    # Complete Jupyter Notebook
├── data/
│   ├── raw/                       # Raw data (Excel)
│   └── cleaned/                   # Cleaned data with engineered features
├── outputs/
│   └── figures/                   # 20 PNG charts (150 DPI, no transparency)
└── README.md
```

## Visualization Standards
- Decluttered: no unnecessary gridlines, no top/right spines, white background
- Labeled: Figure number, title (So What), subtitle (units/timeframe), source
- Color-coded: Red = crisis, Green = beneficiary, Blue = US, Orange = Thai
- No transparency: all PNGs saved with `transparent=False` for dark mode compatibility

## Data Summary
- **17,771** total data points (16,404 stock + 1,367 FRED)
- **1,367** weeks of weekly data (Jan 2000 — Mar 2026)
- **12** tickers (5 US + 5 Thai + 2 oil benchmarks)
- **5** macro indicators from FRED
