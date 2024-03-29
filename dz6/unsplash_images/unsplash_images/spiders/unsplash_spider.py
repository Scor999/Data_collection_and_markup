import csv
import os
import requests
import scrapy
from unsplash_images.items import UnsplashImageItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    
    def start_requests(self):
        category = input("Введите категорию, которую нужно искать: ")
        start_url = f"https://unsplash.com/s/photos/{category}"
        yield scrapy.Request(start_url, callback=self.parse, meta={'category': category})
    
    def parse(self, response):
        category = response.meta['category']
        photo_links = response.css('a[itemprop="contentUrl"]::attr(href)').extract()
        for link in photo_links:
            yield response.follow(link, callback=self.parse_photo, meta={'category': category})

    def parse_photo(self, response: HtmlResponse):
        loader = ItemLoader(item=UnsplashImageItem(), response=response)
        loader.add_value('url', response.url)

        photos = response.xpath('//button//img/@srcset').extract()
        if photos:
            loader.add_value('photos', photos)

        name = response.xpath('//h1/text()').extract_first()
        if name:
            loader.add_value('name', name.strip())

        description = response.xpath('//p[@style]/text()').extract_first()
        if description:
            loader.add_value('description', description.strip())

        date = response.xpath('//time/@datetime').extract_first()
        if date:
            loader.add_value('date', date.strip())

        yield loader.load_item()

        # Сохранение данных в CSV файл
        csv_data = [{
            'name': loader.get_output_value('name'),
            'description': loader.get_output_value('description'),
            'date': loader.get_output_value('date'),
            'url': loader.get_output_value('url'),
            'photos': loader.get_output_value('photos')
        }]
        save_to_csv(csv_data, 'data.csv')

        # Загрузка изображений
        download_images(csv_data, 'images')

# Функция для сохранения данных в CSV файл
def save_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'description', 'date', 'url', 'photos']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for item in data:
            writer.writerow(item)

# Функция для загрузки изображений по ссылкам
def download_images(data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for item in data:
        photos = item['photos']
        for idx, photo_url in enumerate(photos):
            response = requests.get(photo_url)
            if response.status_code == 200:
                with open(os.path.join(output_folder, f"{item['name'][0]}_{idx}.jpg"), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {item['name'][0]}_{idx}.jpg")
            else:
                print(f"Failed to download {photo_url}")
