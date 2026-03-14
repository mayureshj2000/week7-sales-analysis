from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional
import json
import pandas as pd


@dataclass
class SalesReporter:
    reports_dir: Path

    def __init__(self, reports_dir: str | Path = "data/reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def save_basic_stats(self, stats: Dict[str, Any], filename: str = "basic_stats.json") -> Path:
        path = self.reports_dir / filename
        with path.open("w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, default=str)
        return path

    def save_dataframe(self, df: pd.DataFrame, filename: str) -> Path:
        path = self.reports_dir / filename
        df.to_csv(path, index=False)
        return path

    # ---------- NEW: build + save pretty text report ----------

    def build_text_report(
        self,
        basic_stats: Dict[str, Any],
        category_df: Optional[pd.DataFrame] = None,
        monthly_df: Optional[pd.DataFrame] = None,
    ) -> str:
        # Analysis period
        dr = basic_stats.get("date_range", {})
        start = dr.get("start", "N/A")
        end = dr.get("end", "N/A")

        total_sales = basic_stats.get("total_sales", 0.0)
        total_orders = basic_stats.get("total_orders", 0)
        avg_order = basic_stats.get("average_order", 0.0)
        unique_customers = basic_stats.get("unique_customers", 0)
        unique_products = basic_stats.get("unique_products", 0)

        lines: list[str] = []
        lines.append("SALES DATA ANALYSIS REPORT")
        lines.append("===============================")
        lines.append("")
        lines.append(f"Analysis Period: {start} - {end}")
        lines.append("")
        lines.append("BASIC STATISTICS:")
        lines.append(f"- Total Sales: ${total_sales:,.2f}")
        lines.append(f"- Total Orders: {total_orders:,}")
        lines.append(f"- Average Order Value: ${avg_order:,.2f}")
        lines.append(f"- Unique Customers: {unique_customers:,}")
        lines.append(f"- Unique Products: {unique_products:,}")
        lines.append("")

        # Top categories
        if category_df is not None and not category_df.empty:
            cats = category_df.sort_values("total_sales", ascending=False)
            total_cat_sales = cats["total_sales"].sum()
            lines.append("TOP PRODUCT CATEGORIES:")
            for i, (cat, row) in enumerate(cats.head(5).iterrows(), start=1):
                amount = row["total_sales"]
                pct = (amount / total_cat_sales * 100) if total_cat_sales else 0.0
                lines.append(f"{i}. {cat}: ${amount:,.0f} ({pct:.1f}%)")
            lines.append("")

        # Monthly trends
        if monthly_df is not None and not monthly_df.empty:
            m = monthly_df.copy()
            m = m.sort_index()
            amounts = m["total_sales"]

            highest_month = amounts.idxmax()
            highest_val = amounts.max()
            lowest_month = amounts.idxmin()
            lowest_val = amounts.min()
            avg_monthly = amounts.mean()

            growth = m["growth_rate"].dropna()
            best_growth_month = None
            best_growth_rate = None
            if not growth.empty:
                best_growth_month = growth.idxmax()
                best_growth_rate = growth.max()

            lines.append("MONTHLY TRENDS:")
            lines.append(f"- Highest Sales Month: {highest_month} (${highest_val:,.0f})")
            lines.append(f"- Lowest Sales Month: {lowest_month} (${lowest_val:,.0f})")
            lines.append(f"- Average Monthly Sales: ${avg_monthly:,.2f}")
            if best_growth_month is not None:
                lines.append(
                    f"- Best Growth Month: {best_growth_month} ({best_growth_rate:+.1f}%)"
                )
            lines.append("")

        # You can compute real customer insights later; for now this is placeholder
        lines.append("CUSTOMER INSIGHTS:")
        lines.append("- Repeat Customers: N/A")
        lines.append("- Average Customer Value: N/A")
        lines.append("- Top 10% Customers Generate: N/A of revenue")
        lines.append("")

        lines.append("RECOMMENDATIONS:")
        lines.append("1. Focus marketing on top-performing categories")
        lines.append("2. Improve customer retention programs")
        lines.append("3. Consider seasonal promotions in Q4")
        lines.append("4. Expand product range in high-performing categories")
        lines.append(" ")

        return "\n".join(lines)

    def save_text_report(self, content: str, filename: str = "sales_report.txt") -> Path:
        path = self.reports_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

    # in sales_analyzer/reporter.py, inside SalesReporter

    def save_full_report(
        self,
        basic_stats: Dict[str, Any],
        monthly_df: pd.DataFrame | None = None,
        category_df: pd.DataFrame | None = None,
        full_df: pd.DataFrame | None = None,
        prefix: str = "sales",
    ) -> Dict[str, Path]:
        """Save JSON + CSV artifacts and return their paths."""
        outputs: Dict[str, Path] = {}

        # 1) basic stats as JSON
        outputs["basic_stats"] = self.save_basic_stats(
            basic_stats, filename=f"{prefix}_basic_stats.json"
        )

        # 2) monthly trends CSV
        if monthly_df is not None and not monthly_df.empty:
            outputs["monthly_trends"] = self.save_dataframe(
                monthly_df, filename=f"{prefix}_monthly_trends.csv"
            )

        # 3) category sales CSV
        if category_df is not None and not category_df.empty:
            outputs["category_sales"] = self.save_dataframe(
                category_df, filename=f"{prefix}_category_sales.csv"
            )

        # 4) full cleaned data CSV (optional)
        if full_df is not None and not full_df.empty:
            outputs["full_data"] = self.save_dataframe(
                full_df, filename=f"{prefix}_data_clean.csv"
            )

        return outputs