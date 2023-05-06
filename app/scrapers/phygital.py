import requests
import pandas as pd
import time
import json

URL = "https://library.phygital.plus/v1/datasource/airtable/fbfc865c-2f96-4d3b-af6c-8d2a9ee541a2/b7eed368-8057-4d43" \
      "-bd29-81ae695d30da/a940ce25-ee5c-4e8e-9eea-8912f2ce38c3/79f3ddc3-d1f1-47a4-9d7f-cdffc1575078/data"
OUTPUT_FILE = "phygital.csv"
SLEEP_INTERVAL = 1


def fetch_data(offset):
    payload = {
        "filterCriteria": {},
        "options": {"cellFormat": "string", "timeZone": "Asia/Shanghai", "userLocale": "en-US"},
        "pageContext": None,
        "pagingOption": {"offset": offset, "count": 51},
        "sortingOption": {"sortingField": "Для агрегатора: modifiied time", "sortType": "DESC"},
    }

    response = requests.post(URL, json=payload)
    print(response)
    if response.status_code != 200:
        return None
    return response.json()


def extract_data(raw_data):
    extracted_data = []
    if raw_data is not None:
        for record in raw_data.get("records", []):
            fields = record.get("fields", {})
            data = {
                "description": fields.get("Description", ""),
                "name": fields.get("Как бы вы назвали карточку", ""),
                "date": record.get("createdTime", ""),
            }
            extracted_data.append(data)
    return extracted_data


def save_to_csv(data, filename=OUTPUT_FILE):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")


def main():
    final_data = []
    offset = None
    start = time.time()
    while True:
        raw_data = fetch_data(offset)
        if raw_data is None:
            break

        extracted_data = extract_data(raw_data)
        final_data.extend(extracted_data)
        save_to_csv(final_data)

        offset = raw_data.get("offset")
        time.sleep(SLEEP_INTERVAL)
        loop_end = time.time()
        print(f'Collected {len(final_data)} items, used {loop_end - start}s')


if __name__ == "__main__":
    main()
