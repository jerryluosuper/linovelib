import random
import requests
from bs4 import BeautifulSoup
import fake_useragent

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

linovelib_rec()