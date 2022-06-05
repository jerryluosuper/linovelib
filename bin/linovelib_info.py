import requests
from bs4 import BeautifulSoup
import fake_useragent

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

linovelib_info("2547")
