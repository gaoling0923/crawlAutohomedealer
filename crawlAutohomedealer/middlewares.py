# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import time

from scrapy import signals
from scrapy.conf import settings
import random
# from crawAutohomebbsdetail.dbpackage.dbresdis import RedisClient
from selenium.webdriver.common.proxy import ProxyType

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class IsJavaScriptMiddleware(object):

    # def __init__(self):
    #     self.browser = webdriver.PhantomJS()

    def process_request(self, request, spider):
        # conn = RedisClient();
        # proxy = conn.pop();
        # print('当前使用的IP:', proxy);
        # request.meta['proxy'] = "http://%s" % proxy
        # if spider.name in("spiderbbsdetail","crawlb30bbsdetail"):
        isjs = request.meta['isjs']
        print('isjs=', isjs)
        if isjs == 'True':
            print("execute PhantomJS spiderName", spider.name);
            print("PhantomJS is starting...")
            browser = webdriver.PhantomJS() #指定使用的浏览器
            # browser = webdriver.Chrome()
            # driver = webdriver.Firefox()
            # time.sleep(1)
            # driver.implicitly_wait(30)  # seconds
            # wait = WebDriverWait(driver, 60)
            browser.get(request.url)
            print("访问:" + request.url)
            # 等待完成

            body = browser.page_source

            response = HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
            # soup = BeautifulSoup(response.text, 'lxml')
            # return HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
            browser.close()
            return response
        else:
            # print('')
            return
class CrawlautohomedealerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
