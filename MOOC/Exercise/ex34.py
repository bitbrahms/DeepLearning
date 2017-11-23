import requests

from bs4 import BeautifulSoup
url = 'http://baidu.com'
r = requests.get('url')
soup = BeautifulSoup(r.text, 'lxml')
print(soup.status_code)
import urllib
import time