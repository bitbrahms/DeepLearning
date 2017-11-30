
# coding: utf-8

# In[23]:


import urllib
import os
import re
import requests
from bs4 import BeautifulSoup


# In[2]:


print(os.path)


# In[3]:


if not os.path.exists('D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images/'):
    os.mkdir('D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images/')


# In[7]:


def main():
    url = 'http://www.baidu.com'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) 		AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    html = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(html)
    print(data.read())


# In[8]:


if __name__ == 'main':
    main()


# In[20]:


url = 'http://www.baidu.com'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) 		AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
html = urllib.request.Request(url, headers=headers)
data = urllib.request.urlopen(html)
data = data.read()
print(data)


# In[54]:


res = requests.get('https://site.douban.com/106875/',headers=headers)
data = re.findall('class="pic"><img src="(.*?)"',res.text)
local = 'D:/CPU_Manny/workspace/DeepLearning/MOOC/Exercise/images/'
x = 0
for i in data:
    urllib.request.urlretrieve(i,local+str(x)+'.jpg',cbk)
    x = x+1


# In[53]:


def cbk(a,b,c):
    percent = 100*a*b/c
    if percent > 100:
        percent = 100
    print("%.2f%%" % percent)


# In[55]:


get_ipython().magic('pinfo requests.session')


# In[56]:


session = requests.Session()


# In[57]:


s = requests.Session()
r = s.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(r.text)


# In[64]:


import requests  
login_data = {'email': 'beilixumeng@163.com',  
        'passWord': 'bit2010010203'}
login_url = 'https://www.zhihu.com/login/email'
requests.post(login_url, data=login_data)


# In[72]:


url = 'https://www.zhihu.com/'
cookie = 'd_c0="ABAA2gGILwqPTjUnnIph_y9EWCgKaQsH3vc=|1467768461"; _za=e030fe39-123f-4ad7-97f7-9f2eeb401fdc; _zap=9c07f954-1917-45b7-9f98-bcc4d6f82f96; q_c1=4166c4ce091c444eb6f4ee4c0987c957|1507530593000|1467768461000; _xsrf=e4ed7c5b221ea0b587bc833f032ac284; q_c1=4166c4ce091c444eb6f4ee4c0987c957|1511235210000|1467768461000; aliyungf_tc=AQAAAJ3W+Qe3wgwAzjPndAZKJDm4ifoM; _xsrf=e4ed7c5b221ea0b587bc833f032ac284; __utma=51854390.1329783140.1508292606.1510206886.1512031362.7; __utmc=51854390; __utmz=51854390.1510206886.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|2=registration_date=20130421=1^3=entry_date=20160706=1; z_c0=Mi4xOGJNS0FBQUFBQUFBRUFEYUFZZ3ZDaGNBQUFCaEFsVk5mVFFOV3dDa3c1U0p1QWpYSFJORUZJY2pMTlNhaG9taXBn|1512040061|4477179d4be38c2c3d0cba8cafe2ee97521a2b3b; r_cap_id="MTYxNDM3Mzk2NmVjNDllNGE2MTdmNzY3ZjRmNDVhOTU=|1512040061|9c876d59b079912433586a7ee9e128503735a75b"; cap_id="MTcyZDY0ODczNmJiNDEwN2I2Nzg5ODg0Mjk3ZDNjMzg=|1512040061|2e1476ffa6a9bf758fcba667df3e8dd6dafe41be"'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) 	AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','cookie':cookie}
res = requests.get(url,headers=headers)
print(res)


# In[122]:


url = 'https://accounts.douban.com/login'
formdata = {
    'form_email':'beilixumeng@163.com',
    'form_password':'2010010203',
    'user_login':'登录'}
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) 	AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
res = requests.post(url,data=formdata,headers=headers)
#print(res.text)
print(res.url)
soup = BeautifulSoup(res.text,'lxml')
data=soup.find_all('img',id='captcha_image')
print(data)|

