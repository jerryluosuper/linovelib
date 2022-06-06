import os
import random
import re
import time

import pypandoc

import fake_useragent
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

def get_title_chapter(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    title = soup.select_one("#mlfy_main_text > h1")
    return title.text

def get_chapter_one_chapter(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    soup_text = soup.findAll('div', class_="read-content")
    print("Getting from:",web)
    return soup_text

def get_chapter_all(web,sleep_time=1):
    try:
        soup_list = [ ]
        soup_list.append(get_chapter_one_chapter(web))
        web_original = web[0:(len(web)-5)]
        text_original_all = soup_list[0][0].get_text()
        text_original = text_original_all[0:5]
        i=2
        while True:
            time.sleep(sleep_time)
            web = web_original + '_' + str(i) + '.html'
            chapter_now = get_chapter_one_chapter(web)
            if len(chapter_now) == 0 or chapter_now[0].get_text() == "\n\n":
                # print("Error: No chapter now")
                break
            try:
                if chapter_now[0].get_text()[0:5] == text_original:
                    # print("Error: Chapter now is the same as the last one")
                    break
            except:
                if chapter_now[0].get_text() == text_original_all:
                    # print("Error: Chapter now is the same as the last one")
                    break
            soup_list.append(chapter_now)
            i += 1
        # print(soup_list)
    except ConnectionResetError:
        print("ConnectionResetError from")
    except:
        print("Error from")
    return soup_list

def get_text(soup_list,separator_now):
    text=''
    img_re = re.compile(r'src="(.*?)"')
    text_re = re.compile(r'<p>(.*?)</p>')
    for i in soup_list:
        if len(i) != 0:
            text_list = str(i[0]).split("\n")
            for j in text_list:
                # print(j)
                if j.find("img") != -1:
                    text += img_re.findall(j)[0] + "\n" +separator_now
                elif j.find("<br/>") != -1:
                    text += "\n"
                elif j.find("div") != -1:
                    pass
                else:
                    text += text_re.findall(j)[0] + "\n" +separator_now
    text = text.replace('（本章未完）', '')
    return text

def write_txt_all(text,title,path='./',type='txt'):
    f = open(path + "/" + title +'.' + type,'w',encoding="utf-8")
    f.write(text)
    f.close()

def get_chapter_all_txt(web,wait_time=0.5,split_char='\n',path='./'):
    soup_list = get_chapter_all(web,wait_time)
    title = get_title_chapter(web)
    text = get_text(soup_list,split_char)
    write_txt_all(text,title,path)

def get_title_book(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    title = soup.select_one("html body div.wrap div.container div.book-meta h1")
    return title.text

def get_chapter_list(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")

    chapter = soup.find_all("li",class_="col-4")
    re_href = re.compile(r'<a href="(.*?)">')
    chapter_list = []
    for i in chapter:
        chapter_link = re_href.findall(str(i))[0]
        if chapter_link == "javascript:cid(0)":
            chapter_link_real = None
        else:
            chapter_link_real = "https://www.linovelib.com" + chapter_link
        chapter_list.append([i.text,chapter_link_real])

    chapter_real = soup.find("ul",class_="chapter-list clearfix").text
    chapter_list_real = chapter_real.split("\n")

    chapter_list_i = 0
    chapter_list_fix = []
    for i in chapter_list_real:
        if i == '':
            pass
        elif i == chapter_list[chapter_list_i][0]:
            chapter_list_fix.append(chapter_list[chapter_list_i])
            chapter_list_i += 1
        else:
            chapter_list_fix.append([i])
    return chapter_list_fix

def linovelib_download(id,wait_time=1,split_char='\n',path=os.getcwd(),type='txt',enable_pic_download=True,begin_chapter=0,end_chapter=0):
    novel_catalog = "https://www.linovelib.com/novel/" + id + "/catalog"
    catalog_list = get_chapter_list(novel_catalog)
    book_title = get_title_book(novel_catalog)
    if begin_chapter >= end_chapter:
        range_time = [0,len(catalog_list)]
    else:
        range_time = [begin_chapter,end_chapter]
        book_title = book_title + " " + str(begin_chapter) + "-" + str(end_chapter)
    print("Downloading",book_title)
    write_txt = ""
    if type == 'txt':
        write_txt = book_title + "\n\n"
    elif type == 'md':
        write_txt = "# " + book_title + "\n\n"
    dir_now = path + "/" +book_title + "/"
    os.makedirs(dir_now,exist_ok=True)
    for i in range(range_time[0],range_time[1]):
        print("Downloading",catalog_list[i][0])
        if len(catalog_list[i]) == 1:
            if type == 'txt':
                write_txt += catalog_list[i][0] + "\n\n"
            elif type == 'md':
                write_txt += "## " + catalog_list[i][0] + "\n\n"
        else:
            if catalog_list[i][1] == None:
                write_txt += catalog_list[i][0] +"\n"+ "本章获取失败" +"\n\n"
            elif catalog_list[i][0] == "插图":
                if enable_pic_download:
                    write_txt += "### " + catalog_list[i][0] + "\n\n"
                    os.chdir(dir_now)
                    print("Start getting picture from:",catalog_list[i][1])
                    try:
                        pic_list = get_chapter_pic(catalog_list[i][1],wait_time,enable_pic_download)
                    except ConnectionResetError:
                        break
                    except:
                        pic_list = []
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
                            pic_list = get_chapter_pic(catalog_list[i][1],wait_time,enable_pic_download)
                        except ConnectionResetError:
                            break
                        except:
                            pic_list = []
                            pass
                        for j in pic_list:
                            write_txt +=  j + "\n"
            else:
                print("Start getting from:",catalog_list[i][1])
                try:
                    soup_list = get_chapter_all(catalog_list[i][1],wait_time)
                except ConnectionResetError:
                    break
                except:
                    soup_list = []
                    pass
                chapter_text = get_text(soup_list,split_char)
                if type == 'txt':
                    write_txt += catalog_list[i][0] + "\n\n" + chapter_text + "\n\n"
                elif type == 'md':
                    write_txt += "### " + catalog_list[i][0] + "\n\n" + chapter_text + "\n\n"
            print(catalog_list[i][0],"is over.")
        
    if type == 'txt':
        pass
    elif type == 'md':
        pic_name_list = [".jpg",".jpeg",".png"]
        if enable_pic_download:
            for k in pic_name_list:
                pic_url_re = re.compile(r'https:(.*?)'+k)
                pic_url_list = pic_url_re.findall(write_txt)
                pic_real_list = []
                for i in range(len(pic_url_list)):
                    pic_url_list[i] = "https:" + pic_url_list[i] + k
                    pic_real = "![](" + dir_now + "\\" + pic_url_list[i].split('/')[-1] + ")" + "\n"
                    pic_real_list.append(pic_real)
                for i in range(len(pic_url_list)):
                    write_txt = write_txt.replace(pic_url_list[i],pic_real_list[i])
        else:
            for k in pic_name_list:
                write_txt = write_txt.replace("https:","![](https:").replace(k,k+")")
    if split_char == "\n":
        write_txt = write_txt.replace("\n\n\n","\n\n")
    os.chdir(path)

    write_txt_all(write_txt,book_title,path,type)

    if type !="md" or type != "txt":
        pypandoc.convert_file(book_title + '.md', type, format='markdown', outputfile= book_title + '.' + type)
    
    print(book_title,"is over.")
    print("Downloading",book_title,"is over.")

def linovelib_search(keyword,num=5):
    keyword = quote(keyword)
    web = "https://www.linovelib.com/S0/?searchkey=" + keyword + "&searchtype=all"
    content = requests.get(web, headers={'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-cn; Redmi K30 Pro Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.6 Mobile Safari/537.36 COVC/045635'})
    soup = BeautifulSoup(content.text, "html.parser")
    title_list = soup.find_all("h4", class_="book-title")
    desc_list = soup.find_all("p", class_="book-desc")
    author_list = soup.find_all("span", class_="book-author")
    link_list = soup.find_all("a", class_="book-layout",href=True)
    for i in range(max(num,len(title_list))):
        title = title_list[i].get_text()
        desc = desc_list[i].get_text()
        author = author_list[i].get_text()
        link = link_list[i]["href"]
        print("书名:",title.replace("\n", "").replace("\r", "").replace("\t", ""))
        print(author.replace("作者", "作者: ").replace("\n", "").replace("\r", "").replace("\t", ""))
        print("简介:",desc.replace("\n", "").replace("\r", "").replace("\t", ""))
        print("网址:","https://www.linovelib.com" + link)
        print("下载：","linovelib download",link.replace("/novel/","").replace(".html",""))
        print("--------------")
    print("搜索结果:",max(num,len(title_list)),"本")
    return link_list[0]["href"].replace("/novel/","").replace(".html","")

def linovelib_search_simple(keyword):
    keyword = quote(keyword)
    web = "https://www.linovelib.com/S0/?searchkey=" + keyword + "&searchtype=all"
    content = requests.get(web, headers={'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-cn; Redmi K30 Pro Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.6 Mobile Safari/537.36 COVC/045635'})
    soup = BeautifulSoup(content.text, "html.parser")
    link_list = soup.find_all("a", class_="book-layout",href=True)
    return link_list[0]["href"].replace("/novel/","").replace(".html","")

def change_to_id(id):
    if type(id) == int:
            id = str(id)
    elif id.find('https://www.linovelib.com/novel/') != -1:
        if id.find('catalog') != -1:
            id = id.split('/')[-2]
        elif id.count('/') == 5:
            id = id.split('/')[-2]
        elif id.count('/') == 4:
            id = id.split('/')[-1].strip(".html")
    else:
        id = linovelib_search_simple(id)
    return id

def linovelib_info(id):
    web = "https://www.linovelib.com/novel/" + id + ".html"
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    info_txt = soup.find("div",class_="book-dec Jbook-dec hide").get_text()
    title_txt = soup.find("h1",class_="book-name").get_text()
    nums_txt  = soup.find("div",class_="nums").get_text()
    label_txt = soup.find("div",class_="book-label").get_text()
    print(title_txt.replace("\n","")+"\n")
    print(label_txt.replace("\n"," ")+"\n")
    print(nums_txt.replace("\n",""))
    print(info_txt)
    return title_txt.replace("\n","")+"\n"+label_txt.replace("\n"," ")+"\n"+nums_txt.replace("\n","")+"\n"+info_txt

def linovelib_show(id):
    novel_catalog = "https://www.linovelib.com/novel/" + id + "/catalog"
    catalog_list = get_chapter_list(novel_catalog)
    book_title = get_title_book(novel_catalog)
    print("书名：",book_title)
    for i in range(len(catalog_list)):
        if len(catalog_list[i]) == 1:
            print(i,":",catalog_list[i][0]+":\n")
        else:
            print(i,":",catalog_list[i][0],":",catalog_list[i][1])
    return catalog_list

def linovelib_rec(type='monthvisit',page=1):
    web = "https://www.linovelib.com/top/" + type + "/" +str(page)+ ".html"
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    title_list = soup.find_all("div",class_="rank_d_b_name")
    cate_list = soup.find_all("div",class_="rank_d_b_cate")
    info_list = soup.find_all("div",class_="rank_d_b_info")
    last_list = soup.find_all("div",class_="rank_d_b_last")
    i = random.randint(0,len(title_list)-1)
    title = title_list[i].get_text()
    cate = cate_list[i].get_text()
    info = info_list[i].get_text()
    last = last_list[i].get_text()
    url = "https://www.linovelib.com" + title_list[i].find("a").get("href")
    print(title.strip()+"\n"+cate+"\n"+info+"\n"+last.replace("最新章节","最新章节: ")+"\n"+"网址: "+url+"\n\n"+"下载：linovelib download "+url.replace("https://www.linovelib.com/novel/","").replace(".html","")+"\n")
    return title,cate,info,last,url


def get_chapter_pic(web,sleep_time=1,enable_pic_download=True):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    pic_list = []
    pic_list_soup = soup.find_all("img",class_="imagecontent")
    for i in pic_list_soup:
        IMAGE_URL = i.get('src')
        if enable_pic_download:
            time.sleep(sleep_time)
            print("Getting from:",IMAGE_URL)
            image_name = IMAGE_URL.split('/')[-1]
            r = requests.get(IMAGE_URL)
            with open(image_name, 'wb') as f:
                f.write(r.content) 
        pic_list.append(IMAGE_URL)
    return pic_list

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