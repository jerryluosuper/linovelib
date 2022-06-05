import re
import time

import fake_useragent
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