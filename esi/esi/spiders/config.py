# encoding=utf8
import logging
from threading import Thread, Event

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
    # 'username': '20121344014',
    'password': '250036',
    # 'password': '293035',
    'realm': u'本专科生',
    'btnSubmit': u'登陆',
}


class MyThread(Thread):
    def __init__(self, function, interval=1):
        """

        :param event:
        :param timeout:
        :return:
        """
        Thread.__init__(self)
        if not callable(function):
            raise AssertionError("'{0}' is not an function!!".format(str(function)))
        else:
            self.func = function
        self.interval = interval
        self.stopped = Event()

    def run(self):
        while not self.stopped.wait(self.interval):
            self.func()

    def stop(self):
        self.stopped.set()



