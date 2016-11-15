# coding=utf-8
import base64
import logging
import random

# https 代理IP
# http://www.xicidaili.com/nt/3
proxy_list = [
    {'ip_port': '111.206.190.155:80', 'user_pass': ''},
    {'ip_port': '111.206.190.156:80', 'user_pass': ''},
    {'ip_port': '222.45.196.46:8118', 'user_pass': ''},
    {'ip_port': '210.33.29.31:9000', 'user_pass': ''},

    {'ip_port': '124.202.180.6:8118', 'user_pass': ''},
    {'ip_port': '123.124.168.107:80', 'user_pass': ''},

    # HTTPS
    # {'ip_port': '123.124.168.149:80', 'user_pass': ''},
    # {'ip_port': '218.241.167.190:3128', 'user_pass': ''},
    # {'ip_port': '59.44.152.110:9999', 'user_pass': ''},

]

__author__ = 'youzipi'

logger = logging.getLogger()


class ProxyMiddleware(object):
    """
    代理IP
    """

    def process_request(self, request, spider):
        proxy = random.choice(proxy_list)

        if 'login' in request.url:
            pass
        else:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']




            # http://www.xicidaili.com/nt/
            # //*[@id="ip_list"]//tr[./td[6]/text() = 'HTTPS' and ./td[7]/div/div[@class='bar_inner fast'] and ./td[8]/div/div[@class='bar_inner fast']]
            #  HTTPS and 速度=fast,连接时间=fast
