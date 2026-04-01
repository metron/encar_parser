import json
import os
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from mark_translates import MARK_TRANSLATES

LIMIT = 10000
DB_FILE = "database.json"

service = Service('/usr/bin/chromedriver')
browser = webdriver.Chrome(service=service)
browser.get("https://car.encar.com/list/car?page=1")

# скролим страницу вниз
for i in range(100):
    browser.execute_script("window.scrollBy(0, 500);")
    time.sleep(0.3)

soup = BeautifulSoup(browser.page_source, 'html.parser')

# 1. Найти все элементы с классом, начинающимся с "ItemBigImage_item__"
item_elements = soup.find_all(class_=re.compile(r'^ItemBigImage_item__'))

Path("images").mkdir(exist_ok=True)
cars = {}
if os.path.isfile(DB_FILE):
    with open(DB_FILE, "r") as f:
        cars = json.load(f)
i = 0
marks = set()

# 2. Внутри каждого элемента найти <img>
for item in item_elements:
    images = item.find_all('img')
    img_src = images[0].attrs["src"].split("?")[0]
    filename = img_src.split("/")[-1]
    id_ = filename.split("_")[0]
    try:
        response = requests.get(img_src, timeout=30)
        # time.sleep(1)
        response.raise_for_status()  # Проверка на ошибки HTTP
        with open(f"""images/{filename}""", 'wb') as f:
            f.write(response.content)
    except RequestException as e:
        print(f"Ошибка при загрузке файла: {img_src}")
        continue

    # марка, модель, год, пробег, цена, фото
    mark = str(item.find(class_=re.compile(r'^ItemBigImage_name__')).contents[0]).strip()
    marks.add(mark)
    cars[id_] = {
        "mark": MARK_TRANSLATES.get(mark, mark),
        "year": 2000 + int(item.find(class_=re.compile(r'^ItemBigImage_info__')).select("li")[0].contents[0][:2]),
        "mileage": item.find(class_=re.compile(r'^ItemBigImage_info__')).select("li")[1].contents[0][:-2],
        "price": item.find(class_=re.compile(r'^ItemBigImage_price__')).select("span")[0].contents[0],
        "img": filename
    }
    i += 1
    print(i)
    if i == LIMIT:
        break

with open(DB_FILE, "w") as f:
    json.dump(cars, f)

print("Марки требующие перевода")
res = "; ".join(marks - MARK_TRANSLATES.keys())
with open("kor_marks.txt", "w") as f:
    f.write(res)
print(res)
