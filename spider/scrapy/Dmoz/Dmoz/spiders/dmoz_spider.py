#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-11 09:42:12
# @Author  : mannyxu (beilixumeng@163.com)

import scrapy

class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['domz.org']
    start_urls = ["http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
    "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"]

    def parse(self,response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print(title, link, desc)