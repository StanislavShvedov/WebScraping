import json

import bs4
import requests
from fake_headers import Headers
import re


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

response = requests.get('https://habr.com/ru/articles/',
                        headers=Headers(browser='chrom', os='mac').generate())

soup = bs4.BeautifulSoup(response.text, features='lxml')
news_list = soup.select_one('div.tm-articles-list')
items = news_list.select('div.tm-article-snippet.tm-article-snippet')

parsed_data = []

for item in items:
    link = item.select_one('a.tm-title__link')
    item_response = requests.get('https://habr.com' + link['href'])
    item_soup = bs4.BeautifulSoup(item_response.text, features='lxml')
    date = item_soup.select_one('time')['datetime']
    title = item_soup.select_one('h1').text
    text = item_soup.select_one('div.article-formatted-body').text

    for word in KEYWORDS:
        if len(re.findall(word, text)) > 1 or len(re.findall(word, title)) > 1:
            parsed_data.append({
                'date': date,
                'title': title,
                'link': 'https://habr.com' + link['href']
            })

with open('parced_habr.json', 'w') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))
