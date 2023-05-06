import pandas as pd
import json
import requests
import logging
from time import sleep
from tqdm import tqdm
from datetime import datetime

from pinyin import is_capitalized_pinyin

logging.basicConfig(
    handlers=[
        logging.FileHandler("output.log"),
        logging.StreamHandler()
    ],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def is_within_date_range(date_str, start_date, end_date):
    date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return start_date <= date_obj <= end_date


def version_to_time(record):
    for version in record['versions']:
        if version['version'] == 'v1':
            return version['created']
    return None


def is_within_categories(categories):
    return any(x in categories for x in ['cs.AI', 'cs.CV', 'cs.LG'])


def is_chinese_authors_by_name(author_info, threshold=0.8):
    chinese_count = 0
    all_authors = len(author_info)
    for author in author_info:
        author = [word for word in author if word]
        is_all_pinyin = all(is_capitalized_pinyin(word) for word in author)
        if is_all_pinyin:
            chinese_count += 1

    ratio = chinese_count / all_authors
    return ratio >= threshold


def read_and_filter_jsonl(file_path):
    data = []
    start_date = datetime(2022, 12, 1)
    end_date = datetime(2023, 5, 5)

    with open(file_path, 'r') as file:
        for line in tqdm(file, desc="Processing JSONL file"):
            record = json.loads(line)
            categories = record.get('categories')

            if not is_within_categories(categories):
                continue

            v1_created = version_to_time(record)
            if not v1_created:
                continue

            if not is_within_date_range(v1_created, start_date, end_date):
                continue

            is_chinese = is_chinese_authors_by_name(record['authors_parsed'])

            data.append({
                'title': record['title'],
                'authors': record['authors'],
                'abstract': record['abstract'],
                'time': v1_created,
                'doi': record['doi'],
                'is_chinese': is_chinese
            })
    df = pd.DataFrame.from_records(data)

    return df


def add_chinese_author_info(df):
    def get_author_info(doi):
        try:
            url = f'https://api.crossref.org/works/{doi}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                author_data = data['message'].get('author', [])
                return author_data
            else:
                logging.warning(f'Could not get author info for DOI: {doi}, status code: {response.status_code}')
        except Exception as e:
            logging.error(f'Error getting author info for DOI: {doi}, error: {str(e)}')
        return None

    def is_chinese_author(author_info):
        if author_info:
            for author in author_info:
                if 'affiliation' in author:
                    for affiliation in author['affiliation']:
                        if 'name' in affiliation and 'China' in affiliation['name']:
                            return True
        return False

    def get_chinese_author(row):
        doi = row['doi']
        is_chinese = row['is_chinese']
        if not doi:
            return is_chinese

        if not is_chinese:
            return False

        author_info = get_author_info(doi)
        sleep(0.25)  # To avoid too many requests in a short time, 4req/s is recommended rate
        return is_chinese_author(author_info)

    for index, row in tqdm(df.iterrows()):
        try:
            row['is_chinese'] = get_chinese_author(row)
        except Exception as e:
            pass

        if index % 50 == 0:
            df.to_csv('filtered_arxiv.csv')

    return df


if __name__ == '__main__':
    file_path = 'arxiv-metadata-oai-snapshot.json'
    logging.info('Start filtering and converting')
    df = read_and_filter_jsonl(file_path)
    logging.info('Finish filtering and converting')
    logging.info('Start adding is Chinese column')
    df = add_chinese_author_info(df)
    logging.info('Finish adding is Chinese column')
    df.to_csv('./data/filtered_arxiv_data.csv', index=False)
