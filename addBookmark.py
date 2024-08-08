import pikepdf
import json
from PyPDF2 import PdfReader, PdfWriter


def add_bookmark_to_pdf(input_pdf_path, output_pdf_path, bookmarks, offset=0):
    # 打开原始PDF文件
    with pikepdf.open(input_pdf_path) as pdf:
        # 初始化PDF Writer
        writer = PdfWriter()

        # 读取所有页面
        reader = PdfReader(input_pdf_path)
        for page in reader.pages:
            writer.add_page(page)
        
        # 添加书签
        bookmark_hierarchy = {}
        for bookmark in bookmarks:
            add_bookmark(writer, bookmark, bookmark_hierarchy, offset)
        
        # 将书签添加到原始PDF文件
        with open(output_pdf_path, 'wb') as output:
            writer.write(output)
        
def add_bookmark(writer, bookmark, bookmark_hierarchy, offset=0):
    # 书签格式为缩进+编号+标题+页码
    parts = bookmark.rsplit(" ", 1)
    if len(parts) != 2:
        return 
    
    title_page = parts
    title = parts[0].strip()
    page_number = int(parts[1].strip()) - 1 + offset

    # 计算层级，通过之前处理过的缩进数量决定
    level = bookmark.count('    ')
    # level = bookmark.count('.')

    # 获取当前层级的父级书签
    parent = bookmark_hierarchy.get(level - 1)

    # 添加书签到PDF
    new_bookmark = writer.add_outline_item(title, page_number, parent=parent)

    # 更新当前层级的书签
    bookmark_hierarchy[level] = new_bookmark


def process_bookmarks(bookmarks):
    result = []

    for bookmark in bookmarks:
        # 提取章节编号和标题
        parts = bookmark.split("  ", 1)
        if len(parts) < 2:
            continue # 无标题或无编号

        number, title_with_page = parts
        title_parts = title_with_page.split(" ", 1)
        if len(title_parts) != 2:
            continue # 无页码
            
        title, page = title_parts

        # 计算层级
        level = number.count(".")
        if level > 0:
            # 将每个级别缩进4个空格
            indent = ' ' * (level * 4)
        else:
            indent = ''
        
        # 格式化书签
        formatted = f'{indent}{number} {title} {page}'
        result.append(formatted)
    
    return result

if __name__ == '__main__':
    # data = {}
    # with open('C++ Primer Plus  第6版  中文版.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    # data['目录'] = process_bookmarks(data['目录'])
    # with open('C++ Primer Plus  第6版  中文版.json', 'w', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False, indent=4)
    
    print('书签文件处理完成')
