import os
import requests
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def search_venues(category, city, limit):
    # Заголовки запроса к API
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv("Authorization")
    }

    # Параметры запроса к API
    params = {
        'near': city,
        'query': category,
        'limit': limit  # Максимальное количество результатов
    }

    # URL для запроса к API
    url = "https://api.foursquare.com/v3/places/search"

    # Выполнение запроса к API
    response = requests.get(url, headers=headers, params=params)
    # print(response)
    data = response.json()
    # print(data)

    # Обработка результатов запроса
    if 'results' in data:
        venues = data['results']
        for venue in venues:
            name = venue['name']
            address = venue['location']['formatted_address'] if 'formatted_address' in venue[
                'location'] else 'Адрес не указан'
            rating = venue.get('rating', 'Рейтинг не доступен')
            print(f"Название: {name}, Адрес: {address}, Рейтинг: {rating}")
    else:
        print("По вашему запросу ничего не найдено.")


if __name__ == '__main__':
    city = input("Введите название города: ")
    category = input("Введите категорию заведений: ")
    limit = input("Введите max количество ответов:")
    search_venues(category, city, limit)
