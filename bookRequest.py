import requests
import json
import time
from bs4 import BeautifulSoup
from addBookmark import process_bookmarks

# 计时
start_time = time.time()

# 此文件用于重构爬虫，使用requests而非scrapy
search_url = "https://www.shukui.net/so/search.php?q="
# ISBN = input("请输入ISBN：")
ISBN = "9787115279460" # 测试用例
result = requests.get(search_url + ISBN)

# 若请求成功则解析网页得到书籍链接
book_link = ''
if result.status_code == 200:
    # 使用BeautifulSoup解析网页
    soup = BeautifulSoup(result.text, 'html.parser')

    # 从其中提取所需网页链接
    book_link = soup.find('div', {'class': 'cate-info'}).find('a').get('href')
    book_link = "https://www.shukui.net" + book_link
    # print(book_link)

# 使用书籍链接获取书籍信息
result2 = requests.get(book_link)

requests_end_time = time.time()
print(f"request请求时间：{requests_end_time - start_time}秒")

if result2.status_code == 200:
    # 使用BeautifulSoup解析网页
    result2.encoding = 'utf-8'
    soup2 = BeautifulSoup(result2.text, 'html.parser')

    # 作者和书籍名进行特判
    bookInfo = {}
    book_lis = soup2.find('div', {'class': 'b-info'}).find_all('li')

    bookInfo['书名'] = soup2.find('h1', {'class': 'book-name'}).text.replace('pdf电子书版本下载', '')
    bookInfo['作者'] = book_lis[0].text

    for li in book_lis[1:]:
        attribute = li.text.split('：')[0].strip()
        value = li.text.split('：')[1].strip()
        bookInfo[attribute] = value
    
    # print('\n'.join([f'{key}: {value}' for key, value in bookInfo.items()]))

    # 获取书籍目录
    contents_ps = soup2.find('div', {'id': 'book-contents'}).find_all('p')
    book_contents = [p.text.replace('\t', ' ') for p in contents_ps]
    bookInfo['目录'] = process_bookmarks(book_contents)

    # 将此书籍信息存储为json文件
    with open(bookInfo["书名"] + '.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(bookInfo, ensure_ascii=False, indent=4))
    
    print('书籍信息存储完成')

end_time = time.time()
print(f"程序运行时间：{end_time - start_time}秒")