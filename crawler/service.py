import os

from tornado import gen

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'esi.settings')  # Must be at the top before other imports

from scrapy import cmdline
from scrapy.utils.project import get_project_settings
from esi.spiders.EsiSpider import EsiSpider
from scrapy.crawler import CrawlerProcess


@gen.coroutine
def start():
    # cmdline.execute("scrapy crawl esi".split())
    _settings = get_project_settings()

    process = CrawlerProcess(_settings)

    process.crawl(EsiSpider)

    process.start()
