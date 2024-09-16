import numpy as np
import pandas as pd
import json
import requests
import os

base_url = 'https://www.federalregister.gov/api/v1/documents'

# Query Params
params = {
    'per_page': 100,
    'page': 1,
    'type': 'executive_order',
    'order': 'newest'
}

download_dir = 'executive_orders'

if not os.path.exists(download_dir):
    os.makedirs(download_dir)


def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    
    else:
        print(f'Failed to download {url}')


while True:
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'results' not in data or not data['results']:
        break

    for document in data['results']:
        title = document['title']
        pdf_url = document.get('pdf_url')
        if pdf_url:
            filename = os.path.join(download_dir, f'{title}.pdf')
            download_file(pdf_url, filename)
            print(f'Downloaded: {title}')
    
    params['page'] += 1
