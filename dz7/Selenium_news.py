import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# URL сайта
url = "https://lenta.ru/"

# Устанавливаем сервис и создаем экземпляр веб-драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Открываем главную страницу
driver.get(url)

# Используем BeautifulSoup для парсинга HTML-кода
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Извлекаем заголовки и ссылки на новости
data = []
titles = soup.find_all("h3", class_="card-mini__title")
for title in titles:
    title_text = title.text.strip()
    link = url + title.find_parent("a")['href']
    data.append([title_text, link])

# Закрываем веб-драйвер
driver.quit()

# Сохраняем данные в CSV файл
with open('lenta_news.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Заголовок', 'Ссылка'])
    writer.writerows(data)

print("Данные успешно сохранены в файл lenta_news.csv")
