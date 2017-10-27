# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from _md5 import md5

import happybase
import pymongo

from scrapy.conf import settings
import datetime
import random

from crawlAutohomedealer.items import dealerItem


class randomRowKey(object):
    # 生产唯一key
    def getRowKey(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

class HBasePipeline(object):
    def __init__(self):
        self.host = settings['HBASE_HOST']
        self.table_name = settings['HBASE_TABLE']
        self.port = settings['HBASE_PORT']
        # self.connection = happybase.Connection(host=self.host,port=self.port,, timeout=None, autoconnect=False,timeout=120000,transport='framed' protocol='compact')
        self.connection = happybase.Connection(host=self.host, port=self.port, autoconnect=False)
        # self.connection = happybase.Connection(host=self.host,port=self.port)
        # self.table = self.connection.table(self.table_name)




    def process_item(self, item, spider):
        # cl = dict(item)
        # self.connection = happybase.Connection(host=self.host, port=self.port, timeout=None, autoconnect=False)
        self.connection.open()
        table = self.connection.table(self.table_name)
        if isinstance(item, dealerItem):
            # self.table.put('text', cl)
            print('进入pipline')
            randomrkey = randomRowKey()
            rowkey = randomrkey.getRowKey()

            jsxid = item.get('jsxid', '')
            jxsurl = item.get('jxsurl', '')
            jxsname = item.get('jxsname', '')
            jxstype = item.get('jxstype', '')
            zyingpingpai = item.get('zyingpingpai', '')
            zaisaletype = item.get('zaisaletype', '')
            iphone = item.get('iphone', '')
            zaixian = item.get('zaixian', '')
            salefanwei = item.get('salefanwei', '')
            salefwcity = item.get('salefwcity', '')
            address = item.get('address', '')
            cuxiao = item.get('cuxiao', '')
            cuxiaourl = item.get('cuxiaourl', '')
            fromurl = item.get('fromurl', '')
            crawldate = item.get('crawldate', '')
            table.put(md5(str(rowkey).encode('utf-8')).hexdigest(), {
                'cf1:jsxid': jsxid,
                'cf1:jxsurl': jxsurl,
                'cf1:jxsname': jxsname,
                'cf1:jxstype': jxstype,
                'cf1:zyingpingpai': zyingpingpai,
                'cf1:zaisaletype': zaisaletype,
                'cf1:iphone': iphone,
                'cf1:zaixian': zaixian,
                'cf1:salefanwei': salefanwei,
                'cf1:salefwcity': salefwcity,
                'cf1:address': address,
                'cf1:cuxiao': cuxiao,
                'cf1:cuxiaourl': cuxiaourl,
                'cf1:fromurl': fromurl,
                'cf1:crawldate': crawldate
            })
        self.connection.close()
        return item
class CrawlautohomedealerPipeline(object):
    def process_item(self, item, spider):
        return item
