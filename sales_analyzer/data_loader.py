from pathlib import Path
from typing import Optional
import pandas as pd

class DataLoader:
    """Loads sales data from CSV/Excel/JSON into pandas DF"""

    def __init__(self, base_dir: str | Path = "data/raw"):
        self.base_dir = Path(base_dir)

    def load(self, filename: str, file_type: Optional[str] = None) -> pd.DataFrame:
        """load a dataset from raw data direcotry
        file_type=csv, excel, json or None (detect from extenction)
        """
        path = self.base_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if file_type is None:
            ext = path.suffix.lower()
            if ext == ".csv":
                file_type = "csv"
            elif ext == ".xlsx":
                file_type = "excel"
            elif ext == ".json":
                file_type = "json"
            else:
                raise ValueError(f"Unsupported file extension: {ext}")

        if file_type == "csv":
            df = pd.read_csv(path)
        elif file_type == "excel":
            df = pd.read_excel(path)
        elif file_type == "json":
            df = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        print(f"Loaded data from {path} with shape {df.shape}")
        return df