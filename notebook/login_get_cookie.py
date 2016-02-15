# coding: utf-8

# In[1]:

import requests
# from bs4 import BeautifulSoup
# import time
# import os
# import json
from scrapy.selector import Selector
from lxml import html

# In[8]:

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '122',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'vpn.nuist.edu.cn',
    'Origin': 'https://vpn.nuist.edu.cn',
    'Referer': 'https://vpn.nuist.edu.cn/dana-na/auth/url_default/welcome.cgi',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
}

# In[9]:

data = {
    'tz_offset': '480',
    'username': '20121344018',
    'password': '250036',
    'realm': u'本专科生',
    'btnSubmit': u'登陆',
}

# In[10]:

s = requests.session()

# In[11]:

postreq = s.post('https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi', headers=headers, data=data)
postreq.encoding = 'utf8'

# In[6]:

# print postreq.text


# In[12]:

postreq.cookies.get_dict()

# In[13]:

postreq.status_code

# In[15]:

# req = s.post('https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+home.cgi',cookies=postreq.cookies)
# https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=E&searchby=N&hothigh=H&searchtitle=web&searchscientist=&searchinst=&searchcountry=&searchjournal=&x=39&y=6
search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER+SCIENCE&hothigh=G&option=G&x=19&y=2
"""
req = s.get(search_url)

# In[16]:

content = req.text
print content

# In[104]:

c = Selector(text=content)

tables = c.xpath('/html/body/table').extract()
print len(tables)
# sections = c.xpath('/html/body/table[4]') #？？
# sections = c.xpath('/html/body/table[4]/tr[3]/td/table')
# sections = c.xpath('/html/body/table[4]/tr[3]/td/table')
# target_url = c.xpath('/html/body/table[4]/tr[3]/td/table[2]/tbody/tr/td[2]/a')
target_url = c.xpath('/html/body/table[4]/tr[3]/td/table/table[3]/tr/td[2]/a/@href')
# print sections.extract()
# print len(sections)
print len(target_url)

# In[105]:

target_url.extract()

# In[23]:

trs = sections[2].xpath('./tbody/tr')

pairs = trs[0].xpath('./td')
# print trs[0].xpath('./td').extract()
# print pairs[1].xpath('text()').extract()
# print pairs[1].extract()        # <td width="80%">INTERFERON-STIMULATED GENES: A COMPLEX <strong>WEB</strong> OF HOST DEFENSES </td>
for p in trs:
    pair = p.xpath('./td')
    # print pair.extract()
    if len(pair) < 2:
        continue
    print pair[0].extract()
    print pair[1].extract()
