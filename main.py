# main.py
from pathlib import Path

from sales_analyzer import (
    DataLoader,
    DataCleaner,
    CleaningConfig,
    SalesAnalyzer,
    SalesVisualizer,
    SalesReporter,
)


def main():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    loader = DataLoader(base_dir=raw_dir)
    df = loader.load("sales_data.csv")

    # 2. Clean data
    cleaner = DataCleaner(
        CleaningConfig(
            date_columns=["order_date"],
            # numeric/category inferred if omitted
        )
    )
    df_clean = cleaner.clean(df)
    df_clean.to_csv(processed_dir / "sales_data_clean.csv", index=False)

    # 3. Analyze
    analyzer = SalesAnalyzer(df_clean)
    stats = analyzer.basic_stats()
    category_df = analyzer.sales_by_category()
    monthly_df = analyzer.monthly_trends()

    # 4. Visualize
    visualizer = SalesVisualizer(output_dir="data/reports")
    visualizer.plot_monthly_trend(monthly_df)
    visualizer.plot_category_sales(category_df)
    visualizer.plot_order_distribution(df_clean)

        # 5. Report
    reporter = SalesReporter(reports_dir="data/reports")
    reporter.save_basic_stats(stats)
    reporter.save_full_report(stats, monthly_df, category_df, df_clean)

    # NEW: pretty console/file report
    text_report = reporter.build_text_report(
        basic_stats=stats,
        category_df=category_df,
        monthly_df=monthly_df,
    )
    reporter.save_text_report(text_report, filename="sales_report.txt")

    print("\n" + text_report)

if __name__ == "__main__":
    main()
