import requests
from bs4 import BeautifulSoup
from urllib import parse

web = "fate"

def search_book(keyword):
    keyword = parse.quote(keyword)
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
search_book(web)