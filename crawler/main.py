import logging

from scrapy import cmdline, signals

# settings = cmdline.get_project_settings()
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

# cmdline.execute("scrapy crawl esi".split())
from esi.spiders.EsiSpider import EsiSpider

logger = logging.getLogger('root')
from scrapy.crawler import CrawlerProcess

_settings = get_project_settings()

process = CrawlerProcess(_settings)

process.crawl(EsiSpider)
process.start()
