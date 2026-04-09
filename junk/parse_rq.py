import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd

st_accept = "text/html" # говорим веб-серверу, что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

# отправляем запрос с заголовками по нужному адресу
# req = requests.get("https://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.Manufacturer.%ED%98%84%EB%8C%80.))%22%7D", headers)
# req = requests.get("https://car.encar.com/carpicture04/pic4144/41440017_017.jpg", headers)
req = requests.get("https://selectel.ru/blog/courses/", headers=headers)
# считываем текст HTML-документа
src = req.text
# print(src)

# инициализируем html-код страницы
soup = BeautifulSoup(src, 'lxml')
# считываем заголовок страницы
title = soup.title.string
print(title)
