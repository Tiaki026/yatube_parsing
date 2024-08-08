import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        all_group = response.css('a.group_link::attr(href)')
        for group_link in all_group:
            yield response.follow(group_link, callback=self.parse_group)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        for quote in response.css('div.card'):
            yield {
                'group_name': quote.css('div.card-body h2::text').get().strip(),
                'description': quote.css('p.group_descr::text').get().strip(),
                'posts_count': int(
                    quote.css('div.h6.text-muted.posts_count::text')
                    .get()
                    .strip()
                    .replace('Записей: ', '')
                )
            }


# with open('groups.csv', encoding='utf-8') as file:
#     content = file.read()
#     print(len(content))
