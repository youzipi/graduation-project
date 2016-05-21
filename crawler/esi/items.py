# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy import Item, Field


class EsiItem(Item):
    # define the fields for your item here like:
    # name = Field()
    wos_link = Field()
    wos_no = Field()

    citations = Field()

    title = Field()
    journal = Field()
    authors = Field()
    addresses = Field()
    abstract = Field()
    keywords = Field()

    pulished = Field()
    pub_year = Field()

    year_citations = Field()

    # Categories / Classification
    research_areas = Field()
    WOS_categories = Field()

    # citation network
    cited_times = Field()
    cited_references = Field()
