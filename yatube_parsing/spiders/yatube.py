import scrapy
from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        for quote in response.css('div.card-body'):
            # Для каждой найденной цитаты создаём и возвращаем словарь:
            data = {
                'author': quote.css('strong::text').get(),
                'text': ' '.join(
                    t.strip() for t in quote.css('p::text').getall()
                ).strip(),
                'date': quote.css('small.text-muted::text').get(),
            }
            yield YatubeParsingItem(data)
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            # Если ссылка нашлась, загружаем страницу по ссылке
            # и вызываем метод parse() ещё раз.
            yield response.follow(next_page, callback=self.parse)
