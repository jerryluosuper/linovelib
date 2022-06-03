import requests
import time
from bs4 import BeautifulSoup
import re
import fake_useragent

web = "https://www.linovelib.com/novel/568/catalog"

def get_title_book(web):
    content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
    soup = BeautifulSoup(content.text, "html.parser")
    title = str(soup.select("html body div.wrap div.container div.book-meta h1"))
    re_title = re.compile(r'<h1>(.*?)</h1>')
    title = re_title.findall(title)
    return title[0]

print(get_title_book(web))