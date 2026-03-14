# tests/test_data_cleaner.py
import numpy as np
import pandas as pd

from sales_analyzer.data_cleaner import DataCleaner, CleaningConfig


def test_cleaner_drops_duplicates_and_fills_missing():
    df = pd.DataFrame(
        {
            "order_id": [1, 1, 2],
            "order_date": ["2024-01-01", "2024-01-01", "2024-01-02"],
            "total_amount": [100.0, 100.0, np.nan],
            "category": ["Electronics", None, "Books"],
        }
    )

    config = CleaningConfig(date_columns=["order_date"])
    cleaner = DataCleaner(config)
    cleaned = cleaner.clean(df)

    # duplicates removed -> 2 rows
    assert len(cleaned) == 2

    # no missing values
    assert cleaned.isna().sum().sum() == 0

    # order_date converted to datetime
    assert np.issubdtype(cleaned["order_date"].dtype, np.datetime64)
