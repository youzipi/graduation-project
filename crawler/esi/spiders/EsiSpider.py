# coding=utf-8
import logging
import logging.handlers

import re

import pymongo
import requests
import scrapy
from scrapy.selector import Selector
from scrapy import Request, FormRequest, signals
from scrapy.signalmanager import SignalManager
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher

from config import headers, login_form_data, MyThread
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

    base_url = "https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+"

    # rules = (
    #     Rule(LinkExtractor(allow=("/*",)), callback='parse'),
    # )

    def __init__(self, *a, **kw):

        settings = get_project_settings()
        super(EsiSpider, self).__init__(*a, **kw)
        LogoutMixin.__init__(self, logger)
        self.currpage = 1
        self.search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search=COMPUTER%20SCIENCE&hothigh=G&option=G&x=19&y=2&currpage={currpage}"""

        dispatcher.connect(self._spider_opend, signals.spider_opened)
        #  todo spider_closed 好像是关闭后，才发送信号的，用于做一些善后处理，实质上是after_spider_closed 如果要对logout发起请求的话，cookie就不在了，没法正常退出
        # dispatcher.connect(self._spider_logout, signal=signals.spider_idle)

        self.logger.logger.addHandler(file_handler)
        self.logger.logger.setLevel(logging.DEBUG)

        self.thread = MyThread(self.keep_cookie, interval=60)

        connection = pymongo.MongoClient(
            settings['MONGO_HOST'],
            settings['MONGO_PORT']
        )
        db = connection[settings['MONGO_DBNAME']]
        self.post = db[settings['MONGO_DOCNAME']]

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
        logger.info(("after_login.cookies=", response.headers.get('Set-Cookie')))

        self.thread.start()

        for i in xrange(176):
            #176 pages
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
        # logger.info(("parse.cookies=", response.headers['Set-Cookie']))
        """
        <a href="https://vpn.nuist.edu.cn/gateway/,DanaInfo=.agbvh0f4G4nlzrx13A2ww0zVzA.+Gateway.cgi?&amp;GWVersion=2&amp;SrcAuth=ESI&amp;SrcApp=ESI&amp;DestLinkType=FullRecord&amp;DestApp=WOS&amp;SrcAppSID=T24LUnOT9HuPw5EtTxm&amp;SrcDesc=RETURN_ALT_TEXT&amp;SrcURL=http%3A//esi.webofknowledge.com/paperpage.cgi%3Foption%3DG%26option%3DG%26searchby%3DF%26search%3DCOMPUTER%2520SCIENCE%26hothigh%3DG%26x%3D19%26y%3D2&amp;KeyUT=000226308500016&amp;SrcImageURL=">
            <img src="../images/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+gotowos.gif">
        </a>
        :param response:
        """

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
        citations_list = c.xpath(
            '/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../text()[2]').extract()

        # year_citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../a/@href').extract()

        length = len(wos_links)
        # logger.debug(("wos_links=", wos_links))
        # logger.debug(("len(wos_links)=", length))

        if length > 0:
            # if target_url.size > 0:
            for i in range(length):
                wos_link = wos_links[i]
                logger.debug("parse proxy=%s",response.meta['proxy'])
                wos_no = re.search("KeyUT=([\d]*)&", wos_link).group(1)
                citations = int(re.sub('[,|\t]', '', citations_list[i]))

                # year_citations_link = year_citations_list[i]     # todo

                """
                Number of Citations (by year) 最短url
                from=paperpage
                articleid=`wos_no`
                """
                year_citations_link = self.base_url + 'tabulargraphdata.cgi?from=paperpage&articleid=' + wos_no

                item = EsiItem()
                item['wos_link'] = wos_link
                item['wos_no'] = wos_no
                item['citations'] = citations

                # if self.post.find({'wos_no': wos_no}).count() > 0:
                #     yield item
                # else:
                # yield Request(wos_link, callback=self.parse_wos_page, meta={'item': item})

                if self.post.find({'wos_no': wos_no}).count() == 0: #  该论文不存在
                    # yield Request(wos_link, callback=self.parse_wos_page, meta={'item': item})

                    yield Request(year_citations_link, callback=self.parse_year_citations, meta={'item': item})
                else:
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

    def parse_wos_page(self, response):
        logger.debug('===parse_wos_page===')
        # logger.info(("parse_wos_page.cookies=", response.headers['Set-Cookie']))
        logger.debug("parse_wos_page proxy=%s", response.meta['proxy'])

        item = response.meta['item']

        logger.info(("wos_no=", item['wos_no']))

        content = response.body
        c = Selector(text=content)
        title = c.css(
            '.NEWfullRecord > form[name=correction_form]>input[name="00N70000002BdnX"]::attr(value)').extract()
        pub_years = c.css(
            '.NEWfullRecord > form[name=correction_form]>input[name="00N70000002BdnY"]::attr(value)').extract()
        journal = c.css(
            '.NEWfullRecord > form[name=correction_form]>input[name="00N70000002C0wf"]::attr(value)').extract()


        publisheds = c.xpath(
            '//span[contains(@class,"FR_label") and contains(text(),"Published")]/../value/text()').extract()
        abstracts = c.xpath('//div[contains(@class,"title3") and contains(text(),"Abstract")]/../p/text()').extract()
        keywords = c.xpath('//span[contains(@class,"FR_label") and contains(text(),"KeyWords")]/../a/text()').extract()

        research_areas = c.xpath(
            '//span[contains(@class,"FR_label") and contains(text(),"Research Areas")]/../text()').extract()
        research_areas = list_get(research_areas, 1)

        # authors = c.xpath('//span[contains(@class,"FR_label") and contains(text(),"By")]/../a/text()').extract()
        authors = c.xpath('//span[contains(@class,"FR_label") and contains(text(),"By")]/..//a[@title]/text()').extract()


        addresses = c.xpath('//*[@class="fr_address_row2"]/a/text()').extract()     # List(str)

        cleaned_addresses = map(lambda x: re.sub('\[ \d \] ', '', x), addresses)

        # address.split(',')[0]
        # address.split(',')[-1]
        # if research_areas is None:
        #     yield FormRequest(
        #             "https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi",
        #             formdata=login_form_data,
        #             callback=self.re_login,
        #             meta={'url': response.url,'item':item}
        #     )

        if len(research_areas) > 0:
            research_areas = research_areas.split(';')

        cleaned_title = list_get(title)
        cleaned_pub_year = int(list_get(pub_years))
        cleaned_journal = list_get(journal)
        cleaned_published = list_get(publisheds)
        # authors = list_get(authors)

        abstract = list2str(abstracts)
        # 去除两边的空白
        cleaned_abstract = abstract.strip()
        cleaned_keywords = map(lambda x: x.strip(), keywords)
        cleaned_research_areas = map(lambda x: x.strip(), research_areas)
        #
        item['title'] = cleaned_title
        item['authors'] = authors

        item['journal'] = cleaned_journal
        item['addresses'] = cleaned_addresses
        item['pulished'] = cleaned_published
        item['abstract'] = cleaned_abstract
        item['pub_year'] = cleaned_pub_year

        item['keywords'] = cleaned_keywords
        item['research_areas'] = cleaned_research_areas

        return item
        # wos_links = c.xpath('//td/a/img[contains(@src, "gotowos.gif")]/../@href').extract()
        # citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../text()[2]').extract()
        # year_citations_list = c.xpath('/html/body/table[4]//td//tr/td[1]/b[contains(text(),"Citations")]/../a/@href').extract()

    def parse_year_citations(self, response):
        logger.debug("parse_year_citations proxy=%s",response.meta['proxy'])

        item = dict()
        item = response.meta['item']
        content = response.body
        c = Selector(text=content)
        year_citations = c.xpath('/html/body/table[5]/tr[2]/td/center/table/tr[2]/td/text()').extract()  # type: list

        _year_citations = {}

        cur_year = 2016
        start_year = 2005  # todo 不知道

        years = cur_year - start_year

        for i in range(years):
            _year_citations.update({str(start_year + i): int(list_get(year_citations, i).strip())})

        item['year_citations'] = _year_citations

        yield Request(item['wos_link'], callback=self.parse_wos_page, meta={'item': item})

        # return item


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
