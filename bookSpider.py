import scrapy
import json

from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor
from addBookmark import process_bookmarks

# 此爬虫用于获取具体的书籍信息
class bookInfoSpider(scrapy.spiders.Spider):
    name = "bookInfoSpider"
    # 必要的网址前缀
    base_url = "https://www.shukui.net"

    # 重载init函数使其能使用网址信息
    def __init__(self, bookLink=None, *args, **kwargs):
        super(bookInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls = bookLink

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        book_data = {}
        
        # 获取书籍名称并去除不必要文字
        tmp = response.xpath('//*[@id="main"]/div[1]/h1/text()')
        bookName = tmp.get() if len(tmp) > 0 else ''
        bookName = bookName.replace('pdf电子书版本下载', '')
        book_data['书名'] = bookName
        print("书名获取完成")

        # 获取书籍相关信息
        tmp = response.xpath('//*[@id="main"]/div[1]/div[2]/div[2]/ul/li/text()')
        bookInfo = []
        bookInfo.extend(tmp.getall() if len(tmp) > 0 else [])
        # 处理其信息为字典格式方便json存储
        book_data['作者'] = bookInfo[0]
        for info in bookInfo:
            index = info.find('：')
            if index != -1:
                book_data[info[:index].strip()] = info[index + 1:].strip()
        print("书籍信息获取完成")

        # 获取书籍目录
        tmp = response.xpath('//*[@id="book-contents"]/p/text()')
        bookContents = []
        if len(tmp) > 0:
            for re in tmp:
                bookContents.append(re.get().replace('\t', ' '))
        # 处理目录为标准格式
        book_data['目录'] = process_bookmarks(bookContents)
        print("书籍目录获取完成")

        # 以json格式存储
        json_data = json.dumps(book_data, ensure_ascii=False, indent=4)
        with open(bookName + '.json', 'w', encoding='utf-8') as f:
            f.write(json_data)
        print("文件写入完成")

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

# 爬虫启动器
runner = CrawlerRunner(settings=settings)

# 设定爬虫入口函数，使其能按顺序执行
@defer.inlineCallbacks
def crawl(bookName):
    yield runner.crawl(bookLinkSpider, bookName=bookName)
    yield runner.crawl(bookInfoSpider, bookLink=book_urls)
    reactor.stop()

# 启动爬虫
def runSpider(bookName):
    crawl(bookName)
    reactor.run()



        
        


        
        