import pandas as pd

def load_excel(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        return pd.read_excel(file, engine="openpyxl")
    except Exception as e:
        return None
