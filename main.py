import json
import addBookmark

from bookSpider import runSpider
from addBookmark import process_bookmarks, add_bookmark_to_pdf


# 脚本启动说明文字
startNotes = '''此脚本主要处理以下情况：
1. PDF本身自带书签文件，但是其存在格式错位，此时需要用户输入PDF文件地址
2. PDF本身自带书签文件，但是其存在对应错误，此时需要用户输入错位偏移量-offset
3. PDF本身不带书签文件，此时需要用户输入PDF的ISBN号（输入书名会返回多个版本结果，而ISBN对于书籍的特定版本是唯一的）
'''


if __name__ == "__main__":
    # 启动脚本，给出说明
    print(startNotes)
    case = input("请输入你需要处理的情况：")
    # 第一种情况需读取书签后改格式
    bookPath = ''
    bookmarks = []
    offset = 0

    if case == '1':
        bookPath = input("请输入PDF文件地址：")
        bookmarks = addBookmark.extract_bookmarks(bookPath)
        bookmarks = addBookmark.process_bookmarks(bookmarks)
    elif case == '2':
        bookPath = input("请输入PDF文件地址：")
        offset = int(input("请输入偏移值："))
        bookmarks = addBookmark.extract_bookmarks(bookPath)
    elif case == '3':
        bookName = input("请输入PDF的ISBN号：")
        # 启动爬虫
        print("crawl starting...")
        runSpider(bookName)
        print("crawl finished")

        print("书籍信息以json文件形式存储，如有需要自行查看")

        # 要求用户检查书签页数对应是否正确，如果不正确，需输入偏移值
        print("请检查json文件中书签对应页数是否正确，若不则输入偏移值（正确为0）:")
        offset = int(input("请输入偏移值："))
        bookPath = input("请输入PDF文件地址：")
        with open(bookName + '.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            bookmarks = data['目录']

    addBookmark.add_bookmark_to_pdf(bookPath, bookPath, bookmarks, offset)
    print("处理完成")

    



    
