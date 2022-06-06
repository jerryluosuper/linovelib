
from linovelib_all import *
def linovelib_pic(id,wait_time=1,path=os.getcwd(),begin_chapter=0,end_chapter=0):
    novel_catalog = "https://www.linovelib.com/novel/" + id + "/catalog"
    catalog_list = get_chapter_list(novel_catalog)
    book_title = get_title_book(novel_catalog)
    if begin_chapter >= end_chapter:
        range_time = [0,len(catalog_list)]
    else:
        range_time = [begin_chapter,end_chapter]
        book_title = book_title + " " +str(begin_chapter) + "-" + str(end_chapter)
    print("Downloading",book_title,"'s pictures...")
    chapter_now = ""
    dir_now = path + "/" +book_title + "/"
    os.makedirs(dir_now,exist_ok=True)
    for i in range(range_time[0],range_time[1]):
        if len(catalog_list[i]) == 1:
            chapter_now = catalog_list[i][0]
            dir_now = path + "/" +book_title + "/" + chapter_now
            os.makedirs(dir_now,exist_ok=True)
            pass
        else:
            if catalog_list[i][0] == "插图":
                os.chdir(dir_now)
                print("Start getting picture from:",catalog_list[i][1])
                try:
                    get_chapter_pic(catalog_list[i][1],wait_time)
                except ConnectionResetError:
                    break
                except:
                    pass
    print("Downloading",book_title,"'s picture is over.")

linovelib_pic("8",1,path=os.getcwd(),begin_chapter=30,end_chapter=50)