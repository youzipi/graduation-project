
# coding: utf-8

# In[2]:

import requests
from scrapy.selector import Selector
from scrapy import Request,FormRequest
from lxml import html


# In[8]:

s = requests.session()


# In[25]:

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '122',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'web2.nuist.edu.cn',
#     'Origin': 'http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html',
    'Referer': 'http://web2.nuist.edu.cn/zsw/sy/index.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
}


# In[28]:

req = s.get('http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html',
#                  headers=headers,
#                  data=data
                )
req.encoding = 'utf8'


# In[29]:

req.text


# In[51]:

content = req.text
c = Selector(text=content)
print c.xpath('//*[@id="content_news"]/div[1]/text()')[0].extract()
table = c.xpath('//*[@class="txt"]//table')
# print c.xpath('//*[@class="txt"]').extract()
trs = table.xpath('.//tr')[1:] # 第一个是表头
# //*[@id="content_news"]/div[3]/div/p/table/tbody/tr[2]/td[2]/p/span[1]
# print trs[0].xpath('.//td[1]/p/span[1]/text()').extract()[0]# 省份
# print trs[0].xpath('.//td[2]/p/span[1]/text()').extract()[0]# 理工
# print trs[0].xpath('.//td[3]/p/span[1]/text()').extract()[0]#最高分
# print trs[0].xpath('.//td[4]/p/span[1]/text()').extract()[0]#最低分
# print trs[0].xpath('.//td[5]/p/span[1]/text()').extract()[0]#平均分
# print trs[0].xpath('.//td[6]/p/span[1]/text()').extract()[0]#省控线

for tr in trs:
    datas = tr.xpath('.//td/p/span[1]/text()').extract()
#     for i in datas:
#         print i  
    print datas[0],datas[1],datas[4]
# print trs.extract()


# In[56]:


def parse(url):
    req = s.get('http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html',
#                  headers=headers,
#                  data=data
                )
    req.encoding = 'utf8'
    content = req.text
    c = Selector(text=content)
    print c.xpath('//*[@id="content_news"]/div[1]/text()')[0].extract()
    table = c.xpath('//*[@class="txt"]//table')
    # print c.xpath('//*[@class="txt"]').extract()
    trs = table.xpath('.//tr')[1:] # 第一个是表头
    # //*[@id="content_news"]/div[3]/div/p/table/tbody/tr[2]/td[2]/p/span[1]
    # print trs[0].xpath('.//td[1]/p/span[1]/text()').extract()[0]# 省份
    # print trs[0].xpath('.//td[2]/p/span[1]/text()').extract()[0]# 理工
    # print trs[0].xpath('.//td[3]/p/span[1]/text()').extract()[0]#最高分
    # print trs[0].xpath('.//td[4]/p/span[1]/text()').extract()[0]#最低分
    # print trs[0].xpath('.//td[5]/p/span[1]/text()').extract()[0]#平均分
    # print trs[0].xpath('.//td[6]/p/span[1]/text()').extract()[0]#省控线

    for tr in trs:
        datas = tr.xpath('.//td/p/span[1]/text()').extract()
    #     for i in datas:
    #         print i  
        print datas[0],datas[1],datas[4]
    # print trs.extract()


# In[54]:

url_list = [
    'http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html',# 2015
    'http://web2.nuist.edu.cn/zsw/2015-4/201547131450.html', # 2014
    #页面链接
]


# In[57]:

map(parse,url_list)


# In[ ]:



