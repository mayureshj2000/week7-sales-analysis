# tests/test_visualizer_reporter.py
from pathlib import Path

import pandas as pd

from sales_analyzer.visualizer import SalesVisualizer
from sales_analyzer.reporter import SalesReporter


def test_visualizer_creates_files(tmp_path: Path):
    visualizer = SalesVisualizer(output_dir=tmp_path)

    monthly = pd.DataFrame({"total_sales": [100.0, 150.0]}, index=["2024-01", "2024-02"])
    visualizer.plot_monthly_trend(monthly, filename="trend.png")

    assert (tmp_path / "trend.png").exists()


def test_reporter_writes_summary_and_excel(tmp_path: Path):
    reporter = SalesReporter(reports_dir=tmp_path)

    stats = {"total_sales": 1000.0, "total_orders": 10}
    monthly = pd.DataFrame({"total_sales": [100.0]}, index=["2024-01"])
    category = pd.DataFrame({"total_sales": [100.0]}, index=["Electronics"])
    raw = pd.DataFrame({"order_id": [1], "total_amount": [100.0]})

    reporter.save_basic_stats(stats, filename="summary.csv")
    assert (tmp_path / "summary.csv").exists()

    ok = reporter.save_full_report(stats, monthly, category, raw, filename="report.xlsx")
    assert ok
    assert (tmp_path / "report.xlsx").exists()