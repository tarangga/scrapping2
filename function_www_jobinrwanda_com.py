# -*- coding: utf-8 -*-
"""Function - www.jobinrwanda.com

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RtjCvHOfrvWurrzLjPxKyeRc4-vBzv4X

# Import Library
"""

from requests import get, post
from bs4 import BeautifulSoup as Soup
import pandas as pd
import re
from json import loads, dumps

"""# Function"""

def get_page(url):
  try:
    html = Soup(get(url).text)
    job_url = html.find_all('small', {'class':'text-muted'})
    record = {
        'title': html.find('h5', {'class':'card-title'}).text,
        'short_description': html.find('div', {'class': 'employer-description'}).text.strip() if html.find('div', {'class': 'employer-description'}) else '',
        'rating': html.find('div', {'class': 'fivestar-summary fivestar-summary-average-count'}).text,
        'job_url': job_url[1].text.strip() if len(job_url) > 1 else '',
        'description': html.find('div', {'class':'field--name-field-job-full-description'}).text.strip()
    }
    return record
  except Exception as e:
    print(e, url)
    return {}

get_page('https://www.jobinrwanda.com/job/sales-officer-0')

url = 'https://www.jobinrwanda.com/'
html = Soup(get(url).text)
elements =html.find_all('div', {'class': 'card-body p-2'})

def get_item(element):
  employ = element.find('p', {'class':'card-text'})
  return {
    'item_url': 'https://www.jobinrwanda.com' + element.find('a')['href'],
    'item_title': element.find('a').text.strip(),
    'information': re.sub(r'[ \r\n\t]+', ' ', employ.text).strip(),
    'employe_url': 'https://www.jobinrwanda.com' + employ.a['href'],

  }

items = [get_item(el) for el in elements]

for item in items:
  item.update(get_page(item['item_url']))

df = pd.DataFrame(items)
df.to_csv('./temp_data-jobinrwanda.csv', index=False)