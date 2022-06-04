import json
import requests
import time
import fake_useragent
from bs4 import BeautifulSoup
import re

web_original = "https://www.linovelib.com/novel/"

web_fake = "https://www.linovelib.com/novel/10000.html"
content_fake = requests.get(web_fake, headers={'User-Agent': fake_useragent.UserAgent().firefox})

i = 2001
novel_list = ["Name"]

while True:
    try:
        time.sleep(5)
        web = web_original + str(i) + ".html"
        content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().firefox})
        if content.text == content_fake.text:
            break
        soup = BeautifulSoup(content.text, "html.parser")
        try:
            soup_text = str(soup.select("body > div.wrap > div.book-html-box.clearfix > div:nth-child(1) > div.book-detail.clearfix > div.book-info > h1"))
            re_title = re.compile(r'>(.*?)</h1>')
            title = re_title.findall(soup_text)
            novel_list.append(title[0])
            print(i,":",title[0])
        except:
            novel_list.append("None")
            print(i,":","None")
    except:
        break
    i += 1

with open('novel_list.json', 'w+') as f:
    json.dump(novel_list, f,ensure_ascii=False)