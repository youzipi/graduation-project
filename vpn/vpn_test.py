import requests
from lxml import html

cookies = {

    "DSFirstAccess": "1453365010",
    "DSID": "a7e6bfee1178572278731f46c2e17955",
    "DSLastAccess": "1453368982",
    "DSSignInURL": "/",
}

"""
https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=E&searchby=N&hothigh=G&searchtitle=HTTP&searchscientist=&searchinst=&searchcountry=&searchjournal=&x=30&y=6
"""

r = requests.get('https://vpn.nuist.edu.cn/dana-na/auth/url_default/welcome.cgi',
                 auth=('20121344018', '250036'))
# print r.content

# esi = requests.get(
#         'https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=E&searchby=N&hothigh=H&searchtitle=web&searchscientist=&searchinst=&searchcountry=&searchjournal=&x=39&y=6',
#     # 'D:\0projects\graduation-project\Essential Science Indicators Version 2.3.html',
#         cookies=cookies,
#         # auth=('20121344018', '250036'),
# )
#
# content = esi.content
from cookies import content
from scrapy.selector import Selector

tree = html.fromstring(content)
# print content

# table1 = tree.xpath('/html/body/table[4]/tbody/tr[3]/td/table')
table1 = tree.xpath('/html/body/table[4]')
# table1 = tree.xpath('/html/head')
# for t in table1:
#     print

# print dir(table1[0])
# print table1[0].__dict__
# print table1[0].text()
# print table1[0].text_content()
c = Selector(text=content)
print len(c.xpath('/html/body/table').extract())

tables = c.xpath('/html/body/table').extract()  # 单个论文
# for t in tables:
#     print t
ts = c.xpath('/html/body/table[4]/tbody/tr[3]/td/table')
trs = ts[2].xpath('./tbody/tr')

pairs = trs[0].xpath('./td')
# print trs[0].xpath('./td').extract()
# print pairs[1].xpath('text()').extract()
print pairs[1].extract()        # <td width="80%">INTERFERON-STIMULATED GENES: A COMPLEX <strong>WEB</strong> OF HOST DEFENSES </td>


# print c.xpath('/html/body/table[4]/tbody/tr[3]/td/table').extract()
# c.xpath('/html/body/table[4]/tbody/tr[3]/td/table').extract()
