# coding: utf-8

# In[2]:

import requests
from scrapy.selector import Selector
from scrapy import Request, FormRequest
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

# In[67]:

req = s.get(
    'http://web2.nuist.edu.cn/zsw/2011-12/201112914198.html',
    #     'http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html',
    #                  headers=headers,
    #                  data=data
)
req.encoding = 'utf8'

# In[64]:

req.text

# In[78]:

content = req.text
c = Selector(text=content)
# print c.xpath('//*[@id="content_news"]/div[1]/text()')[0].extract()
table = c.xpath('//*[@class="txt"]//table')
# print c.xpath('//*[@class="txt"]').extract()
th = table.xpath('.//tr')[0]  # 第一个是表头
datas = th.xpath('.//td/p//text()').extract()
# //*[@class="txt"]//table//tr[1]//td/p//text()
# print datas
for i in datas:
    print i

trs = table.xpath('.//tr')[1:]  # 第一个是表头
# print trs.extract()
# //*[@id="content_news"]/div[3]/div/p/table/tbody/tr[2]/td[2]/p/span[1]
# print trs[0].xpath('.//td[1]/p/span[1]/text()').extract()[0]# 省份
# print trs[0].xpath('.//td[2]/p/span[1]/text()').extract()[0]# 理工
# print trs[0].xpath('.//td[3]/p/span[1]/text()').extract()[0]#最高分
# print trs[0].xpath('.//td[4]/p/span[1]/text()').extract()[0]#最低分
# print trs[0].xpath('.//td[5]/p/span[1]/text()').extract()[0]#平均分
# print trs[0].xpath('.//td[6]/p/span[1]/text()').extract()[0]#省控线 2
for tr in trs:
    datas = tr.xpath('.//td/p//text()').extract()
    #     print datas
    #     for i in datas:
    #         print i
    print datas[0], datas[1], datas[4]


# print trs.extract()


# In[79]:


def parse(url):
    req = s.get(url,
                #                  headers=headers,
                #                  data=data
                )
    req.encoding = 'utf8'
    content = req.text
    c = Selector(text=content)
    title = c.xpath('//*[@id="content_news"]/div[1]/text()')[0].extract()
    print title
    table = c.xpath('//*[@class="txt"]//table')
    # print c.xpath('//*[@class="txt"]').extract()
    th = table.xpath('.//tr')[0]  # 第一个是表头
    datas = th.xpath('.//td/p//text()').extract()
    # //*[@class="txt"]//table//tr[1]//td/p//text()
    # print datas
    for i in datas:
        print i
    trs = table.xpath('.//tr')[1:]  # 第一个是表头
    # //*[@id="content_news"]/div[3]/div/p/table/tbody/tr[2]/td[2]/p/span[1]
    # print trs[0].xpath('.//td[1]/p/span[1]/text()').extract()[0]# 省份
    # print trs[0].xpath('.//td[2]/p/span[1]/text()').extract()[0]# 理工
    # print trs[0].xpath('.//td[3]/p/span[1]/text()').extract()[0]#最高分
    # print trs[0].xpath('.//td[4]/p/span[1]/text()').extract()[0]#最低分
    # print trs[0].xpath('.//td[5]/p/span[1]/text()').extract()[0]#平均分
    # print trs[0].xpath('.//td[6]/p/span[1]/text()').extract()[0]#省控线 # 每年的顺序不一样

    for tr in trs:
        #         datas = tr.xpath('.//td/p/span[1]/text()').extract()
        #         datas = tr.xpath('.//td/p//text()').extract() # 2015
        # datas = tr.xpath('.//td/p//text()').extract()  # 2015
        datas = tr.xpath('.//td//text()').extract()  # 2014
        for i in datas:
            print i,
            print ''
        # print trs.extract()


# In[80]:

url_list = [
    # {
    #     'url': 'http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html',
    #     'year_xpath': './/td/p//text()',
    # },
    # {
    #     'url': 'http://web2.nuist.edu.cn/zsw/2015-4/201547131450.html',
    #     'year_xpath': './/td/text()',
    # },
    'http://web2.nuist.edu.cn/zsw/2015-11/20151116141314.html', # 2015
    'http://web2.nuist.edu.cn/zsw/2015-4/201547131450.html',    # 2014
    'http://web2.nuist.edu.cn/zsw/2011-6/201161102742.html'  # 2010
    # 页面链接
]

# In[81]:

map(parse, url_list)


# In[ ]:
