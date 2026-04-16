# Парсинг корейского сайта продажи машин и лендинг для резултатов парсинга
## Стек
Парсинг: selenium + beautifulsoup4  
Лендинг: FastAPI + Jinja2 + pydantic  

## Установите виртуальное окружение и зависимости
python3.11 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

## Запустите парсер сайта encar.com
python parse_encar.py

## Запустите веб-сервер для лендинга
python main.py
## Рабочий лендинг
http://82.24.19.94:8000/
(FastAPI + Jinja2)
