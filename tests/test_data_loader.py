# tests/test_data_loader.py
from pathlib import Path

import pandas as pd

from sales_analyzer.data_loader import DataLoader


def test_load_csv(tmp_path: Path):
    base_dir = tmp_path / "raw"
    base_dir.mkdir()
    csv_path = base_dir / "sales_data.csv"

    # Create fake CSV
    csv_path.write_text("order_id,total_amount\n1,100.0\n2,200.0\n", encoding="utf-8")

    loader = DataLoader(base_dir=base_dir)
    df = loader.load("sales_data.csv")

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert df["total_amount"].sum() == 300.0
