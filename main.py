import scrapy
import argparse
import json

from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor
from bookInfoSpider import bookInfoSpider
from addBookmark import process_bookmarks, add_bookmark_to_pdf

# 定义全局变量以便于网址信息的传递——由于scrapy无法把结果返回到程序中
bookName = ''
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
    yield runner.crawl(bookLinkSpider, bookName=bookName)
    yield runner.crawl(bookInfoSpider, bookLink=book_urls)
    reactor.stop()

# 命令行参数初始化
def parse_init():
    parser = argparse.ArgumentParser(description="PDF bookmark crawling and adding")

    parser.add_argument('-b', "--bookName", help="the bookName you want to crawl", metavar='')
    parser.add_argument("-i", "--ISBN", help="the ISBN of the book you want to crawl", metavar='')
    parser.add_argument("-o", "--output", help="the output bookInfo file path, default = bookName.json", metavar='')
    # parser.add_argument("--offset", metavar='', type=int, default=0,
    #                     help="the offset of the bookmark corresponds to page number, default = 0")
    return parser

# 验证参数正确性
def parse_check(args):
    # 书名和ISBN不能同时输入
    if args.bookName and args.ISBN:
        raise Exception("Error: you can only choose one of -b/--bookName and -i/--ISBN")

    # # 书签偏移量应为int类型，否则报错(初始化时规定后则默认检测类型)
    # if type(args.offset) != int:
    #     raise TypeError("Error: the offset must be an integer")


if __name__ == "__main__":
    # 参数解析
    parser = parse_init()
    args = parser.parse_args()

    # 参数验证
    try:
        parse_check(args)
    except Exception as e:
        print(e)
        exit(1)
    
    bookName = args.ISBN if args.ISBN else args.bookName
    # offset = args.offset if args.offset else 0
    output = args.output if args.output else ''

    # 启动爬虫
    print("crawl starting...")
    crawl()
    reactor.run()

    # offset值根据用户具体的PDF来确定，因此需用户自行手动输入
    with open(bookName + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['目录'] = process_bookmarks(data['目录'])
    print("\n".join(data['目录'][:5]))
    print("由于不同的PDF书签偏移值不同，请根据爬取到的目录信息，输入对应偏移值")
    offset_user = int(input("请输入偏移值："))

    # 添加书签
    print("开始添加书签...")
    add_bookmark_to_pdf(bookName + '.pdf', bookName + '_add.pdf', data['目录'], offset=offset_user)
    print("添加完成")

    



    
