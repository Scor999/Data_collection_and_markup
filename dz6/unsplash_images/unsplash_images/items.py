# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy

class UnsplashImageItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    download_link = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()  # Добавленное поле 'url'
    photos = scrapy.Field()
