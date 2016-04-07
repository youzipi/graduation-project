# coding=utf-8
import logging

import re
import requests
import scrapy
from scrapy.selector import Selector
from scrapy import Request, FormRequest, signals
from scrapy.signalmanager import SignalManager
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispatcher

from config import headers, login_form_data
from .mixin.logoutmixin import LogoutMixin
from ..items import EsiItem

logger = logging.getLogger('esi-spider')




class EsiSpider(CrawlSpider, LogoutMixin):
# class EsiSpider(CrawlSpider):
    name = "esi"

    # allowed_domains = [""]
    # start_urls = ['https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi']
    start_urls = [
        'https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&option=G&searchby=F&search=COMPUTER%20SCIENCE&hothigh=G&x=1&y=7&currpage=1'
    ]

    logout_url = "https://vpn.nuist.edu.cn/dana-na/auth/logout.cgi"

    rules = (
        Rule(LinkExtractor(allow=("/*",)), callback='parse'),
    )

    def __init__(self, *a, **kw):
        super(EsiSpider, self).__init__(*a, **kw)
        LogoutMixin.__init__(self, logger)
        self.currpage = 1
        self.search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER%20SCIENCE&hothigh=G&option=G&x=19&y=2&currpage={currpage}"""

        dispatcher.connect(self._spider_opend, signals.spider_opened)
        #  todo spider_closed 好像是关闭后，才发送信号的，用于做一些善后处理，实质上是after_spider_closed 如果要对logout发起请求的话，cookie就不在了，没法正常退出
        # dispatcher.connect(self._spider_logout, signal=signals.spider_idle)

    # def start_requests(self):
    # s = requests.session()

    #  post_req = s.post('https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi',
    # headers = headers,
    # data = login_form_data)
    # post_req.encoding = 'utf8'

    # sc_resp = FormRequest(url='https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi',  # method="POST",
    #                     headers=headers,
    #                    formdata=login_form_data)

    # search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search={search}&hothigh=G&option=G&x=19&y=2&currpage={currpage}
    # """.format(search='COMPUTER+SCIENCE', currpage=1)

    # return [Request(url=search_url, headers=headers, cookies=sc_resp.cookies)]

    # return [s.get(search_url)]
    # return [scrapy.FormRequest]

    def _spider_opend(self):
        logger.debug("+++++++spider_opened++++")

    def after_logout(self, response):
        logger.debug("=====after_logout=====")

    def logout(self):
        logger.debug("=====logout=====")
        return super(EsiSpider, self).logout()
        # yield Request("https://vpn.nuist.edu.cn/dana-na/auth/logout.cgi", callback=self.after_logout)

    def start_requests(self):
        return [
            FormRequest(
                    "https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi",
                    formdata=login_form_data,
                    callback=self.after_login
            )
        ]

    def after_login(self, response):
        # for url in self.start_urls:
        # yield self.make_requests_from_url(url)
        # yield self.make_requests_from_url(self.search_url.format(currpage=self.currpage))

        # logger.debug(("cookies", response.request.cookies))  # todo get cookie
        for i in xrange(5):
            try:
                next_url = self.search_url.format(currpage=self.currpage)

                self.currpage += 1
                # next_url = self.search_url.format(currpage=self.currpage)
                logger.debug(('next_page', self.currpage))
                # logger.debug(('next_url', next_url))
                yield Request(next_url, callback=self.parse)
            except ValueError:
                logger.debug(('extra_url', response.url))

    def parse(self, response):
        """
        <a href="https://vpn.nuist.edu.cn/gateway/,DanaInfo=.agbvh0f4G4nlzrx13A2ww0zVzA.+Gateway.cgi?&amp;GWVersion=2&amp;SrcAuth=ESI&amp;SrcApp=ESI&amp;DestLinkType=FullRecord&amp;DestApp=WOS&amp;SrcAppSID=T24LUnOT9HuPw5EtTxm&amp;SrcDesc=RETURN_ALT_TEXT&amp;SrcURL=http%3A//esi.webofknowledge.com/paperpage.cgi%3Foption%3DG%26option%3DG%26searchby%3DF%26search%3DCOMPUTER%2520SCIENCE%26hothigh%3DG%26x%3D19%26y%3D2&amp;KeyUT=000226308500016&amp;SrcImageURL=">
            <img src="../images/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+gotowos.gif">
        </a>
        :param response:
        """

        # logger.debug(response.cookie)
        # s = requests.session()

        # login_resp = s.post('https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi',
        #                     headers=headers,
        #                     data=login_form_data)
        # login_resp.encoding = 'utf8'
        # logger.debug("cookie=", login_resp.cookies.get_dict())
        # print "cookie=", login_resp.cookies.get_dict()

        # print response
        # for i in xrange(1):
        #     search_url = """
        #     https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER+SCIENCE&hothigh=G&option=G&x=8&y=5"""
        #
        #     rq_resp = s.get(search_url)
        #
        #     content = rq_resp.text
        content = response.body
        c = Selector(text=content)
        #
        #     # /html/body/table[4]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/a/img
        # target_url = c.xpath('/html/body/table[4]/tr[3]/td/table/table[3]/tr/td[2]/a/@href')

        # target_urls = c.xpath('/html/body/table[4]/tr[3]/td/table/table[position() mod 2 = 1]/tr/td[2]/a/@href')
        # target_urls_extract = target_urls.extract()
        # wos_links = [u for u in target_urls_extract if "KeyUT" in u]
        # chrome
        # /html/body/table[4]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/a
        # /html/body/table[4]/tbody/tr[3]/td/table[4]/tbody/tr/td[2]/a
        # /html/body/table[4]/tbody/tr[3]/td/table[6]/tbody/tr/td[2]/a
        # target_url = c.xpath('/html/body/table[4]/tr[3]/td/table/table[3]/tr/td[2]/a/@href')
        # target_urls = c.xpath('//td[2]/a/img[contains(@src, "gotowos.gif")]/../@href') chrome

        # td = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/..')
        # citations_list  = td.xpath('./text()[2]')

        wos_links = c.xpath('//td/a/img[contains(@src, "gotowos.gif")]/../@href').extract()
        citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../text()[2]').extract()
        year_citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../a/@href').extract()

        length = len(wos_links)

        # logger.debug(("wos_links=", wos_links))
        logger.debug(("len(wos_links)=", length))

        if length > 0:
            # if target_url.size > 0:
            for i in range(length):
                wos_no = re.search("KeyUT=([\d]*)&", wos_links[i]).group(1)
                citations = int(re.sub('[,|\t]', '', citations_list[i]))

                year_citations = year_citations_list[i]

                item = EsiItem()
                item['wos_link'] = wos_links[i]
                item['wos_no'] = wos_no
                item['citations'] = citations

                yield item
        elif length == 0:
            pass
            # if self.currpage >= 10:
            # yield Request("https://vpn.nuist.edu.cn/dana-na/auth/logout.cgi", callback=self.after_logout)
            # return

            # try:
            #     self.currpage += 1
            #
            #     next_url = self.search_url.format(currpage=self.currpage)
            #     logger.debug(('next_page', self.currpage))
            #     # logger.debug(('next_url', next_url))
            #     yield Request(next_url, callback=self.parse)
            # except ValueError:
            #     logger.debug(('extra_url', response.url))
