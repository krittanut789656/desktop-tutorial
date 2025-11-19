# Excel Export Guide

## Overview

The ETF Backtester now includes Excel export functionality to easily export real market data from the database to Excel files for analysis, reporting, or sharing.

## Installation

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

This will install `openpyxl` and `pandas` needed for Excel export.

## Usage

### Option 1: Using the Main CLI

Run the main application:

```bash
python main.py
```

Navigate to **[4] Reports & Export** section:

- **4.3** - Export ETF_Master to Excel
- **4.4** - Export Price_Data to Excel
- **4.5** - Export All Tables to Excel

### Option 2: Using the Standalone Script

Run the export utility directly:

```bash
python export_to_excel.py
```

Then choose from the menu:
1. ETF_Master table only
2. Price_Data table only
3. Both tables

## Exported Files

All Excel files are saved to the `data/` directory with timestamps:

- `ETF_Master_YYYYMMDD_HHMMSS.xlsx`
- `Price_Data_YYYYMMDD_HHMMSS.xlsx`

## File Contents

### ETF_Master Excel File

**Sheet 1: ETF_Master**
- All 50 ETF records with complete information
- Columns: ETF_ID, Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date

**Sheet 2: Summary**
- Total number of ETFs
- Export timestamp
- Data source (Yahoo Finance)

**Sheet 3: Asset_Type_Breakdown**
- Count of ETFs by asset type
- Shows distribution across Equity, Bond, Commodity, Mixed

### Price_Data Excel File

**Sheet 1: Price_Data**
- All weekly price records (up to 26,000+ rows)
- Columns: Price_ID, Ticker_Symbol, ETF_Name, Asset_Type, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume
- Sorted by date (most recent first) and ticker

**Sheet 2: Summary**
- Total records count
- Date range (start/end dates)
- Number of weeks covered
- Number of ETFs
- Data frequency (Weekly)
- Data source and export timestamp

**Sheet 3: ETF_Statistics**
- Per-ETF statistics summary
- Columns: Ticker_Symbol, Asset_Type, Num_Records, First_Date, Last_Date, Min_Price, Max_Price, Avg_Price, Avg_Volume

## Important Notes

### Large Datasets

The Price_Data table can contain **26,000+ records**. When exporting:

1. **Full Export**: Exports all data (may take 30-60 seconds)
2. **Limited Export**: Option to limit rows (e.g., 1000 rows) for faster export
3. **File Size**: Full export creates ~5-10 MB Excel file

### Performance Tips

- For quick previews, use limited export (1000-5000 rows)
- For full analysis, export all data once and reuse
- Excel can handle up to 1 million rows, so 26,000 rows is well within limits

## Example Usage

### Export All Data

```bash
python main.py
# Choose option 4.5 to export all tables
```

This creates:
- `data/ETF_Master_20250119_120000.xlsx` (50 rows)
- `data/Price_Data_20250119_120000.xlsx` (26,000+ rows)

### Export Individual Tables

```bash
python main.py
# Choose option 4.3 for ETF_Master only
# OR
# Choose option 4.4 for Price_Data only
```

This exports only the selected table to Excel.

## Data Analysis in Excel

Once exported, you can:

1. **Filter by Asset Type**: Use Excel filters to analyze specific asset classes
2. **Create Charts**: Visualize price trends for individual ETFs
3. **Pivot Tables**: Analyze performance across different dimensions
4. **Calculate Returns**: Use formulas to compute returns
5. **Export to Other Tools**: Import into R, Python notebooks, or BI tools

## Sample Queries

After exporting, you can answer questions like:

- Which ETF had the highest average price?
- What's the price volatility for each asset type?
- How many weeks of data do we have per ETF?
- What's the total trading volume across all ETFs?

## Troubleshooting

### Missing Dependencies

If you see an error about missing packages:

```bash
pip install pandas openpyxl
```

### Large File Warning

If Excel warns about large file size:
- This is normal for 26,000+ rows
- Modern Excel handles this easily
- Consider exporting to CSV if needed

### Memory Issues

If export fails due to memory:
- Use limited export (smaller row count)
- Close other applications
- Export tables separately (6.1 then 6.2)

## File Locations

- **Export Directory**: `etf_backtester/data/`
- **ETF Master**: Contains 50 ETF definitions
- **Price Data**: Contains 10 years of weekly market data

## Next Steps

After exporting to Excel, you can:

1. Share data with team members
2. Create presentations with charts
3. Perform custom analysis
4. Archive historical data
5. Import into other analysis tools

---

**Note**: The exported Excel files contain real market data downloaded from Yahoo Finance. This data is suitable for academic analysis and backtesting purposes.
