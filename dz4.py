import requests
from lxml import html
import csv

url = 'https://news.mail.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        
        # Находим заголовки новостей в таблице на главной странице
        news_titles = tree.xpath('//div[contains(@class, "js-module")]//span[contains(@class, "newsitem__title")]/text()')
        
        # Создаем CSV-файл для сохранения заголовков новостей
        with open('news_titles.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Записываем заголовки новостей в CSV-файл
            for title in news_titles:
                writer.writerow([title.strip()])
        
        print("Заголовки новостей успешно извлечены и сохранены в файл 'news_titles.csv'")
    else:
        print("Не удалось получить доступ к странице. Код состояния:", response.status_code)
except Exception as e:
    print("Произошла ошибка:", e)
