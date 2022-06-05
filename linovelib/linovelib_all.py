import re
import time

import fake_useragent
import requests
from bs4 import BeautifulSoup

from urllib.parse import quote

def get_title_chapter(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    title = soup.select_one("#mlfy_main_text > h1")
    return title.text

def get_chapter_one_chapter(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    soup_text = soup.findAll('div', class_="read-content")
    print("Getting From:",web)
    return soup_text

def get_chapter_all(web,sleep_time=1):
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
    return soup_list

def get_text(soup_list,separator_now):
    text=''
    for i in soup_list:
        if len(i) != 0:
            text += i[0].get_text(separator=separator_now)
    text = text.replace('（本章未完）', '')
    return text

def write_txt_all(text,title):
    f = open(title+'.txt','w',encoding="utf-8")
    f.write(text)
    f.close()

def get_chapter_all_txt(web,wait_time=0.5,split_char='\n'):
    soup_list = get_chapter_all(web,wait_time)
    title = get_title_chapter(web)
    text = get_text(soup_list,split_char)
    write_txt_all(text,title)

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

def linovelib_search(keyword):
    keyword = quote(keyword)
    web = "https://www.linovelib.com/S0/?searchkey=" + keyword + "&searchtype=all"
    content = requests.get(web, headers={'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11; zh-cn; Redmi K30 Pro Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/11.6 Mobile Safari/537.36 COVC/045635'})
    soup = BeautifulSoup(content.text, "html.parser")
    title_list = soup.find_all("h4", class_="book-title")
    desc_list = soup.find_all("p", class_="book-desc")
    author_list = soup.find_all("span", class_="book-author")
    link_list = soup.find_all("a", class_="book-layout",href=True)
    for i in range(len(title_list)):
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
    print("搜索结果:",len(title_list),"本")

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