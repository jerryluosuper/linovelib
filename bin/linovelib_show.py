from linovelib_all import *

def linovelib_show(id):
    novel_catalog = "https://www.linovelib.com/novel/" + id + "/catalog"
    catalog_list = get_chapter_list(novel_catalog)
    book_title = get_title_book(novel_catalog)
    print("书名：",book_title)
    for i in catalog_list:
        if len(i) == 1:
            print(i[0]+":\n")
        else:
            print(i[0],":",i[1])

linovelib_show("2457")
