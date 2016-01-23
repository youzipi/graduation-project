# coding=utf-8
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

tables = c.xpath('/html/body/table').extract()
# for t in tables:
#     print t

"""
/html/body/table[4]/tbody/tr[3]/td/table
第一个 是空的
2. Citations: 71
3. 详细信息

"""
sections = c.xpath('/html/body/table[4]/tbody/tr[3]/td/table')

"""
详细信息
1  Title
3 Authors
5 Source
7 Addresses
9 Field

2,4,6,8 为空行
<tr><td colspan="2">&nbsp;</td></tr>
判断方式 len(pair) < 2:

1.
<td width="20%" valign="top"><b>Title:</b></td>
<td width="80%">INTERFERON-STIMULATED GENES: A COMPLEX <strong>WEB</strong> OF HOST DEFENSES </td>

3.
<td width="20%" valign="top"><b>Authors:</b></td>
<td width="80%">SCHNEIDER WM;  CHEVILLOTTE MD;  <a href="https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+rankdatapage.cgi?option=A&amp;search=RICE%2C%20CM&amp;searchby=N">RICE CM </a>   </td>

5.
<td width="20%" valign="top"><b>Source:</b></td>
<td width="80%"><a href="https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+rankdatapage.cgi?option=J&amp;search=ANNU%20REV%20IMMUNOL&amp;searchby=N">ANNU REV IMMUNOL</a> 32: 513-545 2014 </td>
<td width="20%" valign="top"><b>Addresses:</b></td>

7.
<td width="80%"><a href="https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+rankdatapage.cgi?option=I&amp;search=ROCKEFELLER%20UNIV&amp;searchby=N"> Rockefeller Univ,</a> Lab Virol &amp; Infect Dis, New York,  NY 10065 USA.<br></td>

9.
<td width="20%" valign="top"><b>Field:</b></td>
<td width="80%">
       <a href="https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=H&amp;search=IMMUNOLOGY&amp;searchby=F&amp;hothigh=H&amp;article_id=000336427400017">
	IMMUNOLOGY </a><br>

    <br></td>

"""
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


# print c.xpath('/html/body/table[4]/tbody/tr[3]/td/table').extract()
# c.xpath('/html/body/table[4]/tbody/tr[3]/td/table').extract()
