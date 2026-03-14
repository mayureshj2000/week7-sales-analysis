# Sales Data Analysis Dashboard

A comprehensive sales data analysis system built with pandas that loads raw sales data, cleans and enriches it, calculates business metrics, and generates visual and textual reports. This project demonstrates practical data analysis skills for real-world business scenarios.

##Project Description

This project implements an end-to-end sales data analysis dashboard:
- Loads raw sales data from CSV (and optionally Excel).
- Cleans and validates the data.
- Computes key performance indicators (KPIs) such as total sales, average monthly sales, and top products.
- Produces visualizations (trends, breakdowns) and exportable reports.

It is designed to mimic a realistic business analytics workflow using Python and pandas.

## Learnings
Working on this project, I practiced and reinforced:

### Pandas fundamentals
- Using DataFrame and Series
- Filtering, grouping, aggregating, and joining datasets

### Data cleaning
- Handling missing values and duplicates
- Fixing data types (dates, numeric fields)
- Normalizing column names and categories

### Data analysis
- Calculating KPIs (total sales, average sales, growth)
- Identifying top products, customers, and categories
- Building time‑series summaries (monthly/weekly trends)

### Data visualization
- Creating line charts and bar charts for trends and rankings
- Customizing labels, titles, and legends for readability

### Report generation
- Exporting clean datasets and metrics to CSV/Excel
- Saving plots as image files for presentations

### Project structure & testing
- Organizing a Python project into modules
- Writing simple tests for critical logic

## Module Responsibilities
1. data_loader
- Reads raw data from:
  - data/raw/sales_data.csv
  - (Optional) Excel files if configured
- Validates required columns (e.g. date, product, quantity, price, customer).
- Converts date columns to proper datetime and ensures numeric types where needed.

2. data_cleaner
- Cleans the loaded DataFrame:
  - Removes duplicates
  - Handles missing values according to simple rules (e.g. drop or fill)
  - Normalizes column names (lowercase, underscores)
- Optionally filters out invalid rows (e.g. negative quantities or prices).
- Writes cleaned data to data/processed/.

3. analyzer
- Core analysis logic:
  - Computes total sales and revenue.
  - Calculates average monthly sales and growth rates.
  - Identifies:
      - Top product categories
      - Top N products
      - Basic customer metrics (count, repeat customers, average order value).
- Outputs a metrics dictionary / DataFrame that is used by reporter and visualizer.

4. visualizer
- Creates visualizations using matplotlib:
  - Monthly sales trend line chart.
  - Top products bar chart.
  - Category‑wise revenue chart (if available).
  - Saves figures into data/reports/ as PNG images.

5.  reporter
- Formats a textual report similar to the sample output.
- Optionally exports:
  - Metrics to CSV/Excel.
  - Cleaned data snapshot for stakeholders.
- Writes final report files into data/reports/.

6. main
- Load raw data using data_loader.
- Clean it via data_cleaner.
- Run analysis through analyzer.
- Generate charts using visualizer.
- Produce final output via reporter.
- Prints a summary to the console.

## How to Run
pip install -r requirements.txt
python main.py

## Required Libraries
- pandas - data manipulation and analysis
- numpy - numerical operations and derived metrics
- matplotlib - plotting charts and saving figures
- openpyxl - Excel file read/write support
- jupyter/databricks - interactive development via notebooks