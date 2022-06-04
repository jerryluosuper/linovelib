from lib.linovel_catalog import *
from lib.linovel_chapter_download import *
import requests
import time
from bs4 import BeautifulSoup
import re
import fake_useragent

id = 2547

def linovelib_download(id):
    novel_catalog = "https://www.linovelib.com/novel/" + str(id) + "/catalog"
    catalog_list = get_chapter_list(web)
    
