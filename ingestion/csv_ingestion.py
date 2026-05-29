import pandas as pd
import os

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully!")
        print("Shape:", df.shape)
        print("Columns:", df.columns.tolist())
        print(df.head())
        return df
    except Exception as e:
        print("Error loading CSV:", e)
        return None


if __name__ == "__main__":
    file_path = "/mnt/c/Users/Abhishek Pandey/Desktop/pollution_us_2000_2016.csv"

    if not os.path.exists(file_path):
        print("File not found at:", file_path)
    else:
        load_csv(file_path)
