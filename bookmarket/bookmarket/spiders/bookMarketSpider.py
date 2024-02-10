import scrapy


class bookMarketSpider(scrapy.spiders.Spider):
    name = "bookSpider"

    def parse(self, response):
        filename = "../"
