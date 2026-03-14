# sales_analyzer/analyzer.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

import pandas as pd


@dataclass
class ColumnMap:
    order_id: str = "order_id"
    customer_id: str = "customer_id"
    order_date: str = "order_date"
    product_id: str = "product_id"      # fixed
    category: str = "category"
    quantity: str = "quantity"
    total_amount: str = "total_amount"  # canonical
    region: str = "region"


class SalesAnalyzer:
    """Performs reusable sales analyses on a cleaned DataFrame."""

    def __init__(self, df: pd.DataFrame, columns: ColumnMap | None = None):
        self.df = df.copy()
        self.columns = columns or ColumnMap()
        self._ensure_date_index()

    def _ensure_date_index(self):
        col_date = self.columns.order_date
        if col_date in self.df.columns:
            self.df[col_date] = pd.to_datetime(self.df[col_date], errors="coerce")
            self.df = self.df.sort_values(col_date)

    # -------- Basic KPIs --------
    def basic_stats(self) -> Dict[str, Any]:
        c = self.columns
        df = self.df
        stats: Dict[str, Any] = {}

        if c.total_amount in df.columns:
            stats["total_sales"] = df[c.total_amount].sum()
            stats["average_order"] = df[c.total_amount].mean()  # fixed name

        if c.order_id in df.columns:
            stats["total_orders"] = df[c.order_id].nunique()
        if c.customer_id in df.columns:
            stats["unique_customers"] = df[c.customer_id].nunique()
        if c.product_id in df.columns:
            stats["unique_products"] = df[c.product_id].nunique()

        if c.order_date in df.columns:
            date_min = df[c.order_date].min()
            date_max = df[c.order_date].max()
            if pd.notna(date_min) and pd.notna(date_max):
                stats["date_range"] = {
                    "start": date_min.strftime("%Y-%m-%d"),
                    "end": date_max.strftime("%Y-%m-%d"),
                }

        return stats

    # -------- Category / product --------
    def sales_by_category(self) -> pd.DataFrame:
        c = self.columns
        if c.category not in self.df.columns or c.total_amount not in self.df.columns:
            return pd.DataFrame()

        agg = self.df.groupby(c.category).agg(
            total_sales=(c.total_amount, "sum"),
            quantity=(c.quantity, "sum"),
            order_count=(c.order_id, "nunique"),
        )
        return agg.sort_values("total_sales", ascending=False)

    def top_products(self, n: int = 10) -> pd.DataFrame:
        c = self.columns
        if c.product_id not in self.df.columns or c.total_amount not in self.df.columns:
            return pd.DataFrame()

        agg = self.df.groupby(c.product_id).agg(
            total_sales=(c.total_amount, "sum"),
            quantity=(c.quantity, "sum"),
            order_count=(c.order_id, "nunique"),
        )
        return agg.sort_values("total_sales", ascending=False).head(n)

    # -------- Time-based --------
    def monthly_trends(self) -> pd.DataFrame:
        c = self.columns
        if c.order_date not in self.df.columns or c.total_amount not in self.df.columns:
            return pd.DataFrame()

        df = self.df.copy()
        df["month_year"] = df[c.order_date].dt.to_period("M")

        monthly = df.groupby("month_year").agg(
            total_sales=(c.total_amount, "sum"),
            quantity=(c.quantity, "sum"),
            order_count=(c.order_id, "nunique"),
            unique_customers=(c.customer_id, "nunique"),
        )
        monthly["growth_rate"] = monthly["total_sales"].pct_change() * 100
        return monthly

    def average_order_value(self) -> float:
        stats = self.basic_stats()
        return float(stats.get("average_order", 0.0))

    def peak_sales_periods(self, top_n: int = 3) -> pd.DataFrame:
        monthly = self.monthly_trends()
        if monthly.empty:
            return monthly
        return monthly.sort_values("total_sales", ascending=False).head(top_n)
