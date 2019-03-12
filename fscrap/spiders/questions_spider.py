import scrapy


class QuestionsScrapy(scrapy.Spider):
    name = 'questions'  # name must be unique within the project
    iter = 0
    count = 0

    # optional shortcut without start_request and  parse() is Scrapy’s default callback
    # start_urls = [
    #     'https://stackoverflow.com/questions?page=2&sort=newest',
    #     'https://stackoverflow.com/questions?page=3&sort=newest',
    # ]

    def start_requests(self):
        urls = [
            'https://stackoverflow.com/questions?page=2&sort=newest',
            'https://stackoverflow.com/questions?page=3&sort=newest',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     self.iter = self.iter+1
    #     filename = "questions-{}.html".format(self.iter)
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file {}'.format(filename))

    def parse(self, response):
        for question in response.xpath('//div[@class="question-summary"]'):
            vote_div = question.xpath('.//*/div[@class="vote"]')
            votes = vote_div.xpath('.//*/span[@class="vote-count-post "]/strong/text()').extract_first()
            ans = question.xpath('.//*/div[contains(concat(" ", normalize-space(@class), " "), " status unanswered ")]/strong/text()').extract_first()
            summary = question.xpath('.//div[@class="summary"]/h3')
            link = summary.xpath('.//a/@href').extract_first()
            q= summary.xpath('.//a/text()').extract_first()
            tag_div = question.xpath('.//*/div[contains(@class,"tags")]')
            tags = []
            for a in tag_div.xpath('.//a[@class="post-tag"]/text()'):
                tags.append(a.extract())

            yield {
                'votes': votes,
                'answer_count': ans,
                'link': link,
                'question': q,
                'tags': tags
                }

        link = response.xpath('.//*/div[contains(@class,"pager")]/a[@rel="next"]/@href').extract_first()
        if self.count < 10:
            # next_page_url = response.urljoin(link)
            self.count = self.count + 1
            # yield scrapy.Request(url=next_page_url, callback=self.parse)

            # Unlike scrapy.Request, response.follow supports relative URLs directly - no need to call urljoin.
            # Note that response.follow just returns a Request instance; you still have to yield this Request.
            yield response.follow(link, callback=self.parse)



# data=[]
# for q in q_div:
#     vote_div = q.xpath('.//div[@class="statscontainer"]/div[@class="stats"]/div[@class="vote"]')
#     votes = vote_div.xpath('.//div[@class="votes"]/span[@class="vote-count-post "]/strong/text()').extract_first()
#     ans = q.xpath('.//div[@class="statscontainer"]/div[@class="stats"]/div[contains(concat(" ", normalize-space(@class), " "), " status unanswered ")]/strong/text()').extract_first()
#     summary = q.xpath('.//div[@class="summary"]/h3')
#     link = summary.xpath('.//a/@href').extract_first()
#     question = summary.xpath('.//a/text()').extract_first()
#     tag_div = q.xpath('.//div[@class="summary"]/div[contains(@class,"tags")]')
#     tags = []
#     for a in tag_div.xpath('.//a[@class="post-tag"]/text()'):
#         tags.append(a.extract())
#     data.append({'question': question, 'tags': tags, 'link': link, 'ans_count': ans, 'votes': votes})


