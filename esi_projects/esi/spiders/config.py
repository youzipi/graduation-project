# encoding=utf8
import requests
# from bs4 import BeautifulSoup
# import time
# import os
# import json
from scrapy.selector import Selector
from lxml import html

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
# 帐号登陆
login_form_data = {
    'tz_offset': '480',
    'username': '20121344018',
    'password': '250036',
    'realm': u'本专科生',
    'btnSubmit': u'登陆',
}

s = requests.session()

postreq = s.post('https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi', headers=headers, data=login_form_data)
postreq.encoding = 'utf8'

# req = s.post('https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+home.cgi',cookies=postreq.cookies)
# https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=E&searchby=N&hothigh=H&searchtitle=web&searchscientist=&searchinst=&searchcountry=&searchjournal=&x=39&y=6
search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER+SCIENCE&hothigh=G&option=G&x=19&y=2
"""
req = s.get(search_url)

content = req.text
# print content
