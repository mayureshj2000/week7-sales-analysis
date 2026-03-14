# sales_analyzer/data_cleaner.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import pandas as pd


@dataclass
class CleaningConfig:
    date_columns: List[str] = field(default_factory=lambda: ["order_date"])
    numeric_columns: List[str] = field(default_factory=list)
    category_columns: List[str] = field(default_factory=list)
    drop_duplicates: bool = True
    fill_missing_numeric: bool = True
    fill_missing_categorical: bool = True


class DataCleaner:
    """Applies generic cleaning rules to a sales DataFrame."""

    def __init__(self, config: Optional[CleaningConfig] = None):
        self.config = config or CleaningConfig()

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Convert date columns
        for col in self.config.date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        # Detect numeric/category columns if not explicitly provided
        if not self.config.numeric_columns:
            self.config.numeric_columns = list(
                df.select_dtypes(include=[np.number]).columns
            )
        if not self.config.category_columns:
            self.config.category_columns = list(
                df.select_dtypes(exclude=[np.number]).columns
            )

        # Drop duplicates
        if self.config.drop_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            print(f"Removed {before - len(df)} duplicate rows")

        # Handle missing values
        missing = df.isna().sum()
        if missing.sum() > 0:
            print("Missing values found:")
            print(missing[missing > 0])

        # Fill numeric columns
        if self.config.fill_missing_numeric:
            for col in self.config.numeric_columns:
                if col in df.columns and df[col].isna().any():
                    median = df[col].median()
                    df[col] = df[col].fillna(median)

        # Fill categorical columns
        if self.config.fill_missing_categorical:
            for col in self.config.category_columns:
                if col in df.columns and df[col].isna().any():
                    mode = df[col].mode(dropna=True)
                    if not mode.empty:
                        df[col] = df[col].fillna(mode[0])

        return df