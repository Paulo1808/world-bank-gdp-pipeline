from pkgutil import get_data
import requests
import json
import os
from datetime import datetime

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD"
RAW_DIR = "data/raw/world_bank"


def fetch_gdp_data():

    all_records = []
    page = 1

    while True:
        
        if page == 244:
            print("⚠️ Pulando página 244 devido a problemas desconhecidos.")
            page += 1
            continue

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

def save_log(total_records):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "extract_log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: Total de registros extraídos: {total_records}\n")

if __name__ == "__main__":
   gdp_data = fetch_gdp_data()
   print(f"Total de registros: {len(gdp_data)}")
   save_raw_data(gdp_data)
   save_log(len(gdp_data))


