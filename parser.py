import requests
import time
from bs4 import BeautifulSoup
import re
import fake_useragent
# import sys

# if len(sys.argv) != 2 :
#     print('error')
#     sys.exit()

# web = sys.argv[1]
#web = input("请输入网址: ")
web = "https://www.linovelib.com/novel/2547/92958.html"
content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
soup = BeautifulSoup(content.text, "html.parser")
title = str(soup.select("#mlfy_main_text > h1"))
re_title = re.compile(r'<h1>(.*?)</h1>')
title = re_title.findall(title)
print(title)


soup_list = [ ]
soup_list.append(soup.findAll('div', class_="read-content"))

web = web[0:(len(web)-5)]

# i=2
# while i<10:
#     time.sleep(1)
#     try:
#         content = requests.get(web+'_'+str(i)+'.html', headers={'User-Agent': fake_useragent.UserAgent().chrome})
#         soup = BeautifulSoup(content.text, "html.parser")
#         soup_text = soup.findAll('div', class_="read-content")
#         if soup_text[0].text == '\n\n':
#             break
#         soup_list.append(soup_text)
#         i = i + 1
#         print(i)
#     except:
#         break

content = requests.get(web+'_'+str(150)+'.html', headers={'User-Agent': fake_useragent.UserAgent().chrome})
soup = BeautifulSoup(content.text, "html.parser")
soup_text = soup.findAll('div', class_="read-content")
print(soup_text[0].text)
soup_list.append(soup_text)
i = i + 1
print(i)



text=''
for i in soup_list:
    text += i[0].get_text(separator="\n")
text = text.replace('（本章未完）', '')

f = open(title[0]+'.txt','w',encoding="utf-8")
f.write(text)
f.close()

print("Over!")
