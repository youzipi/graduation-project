import scrapy


class EsiSpider(scrapy.Spider):
    name = "esi"
    allowed_domains = [""]
    start_urls = []

    def parse(self, response):
        pass
