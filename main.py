import json

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
    if case == '1':
        bookPath = input("请输入PDF文件地址：")
    elif case == '2':
        bookPath = input("请输入PDF文件地址：")
        offset = int(input("请输入偏移值："))
    elif case == '3':
        bookName = input("请输入PDF的ISBN号：")

    # 启动爬虫
    # print("crawl starting...")
    # runSpider(bookName)
    # print("crawl finished")

    # # offset值根据用户具体的PDF来确定，因此需用户自行手动输入
    # with open(bookName + '.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    # data['目录'] = process_bookmarks(data['目录'])
    # print("\n".join(data['目录'][:5]))
    # print("由于不同的PDF书签偏移值不同，请根据爬取到的目录信息，输入对应偏移值")
    # offset_user = int(input("请输入偏移值："))

    # # 添加书签
    # print("开始添加书签...")
    # add_bookmark_to_pdf(bookName + '.pdf', bookName + '_add.pdf', data['目录'], offset=offset_user)
    # print("添加完成")

    



    
