import requests
import time
import fake_useragent
web = "https://www.linovelib.com/novel/10000.html"
content = requests.get(web, headers={'User-Agent': fake_useragent.UserAgent().chrome})