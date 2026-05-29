import pandas as pd

class DataValidator:
    """
    Basic data validation for ingestion layer.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def check_empty(self):
        if self.df is None or self.df.empty:
            raise ValueError("DataFrame is empty")
        return True

    def check_nulls(self, threshold=0.5):
        """
        Fails if too many null values exist.
        threshold = max allowed % of nulls
        """
        null_ratio = self.df.isnull().mean()

        if any(null_ratio > threshold):
            raise ValueError(f"Too many nulls found:\n{null_ratio}")

        return True

    def check_columns(self, required_columns):
        missing = [col for col in required_columns if col not in self.df.columns]

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        return True

    def run_all(self, required_columns=None):
        self.check_empty()

        if required_columns:
            self.check_columns(required_columns)

        self.check_nulls()

        return True
