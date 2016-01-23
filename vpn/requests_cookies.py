# coding=utf-8
import requests

form_data = {
    'tz_offset': '480',
    'username': '20121344018',
    'password': '250036',
    'realm': u'本专科生',
    'btnSubmit': u'登陆',
}

r = requests.post(url="https://vpn.nuist.edu.cn/dana/home/index.cgi", data=form_data)
print(r.cookies.items())
for cookie in r.cookies:
    print cookie
