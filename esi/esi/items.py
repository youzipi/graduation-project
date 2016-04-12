# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EsiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    wos_link = scrapy.Field()
    wos_no = scrapy.Field()

    citations = scrapy.Field()

    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()

    pulished = scrapy.Field()
    pub_year = scrapy.Field()

    # Categories / Classification
    research_areas = scrapy.Field()
    WOS_categories = scrapy.Field()

    # citation network
    cited_times = scrapy.Field()
    cited_references = scrapy.Field()
