# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class dealerItem(scrapy.Item):
    jsxid = scrapy.Field()
    jxsurl = scrapy.Field()
    jxsname = scrapy.Field()
    jxstype = scrapy.Field()
    zyingpingpai = scrapy.Field()
    zaisaletype = scrapy.Field()
    iphone = scrapy.Field()
    zaixian = scrapy.Field()
    salefanwei = scrapy.Field()
    salefwcity = scrapy.Field()
    address = scrapy.Field()
    cuxiao = scrapy.Field()
    cuxiaourl = scrapy.Field()
    fromurl = scrapy.Field()
    crawldate = scrapy.Field()
class CrawlautohomedealerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
