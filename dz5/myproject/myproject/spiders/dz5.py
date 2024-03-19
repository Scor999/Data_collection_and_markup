import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Извлекаем ссылки на страницы книг
        book_links = response.css('article.product_pod h3 a::attr(href)').getall()
        for book_link in book_links:
            yield scrapy.Request(response.urljoin(book_link), callback=self.parse_book)

        # Следующая страница, если есть
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        # Извлекаем название книги
        title = response.css('h1::text').get()

        # Извлекаем цену книги
        price = response.css('p.price_color::text').get()

        # Извлекаем наличие книги
        availability_element = response.css('p.instock.availability')
        availability = availability_element.css('::text').extract()[-1].strip()
      

        # Извлекаем краткое описание книги
        description = response.css('div#product_description + p::text').get()

        yield {
            'title': title,
            'price': price,
            'availability': availability,
            'description': description
        }
