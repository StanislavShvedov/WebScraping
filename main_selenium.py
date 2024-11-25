import json
import re

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def wait_element(browser, delay=3, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located((by, value))
    )


chrome_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_path)
browser = Chrome(service=browser_service)

browser.get('https://habr.com/ru/articles/')

items = browser.find_elements(by=By.CSS_SELECTOR, value='div.tm-article-snippet.tm-article-snippet')

links = []
parsed_data = []

for item in items:
    item_link = wait_element(browser=item, by=By.CSS_SELECTOR, value='a.tm-title__link').get_attribute('href')
    links.append(item_link)

for link in links:
    browser.get(link)
    date = wait_element(browser=browser, by=By.TAG_NAME, value='time').get_attribute('datetime')
    title = wait_element(browser=browser, by=By.TAG_NAME, value='h1').text
    text = wait_element(browser=browser, by=By.CSS_SELECTOR, value='div.article-formatted-body').text

    for word in KEYWORDS:
        if len(re.findall(word, text)) > 1:
            parsed_data.append({
                'date': date,
                'title': title,
                'link': link
            })

with open('parced_habr2.json', 'w') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))
