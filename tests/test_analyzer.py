# tests/test_analyzer.py
import pandas as pd
import pytest
from sales_analyzer.analyzer import SalesAnalyzer, ColumnMap


def _sample_df():
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "customer_id": [10, 10, 11, 12],
            "product_id": ["A", "B", "A", "C"],
            "category": ["Electronics", "Books", "Electronics", "Books"],
            "order_date": [
                "2024-01-01",
                "2024-01-15",
                "2024-02-01",
                "2024-02-10",
            ],
            "quantity": [1, 2, 1, 3],
            "total_amount": [100.0, 50.0, 150.0, 75.0],
        }
    )


def test_basic_stats():
    df = _sample_df()
    analyzer = SalesAnalyzer(df, ColumnMap())
    stats = analyzer.basic_stats()

    assert stats["total_sales"] == 375.0
    assert stats["total_orders"] == 4
    assert stats["unique_customers"] == 3
    assert stats["unique_products"] == 3
    assert stats["date_range"]["start"] == "2024-01-01"
    assert stats["date_range"]["end"] == "2024-02-10"


def test_sales_by_category():
    df = _sample_df()
    analyzer = SalesAnalyzer(df)
    cat_df = analyzer.sales_by_category()

    assert "Electronics" in cat_df.index
    assert "Books" in cat_df.index
    assert cat_df.loc["Electronics", "total_sales"] == 250.0
    assert cat_df.loc["Books", "total_sales"] == 125.0


def test_monthly_trends_has_growth_rate():
    df = _sample_df()
    analyzer = SalesAnalyzer(df)
    monthly = analyzer.monthly_trends()

    # Two months: 2024-01, 2024-02
    assert len(monthly) == 2
    assert "growth_rate" in monthly.columns
    # First month growth_rate should be NaN, second should be numeric
    assert monthly["growth_rate"].iloc[1] == pytest.approx(
        (225.0 - 150.0) / 150.0 * 100
    )
