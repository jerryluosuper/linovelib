from linovelib_all import *

def linovelib_download(id,wait_time=1,split_char='\n',path=os.getcwd,type='txt',enable_pic_download=True):
    novel_catalog = "https://www.linovelib.com/novel/" + id + "/catalog"
    catalog_list = get_chapter_list(novel_catalog)
    book_title = get_title_book(novel_catalog)
    print("Downloading",book_title)
    write_txt = ""
    if type == 'txt':
        write_txt = book_title + "\n\n"
    elif type == 'md':
        write_txt = "# " + book_title + "\n\n"
    
    chapter_now = ""
    dir_now = path
    for i in catalog_list:
        print("Downloading",i[0])
        if len(i) == 1:
            dir_now = path + "/" +book_title + "/" + chapter_now
            os.makedirs(dir_now,exist_ok=True)
            if type == 'txt':
                write_txt += i[0] + "\n\n"
            elif type == 'md':
                write_txt += "## " + i[0] + "\n\n"
        else:
            if i[1] == None:
                write_txt += i[0] +"\n"+ "本章获取失败" +"\n\n"
            elif i[0] == "插图":
                if enable_pic_download:
                    write_txt += "### " + i[0] + "\n\n"
                    os.chdir(dir_now)
                    print("Start getting picture from:",i[1])
                    try:
                        pic_list = get_chapter_pic(i[1],wait_time,enable_pic_download)
                    except ConnectionResetError:
                        break
                    except:
                        pass
                    if type == 'txt':
                        for j in pic_list:
                            write_txt += j + "\n\n"
                    elif type == 'md':
                        for j in pic_list:
                            write_txt += "![](" + dir_now + "/"+j.split('/')[-1] + ")" + "\n"
                else:
                    if type == 'md':
                        try:
                            pic_list = get_chapter_pic(i[1],wait_time,enable_pic_download)
                        except ConnectionResetError:
                            break
                        except:
                            pass
                        for j in pic_list:
                            write_txt +=  j + "\n"
            else:
                print("Start getting from:",i[1])
                try:
                    soup_list = get_chapter_all(i[1],wait_time)
                except ConnectionResetError:
                    break
                except:
                    pass
                chapter_text = get_text(soup_list,split_char)
                if type == 'txt':
                    write_txt += i[0] + "\n\n" + chapter_text + "\n\n"
                elif type == 'md':
                    write_txt += "### " + i[0] + "\n\n" + chapter_text + "\n\n"
            print(i[0],"is over.")
        
    if type == 'txt':
        pass
    elif type == 'md':
        if enable_pic_download:
            pic_url_re = re.compile(r'https://img.linovelib.com/(.*?)/(.*?)/(.*?)/(.*?).jpg')
            pic_url_list = pic_url_re.findall(write_txt)
            pic_real_list = []
            for i in pic_url_list:
                pic_real = "![](" + dir_now + "/" + i.split('/')[-1] + ")" + "\n"
                pic_real_list.append(pic_real)
            for i in range(len(pic_url_list)):
                write_txt = write_txt.replace(pic_url_list[i],pic_real_list[i])
        else:
            write_txt = write_txt.replace("https:","![](https:").replace(".jpg",".jpg)")
    
    if split_char == "\n\n":
        write_txt = write_txt.replace("\n\n\n","\n\n")
    elif split_char == "\n":
        write_txt = write_txt.replace("\n\n","\n")
    os.chdir(path)

    write_txt_all(write_txt,book_title,path,type)
    print(book_title,"is over.")
    print("Downloading",book_title,"is over.")

linovelib_download("3224",1,"\n",os.getcwd(),"md",True)
