# coding=utf-8
import base64
import logging
import random

proxy_list = [
    {'ip_port': '183.38.4.13:9000', 'user_pass': ''},
    {'ip_port': '61.162.223.41:9797', 'user_pass': ''},
    {'ip_port': '124.206.133.227:80', 'user_pass': ''},


]

__author__ = 'youzipi'

logger = logging.getLogger()


class ProxyMiddleware(object):
    """
    使用代理
    """

    def process_request(self, request, spider):
        proxy = random.choice(proxy_list)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
