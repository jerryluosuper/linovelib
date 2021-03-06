import re
import time

import fake_useragent
import requests
from bs4 import BeautifulSoup

web = "https://www.linovelib.com/novel/2547/161282.html"

def get_title_chapter(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
    soup = BeautifulSoup(content.text, "html.parser")
    title = soup.select_one("#mlfy_main_text > h1")
    return title.text

def get_chapter_one_chapter(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
    soup = BeautifulSoup(content.text, "html.parser")
    soup_text = soup.findAll('div', class_="read-content")
    return soup_text

def get_chapter_all(web,sleep_time=1):
    soup_list = [ ]
    soup_list.append(get_chapter_one_chapter(web))
    web_original = web[0:(len(web)-5)]
    text_original = soup_list[0][0].get_text()[0:10]
    i=2
    while True:
        time.sleep(sleep_time)
        web = web_original + '_' + str(i) + '.html'
        # print_chapter(web)
        chapter_now = get_chapter_one_chapter(web)
        if len(chapter_now) == 0 or chapter_now[0].get_text() == "\n\n":
            # print("Error: No chapter now")
            break
        if chapter_now[0].get_text()[0:10] == text_original:
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
    title = get_title_chapter(web)
    text = title + "\n" + text
    return text

def write_txt_all(text,title):
    f = open(title+'.txt','w',encoding="utf-8")
    f.write(text)
    f.close()

def get_chapter_all_txt(web):
    soup_list = get_chapter_all(web)
    title = get_title_chapter(web)
    text = get_text(soup_list,"\n")
    write_txt_all(text,title)

get_chapter_all_txt(web)

# print(get_chapter_one("https://www.linovelib.com/novel/2890/163993_8.html")[0].get_text()=="\n\n")

print("Over!")
