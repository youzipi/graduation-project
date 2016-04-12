# coding=utf-8
import logging
import logging.handlers

import re
import requests
import scrapy
from scrapy.selector import Selector
from scrapy import Request, FormRequest, signals
from scrapy.signalmanager import SignalManager
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispatcher

from config import headers, login_form_data,MyThread
from ..settings import file_handler
from .mixin.logoutmixin import LogoutMixin
from ..items import EsiItem


logger = logging.getLogger('esi-spider')
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)




class EsiSpider(CrawlSpider, LogoutMixin):
# class EsiSpider(CrawlSpider):
    name = "esi"

    # allowed_domains = [""]
    # start_urls = ['https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi']
    start_urls = [
        'https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&option=G&searchby=F&search=COMPUTER%20SCIENCE&hothigh=G&x=1&y=7&currpage=1'
    ]

    logout_url = "https://vpn.nuist.edu.cn/dana-na/auth/logout.cgi"

    # rules = (
    #     Rule(LinkExtractor(allow=("/*",)), callback='parse'),
    # )

    def __init__(self, *a, **kw):
        super(EsiSpider, self).__init__(*a, **kw)
        LogoutMixin.__init__(self, logger)
        self.currpage = 1
        self.search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER%20SCIENCE&hothigh=G&option=G&x=19&y=2&currpage={currpage}"""

        dispatcher.connect(self._spider_opend, signals.spider_opened)
        #  todo spider_closed 好像是关闭后，才发送信号的，用于做一些善后处理，实质上是after_spider_closed 如果要对logout发起请求的话，cookie就不在了，没法正常退出
        # dispatcher.connect(self._spider_logout, signal=signals.spider_idle)

        self.logger.logger.addHandler(file_handler)
        self.logger.logger.setLevel(logging.DEBUG)

        self.thread = MyThread(self.keep_cookie,interval=5)


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
        self.thread.stop()
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
        logger.info(("after_login.cookies=", response.headers['Set-Cookie']))

        self.thread.start()

        for i in xrange(176):
            try:
                next_url = self.search_url.format(currpage=self.currpage)

                self.currpage += 1
                # next_url = self.search_url.format(currpage=self.currpage)
                logger.debug(('next_page', self.currpage))
                # logger.debug(('next_url', next_url))
                yield Request(next_url, callback=self.parse)
            except ValueError:
                logger.debug(('extra_url', response.url))

    def keep_cookie(self):
        print("keep_cookie")
        yield Request(
                    "https://vpn.nuist.edu.cn/dana/home/index.cgi",
                    callback=self.after_keep_cookie,
            )

    def after_keep_cookie(self, response):
        logger.info("keep_cookies=", response.headers['Set-Cookie'])

    def parse(self, response):
        logger.info(("parse.cookies=", response.headers['Set-Cookie']))
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
                wos_link = wos_links[i]
                wos_no = re.search("KeyUT=([\d]*)&", wos_link).group(1)
                citations = int(re.sub('[,|\t]', '', citations_list[i]))

                year_citations = year_citations_list[i]     # todo

                item = EsiItem()
                item['wos_link'] = wos_link
                item['wos_no'] = wos_no
                item['citations'] = citations

                # yield item

                yield Request(wos_link, callback=self.parse_wos_page, meta={'item': item})

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
    def parse_wos_page(self, response):
        logger.debug('===parse_wos_page===')
        logger.info(("parse_wos_page.cookies=", response.headers['Set-Cookie']))

        item = response.meta['item']
        content = response.body
        c = Selector(text=content)
        title = c.css('.NEWfullRecord > form[name=correction_form]>input[name="00N70000002BdnX"]::attr(value)').extract()
        # fields = c.css('.FR_field')
        # pulished = fields[5].css('value::text').extract()
        # abstract = fields[9].css('::text').extract()

        pub_years = c.css('.NEWfullRecord > form[name=correction_form]>input[name="00N70000002BdnY"]::attr(value)').extract()
        publisheds = c.xpath('//span[contains(@class,"FR_label") and contains(text(),"Published")]/../value/text()').extract()
        abstracts = c.xpath('//div[contains(@class,"title3") and contains(text(),"Abstract")]/../p/text()').extract()
        keywords = c.xpath('//span[contains(@class,"FR_label") and contains(text(),"KeyWords")]/../a/text()').extract()

        research_areas =c.xpath('//span[contains(@class,"FR_label") and contains(text(),"Research Areas")]/../text()').extract()
        research_areas = list_get(research_areas, 1)

        # if research_areas is None:
        #     yield FormRequest(
        #             "https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi",
        #             formdata=login_form_data,
        #             callback=self.re_login,
        #             meta={'url': response.url,'item':item}
        #     )

        if len(research_areas) > 0:
            research_areas = research_areas.split(';')

        title = list_get(title)
        pub_year = int(list_get(pub_years))
        published = list_get(publisheds)
        abstract = list_get(abstracts)
        abstract = list2str(abstracts)
        #
        item['title'] = title
        item['pulished'] = published
        item['abstract'] = abstract
        item['pub_year'] = pub_year
        item['keywords'] = keywords
        item['research_areas'] = research_areas
        yield item
        # wos_links = c.xpath('//td/a/img[contains(@src, "gotowos.gif")]/../@href').extract()
        # citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../text()[2]').extract()
        # year_citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../a/@href').extract()


def list_get(l, i=0):
    try:
        return l[i]
    except IndexError:
        return None


def list2str(l):
    if isinstance(l, list):
        s = ""
        for i in l:
            s += i
        return s
    else:
        return ""
