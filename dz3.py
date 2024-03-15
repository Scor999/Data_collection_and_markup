import requests
from bs4 import BeautifulSoup
import json
import re  # Добавляем импорт модуля re


# Функция для получения информации о книгах из категории
def scrape_books_in_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []

    for book in soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'):
        title = book.h3.a['title']
        price_text = book.find('p', class_='price_color').text
        price = float(re.search(r'\d+\.\d+', price_text).group())  # Извлекаем число из строки цены
        availability_tag = book.find('p', class_='instock availability')
        availability = int(re.search(r'\d+', availability_tag.text).group()) if availability_tag and re.search(r'\d+', availability_tag.text) else 0
        description = book.p.get('title', '')  # Если нет атрибута 'title', устанавливаем пустую строку
        books.append({
            'title': title,
            'price': price,
            'availability': availability,
            'description': description
        })

    return books

# Функция для получения всех категорий на сайте
def scrape_all_categories(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    categories = soup.find('ul', class_='nav-list').find('ul').find_all('a')
    all_books = {}

    for category in categories:
        category_name = category.text.strip()
        category_url = base_url + category['href']
        all_books[category_name] = scrape_books_in_category(category_url)

    return all_books

# URL сайта для скрапинга
base_url = 'http://books.toscrape.com/'

# Получение информации о всех категориях и книгах
all_books = scrape_all_categories(base_url)

# Подключение к MongoDB
client = pymongo.MongoClient('localhost', 27017)
db = client['books_database']  # Создаем базу данных
collection = db['books_collection']  # Создаем коллекцию для хранения книг

# Вставляем данные в коллекцию
collection.insert_one(all_books)

print("Данные успешно сохранены в MongoDB")
