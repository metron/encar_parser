import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


service = Service('/usr/bin/chromedriver')
browser = webdriver.Chrome(service=service)
browser.get("https://selectel.ru/blog/")

# регистрируем кнопку "Поиск" и имитируем нажатие
open_search = browser.find_element(By.CLASS_NAME, 'header__btn-search')
# open_search = browser.find_element_by_class_name("header_search")
open_search.click()
# регистрируем текстовое поле и имитируем ввод строки "Git"
search = browser.find_element(By.CLASS_NAME, 'search-modal_input')
# search = browser.find_element_by_class_name("search-modal_input")
search.send_keys("Git")

# ставим на паузу, чтобы страница прогрузилась
time.sleep(3)
# загружаем страницу и извлекаем ссылки через атрибут rel
soup = BeautifulSoup(browser.page_source, 'lxml')
all_publications = \
   soup.find_all('a', {'rel': 'noreferrer noopener'})[1:5]
# форматируем результат
for article in all_publications:
   print(article['href'])
