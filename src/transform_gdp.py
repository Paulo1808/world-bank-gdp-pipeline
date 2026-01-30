import json
import pandas as pd
import os
from glob import glob
from datetime import datetime

RAW_DIR = "data/raw/world_bank"
PROCESSED_DIR = "data/processed"

def load_raw_data():
    files = glob(os.path.join(RAW_DIR, "gdp_raw_*.json"))

    if not files:
        raise FileNotFoundError("No raw data files found.")
    
    latest_file = max(files, key=os.path.getctime)
    print(f"📂 Loading data from {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def transform_data(raw_data):
    df = pd.DataFrame(raw_data)

    print("Original columns:")
    print(df.columns)

    df_transformed = pd.DataFrame(
        {
            "country_id": df["country"].apply(lambda x: x["id"] if pd.notnull(x) else None),
            "country_name": df["country"].apply(lambda x: x["value"] if pd.notnull(x) else None),
            "indicator": df["indicator"].apply(lambda x: x["value"] if pd.notnull(x) else None),
            "year": df["date"],
            "gdp_value": df["value"]
        }
    )

    df_transformed = df_transformed.dropna(subset=["gdp_value"])

    df_transformed["year"] = df_transformed["year"].astype(int)
    df_transformed["gdp_value"] = df_transformed["gdp_value"].astype(float)

    return df_transformed

def filter_countries(df):

    countries = ["BR", "US", "CN", "IN", "DE"]

    df_filtered = df[df["country_id"].isin(countries)]

    return df_filtered


def save_processed_data(df):
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(PROCESSED_DIR, f"gdp_processed_{timestamp}.csv")

    df.to_csv(file_path, index=False)

    print(f"✅ Dados processados salvos em: {file_path}")


if __name__ == "__main__":
    raw_data = load_raw_data()
    df_transformed = transform_data(raw_data)
    df_final = filter_countries(df_transformed)

    print(f"📊 Registros finais: {len(df_final)}")
    print(df_final.head())

    save_processed_data(df_final)