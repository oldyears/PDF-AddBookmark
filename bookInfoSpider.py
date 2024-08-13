import scrapy
import json

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
        book_data['目录'] = bookContents
        print("书籍目录获取完成")

        # 以json格式存储
        json_data = json.dumps(book_data, ensure_ascii=False, indent=4)
        with open(bookName + '.json', 'w', encoding='utf-8') as f:
            f.write(json_data)
        print("文件写入完成")

        

        
        


        
        