import requests
import json
import os
from datetime import datetime

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD"
RAW_DIR = "data/raw"


def fetch_gdp_data():
    all_records = []
    page = 1

    while True:
        url = f"{BASE_URL}?format=json&page={page}"
        print(f"📥 Coletando página {page}")

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        metadata = data[0]
        records = data[1]

        all_records.extend(records)

        if page >= metadata["pages"]:
            break

        if page == 50:
            print("⚠️ Limite de páginas atingido (50). Parando a coleta.")
            break

        page += 1

    return all_records


def save_raw_data(data):
    os.makedirs(RAW_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"gdp_raw_{timestamp}.json"
    file_path = os.path.join(RAW_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Dados salvos em: {file_path}")


if __name__ == "__main__":
    gdp_data = fetch_gdp_data()
    print(f"Total de registros: {len(gdp_data)}")
    save_raw_data(gdp_data)
