if __name__ == '__main__':
    from linovelib_all import *
else:
    from .linovelib_all import *

def linovelib_download(id,wait_time=1,split_char='\n'):
    novel_catalog = "https://www.linovelib.com/novel/" + id + "/catalog"
    catalog_list = get_chapter_list(novel_catalog)
    book_title = get_title_book(novel_catalog)
    print("Downloading",book_title)
    write_txt = book_title + "\n\n"
    for i in catalog_list:
        try:
            print("Downloading",i[0])
            if len(i) == 1:
                write_txt += i[0] + "\n\n"
            else:
                if i[1] == None:
                    write_txt += i[0] +"\n"+ "本章获取失败" +"\n\n"
                else:
                    print("Start getting From:",i[1])
                    soup_list = get_chapter_all(i[1],wait_time)
                    chapter_text = get_text(soup_list,split_char)
                    write_txt += i[0] + "\n" + chapter_text + "\n\n"
                print(i[0],"is over.")
        except ConnectionResetError:
            print("ConnectionResetError from",i[0])
            break
        except:
            print("Error from",i[0])
    write_txt = write_txt.replace("\n\n\n","\n\n")
    write_txt_all(write_txt,book_title)
    print("Downloading",book_title,"is over.")
