# -*- coding: utf-8 -*-
import datetime

import scrapy
from bs4 import BeautifulSoup

from crawlAutohomedealer.items import dealerItem


class SpiderdealerSpider(scrapy.Spider):
    name = 'spiderdealer'
    allowed_domains = ['dealer.autohome.com.cn']
    # start_urls = ['https://dealer.autohome.com.cn/china?_abtest=1']
    start_urls = ['https://dealer.autohome.com.cn/china?pageIndex=1&_abtest=1']

    baseurl='https://dealer.autohome.com.cn/china?pageIndex={pageindex}&_abtest=1'


    def __init__(self, **kwargs):
        self.count=0

    def start_requests(self):
        for url in self.start_urls:
            request= scrapy.Request(url=url, callback=self.parse)
            # request= scrapy.Request(url=url, callback=self.parse)
            request.meta['isjs']='True'
            # request.meta['isjs']='False'
            yield  request

    def parse(self, response):
        boxlist = response.css('.list-box')
        itemlist=boxlist.css('.list-item')


        # for it in itemlist:
        #     print('it=',it.css(''))
        soup= BeautifulSoup(response.text,'lxml')

        listbox=soup.find('ul',class_='list-box')

        itemlists = listbox.findAll('li', class_='list-item')
        print('itemlists-length=',len(itemlists))

        for it in itemlists:
            ul = it.find('ul', class_='info-wrap').findAll('li')
            print('len(ul)=', len(ul))
            jxsurl= it.find('ul', class_='info-wrap').find('a',class_='link').attrs['href']
            print('jxsurl=', response.urljoin(jxsurl))
            # jxsname =ul[0].find('a',class_='link').find('span').get_text(strip=True)
            # jxstype =ul[0].find()
            jxsnameTag = ul[0].get_text(separator='&', strip=True)
            #经销商
            jxsname = jxsnameTag.split('&')[0]
            #经销商类型
            jxstype = jxsnameTag.split('&')[1]

            zhuying = ul[1].get_text(separator='&', strip=True)
            #主营品牌
            zys = zhuying.split('&')
            zyingpingpai=zys[1]
            #在售车型
            zaisaletype=zys[2]
            #联系方式

            lianxitag = ul[2].get_text(separator='&', strip=True)
            print('lianxitag=',lianxitag)
            lianxis=lianxitag.split('&')
            #电话
            iphone=lianxis[2]
            if len(lianxis)==6:
                #24小时
                zaixian=lianxis[3]
                #销售范围
                salefanwei=lianxis[4]
                #销售城市
                salefwcity=lianxis[5]
            else:
                # 24小时
                zaixian = ''
                # 销售范围
                salefanwei = lianxis[3]
                # 销售城市
                salefwcity = lianxis[4]
            #地址
            addrtag = ul[3].get_text(separator='&', strip=True)
            address=addrtag.split('&')[2]

            if len(ul)==5:
                # 促销活动
                cuxiaotag = ul[4].get_text(separator='&', strip=True)
                cuxiao=cuxiaotag.split('&')[2]

                xurl=ul[4].find('a',class_='link').attrs['href']
                cuxiaourl=response.urljoin(xurl)
            else:
                cuxiao =''
                cuxiaourl=''

            fromurl=response.url
            jsxid=jxsurl[jxsurl.find('cn/')+3:jxsurl.find('/#')]

            crawldate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # print('jsxid',jsxid)
            # print('jxsurl:', response.urljoin(jxsurl))
            # print('jxsname:', jxsname)
            # print('jxstype:', jxstype)
            # print('zyingpingpai:', zyingpingpai)
            # print('zaisaletype:', zaisaletype)
            # print('iphone:', iphone)
            # print('zaixian:', zaixian)
            # print('salefanwei:', salefanwei)
            # print('salefwcity:', salefwcity)
            # print('address=', address)
            # print('cuxiao=', cuxiao)
            # print('cuxiaourl=', cuxiaourl)
            # print('fromurl=', fromurl)

            item=dealerItem()
            item['jsxid'] = jsxid
            item['jxsurl'] = jxsurl
            item['jxsname'] = jxsname
            item['jxstype'] = jxstype
            item['zyingpingpai'] = zyingpingpai
            item['zaisaletype'] = zaisaletype
            item['iphone'] = iphone
            item['zaixian'] = zaixian
            item['salefanwei'] = salefanwei
            item['salefwcity'] = salefwcity
            item['address'] = address
            item['cuxiao'] = cuxiao
            item['cuxiaourl'] = cuxiaourl
            item['fromurl'] = fromurl
            item['crawldate'] = crawldate

            yield item
        pagediv= soup.find('div',class_='pagination-wrap').find('div',class_='pagination')
        pagetag= totalpages = pagediv.findAll('a')
        totalpages = pagetag[len(pagetag)-2].get_text(strip=True)
        print('totalpages=',totalpages)

        # if len(totalpages) >= 2:
        for num in range(2,int(totalpages)+1):
            print('页数：',num)
            url = self.baseurl.replace('{pageindex}', str(num))
            request= scrapy.Request(url=url, callback=self.parse)
            request.meta['isjs']='True'
            yield  request

    def jxsparse(self,response):
        soup=BeautifulSoup(response.text,'lxml')
        cont=soup.find('div',class_='allagency-cont')
        tellv=cont.find('div',class_='telphone').get_text(strip=True)




#body > div.dealer-list-container.cont-width > div.dealer-list-wrap > ul > li:nth-child(1) > ul > li.tit-row > a > span




