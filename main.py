import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor
from bookInfoSpider import bookInfoSpider

# 定义全局变量以便于网址信息的传递——由于scrapy无法把结果返回到程序中
book_urls = []

# 此爬虫用于获取书籍的链接
class bookLinkSpider(scrapy.spiders.Spider):
    name = "bookSpider"
    # 必要的网址前缀
    base_url = "https://www.shukui.net"
    search_url = "https://www.shukui.net/so/search.php?q="

    # 这里重载init函数使其能传入url参数
    def __init__(self, bookName=None, *args, **kwargs):
        super(bookLinkSpider, self).__init__(*args, **kwargs)
        self.start_url = self.search_url + bookName

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        res = response.xpath('//div[@class="cate-info"]/h2/a/@href')
        if len(res) > 0:
            for re in res:
                book_urls.append(self.base_url + re.get())

# 设置爬虫的settings信息，后续可以在此补充或者封装为单独文件
settings = {
    # 'LOG_LEVEL' : "ERROR",
    'REQUEST_FINGERPRINTER_IMPLEMENTATION' : "2.7",
    'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
}

# 此处获得书籍的前10本网址信息
runner = CrawlerRunner(settings=settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(bookLinkSpider, bookName='9787115279460')
    yield runner.crawl(bookInfoSpider, bookLink=book_urls)
    reactor.stop()


if __name__ == "__main__":
    # 启动爬虫
    print("crawl starting...")
    crawl()
    reactor.run()

    # 完成书签的添加
    
