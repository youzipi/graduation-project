# coding=utf-8
import base64
import logging
import random

proxy_list = [
    {'ip_port': '111.206.190.156:80', 'user_pass': ''},
    {'ip_port': '123.124.168.107:80', 'user_pass': ''},
    {'ip_port': '1.195.125.132:80', 'user_pass': ''},


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
