import pandas as pd

class DataCleaner:
    """
    Cleans raw data before validation / storage.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def drop_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self.df

    def fill_missing(self, strategy="mean"):
        """
        Fills missing values.
        - numeric columns: mean
        - non-numeric: 'unknown'
        """

        for col in self.df.columns:
            if self.df[col].dtype in ["int64", "float64"]:
                if strategy == "mean":
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
            else:
                self.df[col] = self.df[col].fillna("unknown")

        return self.df

    def standardize_columns(self):
        self.df.columns = [col.strip().lower().replace(" ", "_") for col in self.df.columns]
        return self.df

    def run_all(self):
        self.drop_duplicates()
        self.standardize_columns()
        self.fill_missing()
        return self.df
