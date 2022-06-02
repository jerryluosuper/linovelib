import requests
import time
from bs4 import BeautifulSoup
import re
import fake_useragent

web = "https://www.linovelib.com/novel/2890/163991.html"

def get_title(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
    soup = BeautifulSoup(content.text, "html.parser")
    title = str(soup.select("#mlfy_main_text > h1"))
    re_title = re.compile(r'<h1>(.*?)</h1>')
    title = re_title.findall(title)
    return title

def get_chapter_one(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
    soup = BeautifulSoup(content.text, "html.parser")
    soup_text = soup.findAll('div', class_="read-content")
    return soup_text

def get_chapter_all(web,sleep_time=1):
    soup_list = [ ]
    soup_list.append(get_chapter_one(web))
    web_original = web[0:(len(web)-5)]
    text_original = soup_list[0][0].get_text()[0:10]
    i=2
    while True:
        time.sleep(sleep_time)
        web = web_original + '_' + str(i) + '.html'
        # print(web)
        chapter_now = get_chapter_one(web)
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

def get_text(soup_list):
    text=''
    for i in soup_list:
        if len(i) != 0:
            text += i[0].get_text()
    text = text.replace('（本章未完）', '')
    title = get_title(web)[0]
    text = title + "\n" + text
    return text

def write_txt(text,title):
    f = open(title+'.txt','w',encoding="utf-8")
    f.write(text)
    f.close()

def get_chapter_all_txt(web):
    soup_list = get_chapter_all(web)
    title = get_title(web)[0]
    text = get_text(soup_list)
    write_txt(text,title)

get_chapter_all_txt(web)

# print(get_chapter_one("https://www.linovelib.com/novel/2890/163993_8.html")[0].get_text()=="\n\n")

print("Over!")
