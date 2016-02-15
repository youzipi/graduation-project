# coding=utf-8
import requests
import scrapy
from scrapy.selector import Selector

from config import headers, login_form_data
from esi.esi.items import EsiItem


class EsiSpider(scrapy.Spider):
    name = "esi"

    # allowed_domains = [""]
    # start_urls = []

    def start_requests(self):
        s = requests.session()

        post_req = s.post('https://vpn.nuist.edu.cn/dana-na/auth/url_default/login.cgi',
                          headers=headers,
                          data=login_form_data)
        post_req.encoding = 'utf8'

        search_url = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search={search}&hothigh=G&option=G&x=19&y=2&currpage={currpage}
""".format(search='COMPUTER+SCIENCE', currpage=1)

        return s.get(search_url)

    def parse(self, response):
        """
        <a href="https://vpn.nuist.edu.cn/gateway/,DanaInfo=.agbvh0f4G4nlzrx13A2ww0zVzA.+Gateway.cgi?&amp;GWVersion=2&amp;SrcAuth=ESI&amp;SrcApp=ESI&amp;DestLinkType=FullRecord&amp;DestApp=WOS&amp;SrcAppSID=T24LUnOT9HuPw5EtTxm&amp;SrcDesc=RETURN_ALT_TEXT&amp;SrcURL=http%3A//esi.webofknowledge.com/paperpage.cgi%3Foption%3DG%26option%3DG%26searchby%3DF%26search%3DCOMPUTER%2520SCIENCE%26hothigh%3DG%26x%3D19%26y%3D2&amp;KeyUT=000226308500016&amp;SrcImageURL=">
            <img src="../images/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+gotowos.gif">
        </a>
        """
        content = response.text
        c = Selector(text=content)

        # /html/body/table[4]/tbody/tr[3]/td/table[2]/tbody/tr/td[2]/a/img

        target_url = c.xpath('/html/body/table[4]/tr[3]/td/table/table[3]/tr/td[2]/a/@href')
        print target_url.extract()[0]
        urls = c.xpath('//td[2]/a/img[contains(@src, "gotowos.gif")]/../@href')
        print urls.extract()
        # len(urls) # 20= 一页的记录数
        item = EsiItem()
        yield item
