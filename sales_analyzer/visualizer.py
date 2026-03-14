# sales_analyzer/visualizer.py
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class SalesVisualizer:
    """Creates charts from analyzer outputs."""

    def __init__(self, output_dir: str | Path = "data/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_monthly_trend(self, monthly_df: pd.DataFrame, filename: str = "monthly_trend.png"):
        if monthly_df.empty:
            print("No monthly data to plot.")
            return

        plt.figure(figsize=(12, 6))
        monthly_df["total_sales"].plot(kind="line", marker="o")
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = self.output_dir / filename
        plt.savefig(path)
        plt.close()
        print(f"Saved monthly trend chart to {path}")

    def plot_category_sales(self, category_df: pd.DataFrame, top_n: int = 10,
                            filename: str = "category_sales.png"):
        if category_df.empty:
            print("No category data to plot.")
            return

        data = category_df.head(top_n)
        plt.figure(figsize=(10, 6))
        data["total_sales"].plot(kind="bar")
        plt.title(f"Top {top_n} Categories by Sales")
        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        path = self.output_dir / filename
        plt.savefig(path)
        plt.close()
        print(f"Saved category sales chart to {path}")

    def plot_order_distribution(self, df: pd.DataFrame, amount_column: str = "total_amount",
                                filename: str = "order_distribution.png"):
        if amount_column not in df.columns:
            print(f"Column '{amount_column}' not found for distribution plot.")
            return

        plt.figure(figsize=(10, 6))
        plt.hist(df[amount_column], bins=30, edgecolor="black", alpha=0.7)
        plt.title("Order Value Distribution")
        plt.xlabel("Order Value")
        plt.ylabel("Frequency")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = self.output_dir / filename
        plt.savefig(path)
        plt.close()
        print(f"Saved order distribution chart to {path}")