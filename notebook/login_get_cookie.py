
# coding: utf-8

# In[138]:

import requests
# from bs4 import BeautifulSoup
# import time
# import os
# import json
from scrapy.selector import Selector
from scrapy import Request,FormRequest
from lxml import html


# In[139]:

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


# In[140]:

data = {
    'tz_offset': '480',
    'username': '20121344018',
    'password': '250036',
    'realm': u'本专科生',
    'btnSubmit': u'登陆',
}


# In[115]:

s = requests.session()


# In[153]:

postreq = s.post('https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi', headers=headers, data=data)
postreq.encoding = 'utf8'


# In[157]:

# sc_resp = FormRequest(url='https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi',
#                       #method="POST",
#                       headers=headers,
#                       formdata=data)


# In[158]:

# sc_resp.cookies


# In[109]:

# print postreq.text
# s.close()


# In[156]:

# s.cookies


# In[118]:

print postreq.cookies.get_dict()


# In[119]:

# postreq.status_code


# In[120]:

#req = s.post('https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+home.cgi',cookies=postreq.cookies)
#https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=E&searchby=N&hothigh=H&searchtitle=web&searchscientist=&searchinst=&searchcountry=&searchjournal=&x=39&y=6
search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER+SCIENCE&hothigh=G&option=G&x=19&y=2
"""
req = s.get(search_url)


# In[121]:

# req.url


# In[126]:

# sc_cookies = s.cookies
# s.close()
# sc_resp = Request(url=search_url, headers=headers,
#                         cookies=sc_cookies
#                         )


# In[127]:

# sc_resp.body


# In[75]:

content = req.text
#print content


# In[106]:

c = Selector(text=content)

#tables = c.xpath('/html/body/table').extract()
#print len(tables)
#print tables
# sections = c.xpath('/html/body/table[4]') #？？
# sections = c.xpath('/html/body/table[4]/tr[3]/td/table')
# sections = c.xpath('/html/body/table[4]/tr[3]/td/table')
# target_url = c.xpath('/html/body/table[4]/tr[3]/td/table[2]/tbody/tr/td[2]/a')
target_url = c.xpath('/html/body/table[4]/tr[3]/td/table/table[34]/tr/td[2]/a/@href')
# print sections.extract()
# print len(sections)
print len(target_url)


# In[123]:

urls = c.xpath('//td[2]/a/img[contains(@src, "gotowos.gif")]/../@href')
urls.extract()
len(urls)


# In[92]:

print target_url.extract()


# In[48]:

# trs = sections[2].xpath('./tbody/tr')

# pairs = trs[0].xpath('./td')
# # print trs[0].xpath('./td').extract()
# # print pairs[1].xpath('text()').extract()
# # print pairs[1].extract()        # <td width="80%">INTERFERON-STIMULATED GENES: A COMPLEX <strong>WEB</strong> OF HOST DEFENSES </td>
# for p in trs:
#     pair = p.xpath('./td')
#     # print pair.extract()
#     if len(pair) < 2:
#         continue
#     print pair[0].extract()
#     print pair[1].extract()

s.close()
