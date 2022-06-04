import requests
from bs4 import BeautifulSoup
import re
import fake_useragent

web = "https://www.linovelib.com/novel/3234/catalog"

def get_title_book(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
    soup = BeautifulSoup(content.text, "html.parser")
    title = soup.select_one("html body div.wrap div.container div.book-meta h1")
    return title.text

def get_chapter_list(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
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

print(get_chapter_list(web))