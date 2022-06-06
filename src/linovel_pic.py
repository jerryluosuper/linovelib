import re
import time

import fake_useragent
import requests
from bs4 import BeautifulSoup
import os

web = "https://www.linovelib.com/novel/2547/164720.html"

os.makedirs("插图")

def get_chapter_pic(web,dir_name,sleep_time=1):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().random})
    soup = BeautifulSoup(content.text, "html.parser")
    pic_list = []
    pic_list_soup = soup.find_all("img",class_="imagecontent",src=True)
    os.chdir(dir_name)
    for i in pic_list_soup:
        IMAGE_URL = i.get('src')
        image_name = IMAGE_URL.split('/')[-1]
        r = requests.get(IMAGE_URL)
        with open(image_name, 'wb') as f:
            f.write(r.content) 
        pic_list.append(IMAGE_URL)
        time.sleep(sleep_time)
    return pic_list
print(get_chapter_pic(web,"插图"))