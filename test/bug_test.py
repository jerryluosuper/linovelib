import requests
import time
import fake_useragent
import re
import os
# web = "https://www.linovelib.com/novel/10000.html"
# content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})
write_txt = "https://img.linovelib.com/3/3224/164377/193718.jpg\nhttps://img.linovelib.com/3/3224/164377/193719.jpg\n然而，当我发的line一直都是未读的时候，我开始担心起来了。"
dir_now = os.getcwd()
pic_url_re = re.compile(r'https:(.*?).jpg')
pic_url_list = pic_url_re.findall(write_txt)
print(pic_url_list)
pic_real_list = []
for i in range(len(pic_url_list)):
    print(i)
    pic_url_list[i] = "https:" + pic_url_list[i] + ".jpg"
    pic_real = "![](" + dir_now + "\" + pic_url_list[i].split('/')[-1] + ")" + "\n"
    pic_real_list.append(pic_real)
for i in range(len(pic_url_list)):
    write_txt = write_txt.replace(pic_url_list[i],pic_real_list[i])
print(write_txt)