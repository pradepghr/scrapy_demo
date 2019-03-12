import scrapy


class ArticleScrapy(scrapy.Spider):
    name = 'article'
    count = 0
    articles = []

    def start_requests(self):
        urls = [
            'https://www.nytimes.com/section/science/space',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        latest = response.xpath('.//*/section[@id="latest-panel"]')
        data_total_pages = latest.xpath('.//div[@class="stream"]/@data-total-pages').extract_first()
        ol = latest.css('.story-menu.theme-stream.initial-set')
        lists = ol.xpath('.//li')
        per_page = round(int(data_total_pages)/len(lists))
        for item in lists:
            link = item.xpath('.//*/a[@class="story-link"]/@href').extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        article = response.xpath('.//article[@id="story"]')
        # title = article.xpath('.//header/h1/span[1]/text()').extract_first()
        # OR
        title = response.xpath('//*[@id="story"]/header/h1/span[1]/text()').extract_first()
        #author = article.xpath('.//*[@class="css-1baulvz"]/text()').extract_first()
        #date = article.xpath('.//*/header/div[contains(concat(" ", normalize-space(@class), " "), " status unanswered ")]')
        #story = article.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " css-18sbwfn StoryBodyCompanionColumn ")]')
        yield {'title':title,}
