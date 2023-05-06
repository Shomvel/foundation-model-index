import requests
import pandas as pd
import time
from tqdm import tqdm

PAGES = 264
SLEEP_INTERVAL = 1  # 1秒间隔，可以根据需要调整
OUTPUT_FILE = "futurepedia.csv"


def fetch_data(page):
    url = f"https://www.futurepedia.io/api/tools?page={page}&sort=verified"
    response = requests.get(url)
    return response.json()


def extract_data(raw_data):
    extracted_data = []
    for item in raw_data:
        categories = ' '.join([category.get('categoryName', '') for category in item.get('toolCategories', [])])
        data = {
            'date': item.get('_createdAt', ''),
            'name': item.get('toolName', ''),
            'description': item.get('toolShortDescription', ''),
            'categories': categories,
        }
        extracted_data.append(data)
    return extracted_data


def save_to_csv(data, filename=OUTPUT_FILE):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')


def main():
    final_data = []
    for page in tqdm(range(PAGES)):
        raw_data = fetch_data(page)
        extracted_data = extract_data(raw_data)
        final_data.extend(extracted_data)
        save_to_csv(final_data)
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()
