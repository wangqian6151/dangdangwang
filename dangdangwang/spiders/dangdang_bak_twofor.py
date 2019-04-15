# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from dangdangwang.items import DangdangBookItem


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.00.00.00.00.00.html']

    base_url = 'http://category.dangdang.com'
    # custom_settings = {
    #     'LOG_FILE': 'log_医学.txt',
    # }

    def parse(self, response):
        print('1' * 20)
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        # first_category_name_list = response.css('li[dd_name="分类"] .list_right > .list_content > div span a::text').extract()[-2::-1]
        first_category_name_dict = dict()

        le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="分类"]/div[2]/div[1]/div')
        for link in le.extract_links(response):
            print(link.url, link.text)
            self.logger.debug('first_category {}，{}'.format(link.url, link.text))
            first_category = link.text
        #     first_category_name_dict.update({link.text:link.url})
        # for text, url in first_category_name_dict.items():
        #     if text != '其他':
        #         first_category = text
        #         print('现在爬取的一级分类是：{}'.format(text))
        #         self.logger.debug('现在爬取的一级分类是：{}'.format(text))
        #         yield Request(url, callback=self.parse_second, meta={'first_category': first_category})

            yield Request(link.url, callback=self.parse_second, meta={'first_category': first_category})

    def parse_second(self, response):
        print('2' * 20)
        first_category = response.meta.get('first_category')
        print('parse_second response.url:' + response.url)
        self.logger.debug('parse_second response.url:' + response.url)
        second_category = third_category = forth_category = ''
        max_page = response.xpath('//*[@dd_name="底部翻页"]/li[last()-2]/a/text()').extract_first()
        max_page = int(max_page) if max_page else 1

        # if response.xpath('//*[@id="navigation"]/ul/li[1]/div[1]/text()').extract_first() == '分类':
        if '分类' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
            le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="分类"]/div[2]/div[1]/div')
            for link in le.extract_links(response):
                print(link.url, link.text)
                self.logger.debug('second_category {}，{}'.format(link.url, link.text))
                second_category = link.text
                yield Request(link.url, callback=self.parse_third,
                              meta={'first_category': first_category, 'second_category': second_category})
        else:
            if max_page < 100 and '价格' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
                le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="价格"]/div[2]/div[1]/div')
                for link in le.extract_links(response):
                    print(link.url, link.text)
                    yield Request(link.url, callback=self.parse_books,
                                  meta={'first_category': first_category, 'second_category': second_category,
                                        'third_category': third_category, 'forth_category': forth_category})
            else:
                print('第二层的全部爬取url：{}'.format(response.url))
                self.logger.debug('第二层的全部爬取url：{}'.format(response.url))
                le = LinkExtractor(restrict_css='.filtrate_list')
                for link in le.extract_links(response):
                    print('parse_second else url:{},text{}'.format(link.url, link.text))
                    self.logger.debug('parse_second else url:{},text{}'.format(link.url, link.text))
                    yield Request(link.url, callback=self.parse_books,
                                  meta={'first_category': first_category, 'second_category': second_category,
                                        'third_category': third_category, 'forth_category': forth_category})

    def parse_third(self, response):
        print('3' * 20)
        first_category = response.meta.get('first_category')
        second_category = response.meta.get('second_category')
        print('parse_third response.url:' + response.url)
        self.logger.debug('parse_third response.url:' + response.url)
        third_category = forth_category = ''
        max_page = response.xpath('//*[@dd_name="底部翻页"]/li[last()-2]/a/text()').extract_first()
        max_page = int(max_page) if max_page else 1

        # if response.xpath('//*[@id="navigation"]/ul/li[1]/div[1]/text()').extract_first() == '分类':
        if '分类' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
            print('parse_third 33333333 == 分类 response.url:{}' + response.url)
            self.logger.debug('parse_third 3333333 == 分类 response.url:' + response.url)
            le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="分类"]/div[2]/div[1]/div')
            for link in le.extract_links(response):
                print(link.url, link.text)
                self.logger.debug('third_category {}，{}'.format(link.url, link.text))
                third_category = link.text
                yield Request(link.url, callback=self.parse_forth,
                              meta={'first_category': first_category, 'second_category': second_category,
                                    'third_category': third_category})
        else:
            if max_page < 100 and '价格' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
                le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="价格"]/div[2]/div[1]/div')
                for link in le.extract_links(response):
                    print(link.url, link.text)
                    yield Request(link.url, callback=self.parse_books,
                                  meta={'first_category': first_category, 'second_category': second_category,
                                        'third_category': third_category, 'forth_category': forth_category})
            else:
                print('第三层的全部爬取url：{}'.format(response.url))
                self.logger.debug('第三层的全部爬取url：{}'.format(response.url))
                le = LinkExtractor(restrict_css='.filtrate_list')
                for link in le.extract_links(response):
                    print('parse_second else url:{},text{}'.format(link.url, link.text))
                    self.logger.debug('parse_second else url:{},text{}'.format(link.url, link.text))
                    yield Request(link.url, callback=self.parse_books,
                                  meta={'first_category': first_category, 'second_category': second_category,
                                        'third_category': third_category, 'forth_category': forth_category})


    def parse_forth(self, response):
        print('4' * 20)
        first_category = response.meta.get('first_category')
        second_category = response.meta.get('second_category')
        third_category = response.meta.get('third_category')
        forth_category = ''
        max_page = response.xpath('//*[@dd_name="底部翻页"]/li[last()-2]/a/text()').extract_first()
        max_page = int(max_page) if max_page else 1
        print('parse_fifth max_page:{} response.url:{}'.format(max_page, response.url))
        self.logger.debug('parse_fifth max_page:{} response.url:{}'.format(max_page, response.url))

        # if response.xpath('//*[@id="navigation"]/ul/li[1]/div[1]/text()').extract_first() == '分类':
        if '分类' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
            print('parse_forth 444444 == 分类 response.url:{}'.format(response.url))
            self.logger.debug('parse_forth 444444 == 分类 response.url:{}'.format(response.url))
            le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="分类"]/div[2]/div[1]/div')
            for link in le.extract_links(response):
                print(link.url, link.text)
                self.logger.debug('parse_forth == 分类{}，{}'.format(link.url, link.text))
                forth_category = link.text
                yield Request(link.url, callback=self.parse_fifth,
                              meta={'first_category': first_category, 'second_category': second_category,
                                    'third_category': third_category, 'forth_category': forth_category})
        else:
            if max_page < 100 and '价格' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
                le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="价格"]/div[2]/div[1]/div')
                for link in le.extract_links(response):
                    print(link.url, link.text)
                    yield Request(link.url, callback=self.parse_books,
                                  meta={'first_category': first_category, 'second_category': second_category,
                                        'third_category': third_category, 'forth_category': forth_category})
            else:
                print('第四层的全部爬取url：{}'.format(response.url))
                self.logger.debug('第四层的全部爬取url：{}'.format(response.url))
                le = LinkExtractor(restrict_css='.filtrate_list')
                for link in le.extract_links(response):
                    print('parse_second else url:{},text{}'.format(link.url, link.text))
                    self.logger.debug('parse_second else url:{},text{}'.format(link.url, link.text))
                    yield Request(link.url, callback=self.parse_books,
                                  meta={'first_category': first_category, 'second_category': second_category,
                                        'third_category': third_category, 'forth_category': forth_category})


    def parse_fifth(self, response):
        print('5' * 20)
        first_category = response.meta.get('first_category')
        second_category = response.meta.get('second_category')
        third_category = response.meta.get('third_category')
        forth_category = response.meta.get('forth_category')
        max_page = response.xpath('//*[@dd_name="底部翻页"]/li[last()-2]/a/text()').extract_first()
        max_page = int(max_page) if max_page else 1
        print('parse_fifth max_page:{} response.url:{}'.format(max_page, response.url))
        self.logger.debug('parse_fifth max_page:{} response.url:{}'.format(max_page, response.url))

        if max_page < 100 and '价格' in response.xpath('//*[@id="navigation"]/ul/li/@dd_name').extract():
            le = LinkExtractor(restrict_xpaths='//*[@id="navigation"]/ul/li[@dd_name="价格"]/div[2]/div[1]/div')
            for link in le.extract_links(response):
                print(link.url, link.text)
                yield Request(link.url, callback=self.parse_books,
                              meta={'first_category': first_category, 'second_category': second_category,
                                    'third_category': third_category, 'forth_category': forth_category})
        else:
            print('第五层的全部爬取url：{}'.format(response.url))
            self.logger.debug('第五层的全部爬取url：{}'.format(response.url))
            le = LinkExtractor(restrict_css='.filtrate_list')
            for link in le.extract_links(response):
                print('parse_second else url:{},text{}'.format(link.url, link.text))
                self.logger.debug('parse_second else url:{},text{}'.format(link.url, link.text))
                yield Request(link.url, callback=self.parse_books,
                              meta={'first_category': first_category, 'second_category': second_category,
                                    'third_category': third_category, 'forth_category': forth_category})


    def parse_books(self, response):
        print('6' * 20)
        first_category = response.meta.get('first_category')
        second_category = response.meta.get('second_category')
        third_category = response.meta.get('third_category')
        forth_category = response.meta.get('forth_category')
        print('parse_books category:{} {} {} {}'.format(first_category, second_category, third_category, forth_category))
        self.logger.debug('parse_books category:{} {} {} {}'.format(first_category, second_category, third_category, forth_category))
        print('parse_books response.url: {}'.format(response.url))
        self.logger.debug('parse_books response.url:'.format(response.url))

        li = response.xpath('//*[@class="bigimg"]/li')
        for i in li:
            self.logger.debug('current parse_books response.url:' + response.url)
            print('current parse_books response.url:' + response.url)
            item = DangdangBookItem()
            item['first_category'] = first_category
            item['second_category'] = second_category
            item['third_category'] = third_category
            item['forth_category'] = forth_category
            item['title'] = i.xpath('./p[@class="name"]/a/@title').extract_first()
            item['url'] = i.xpath('./p[@class="name"]/a/@href').extract_first()
            item['id'] = i.xpath('@id').extract_first()
            if i.xpath('./a/img/@data-original'):
                item['img'] = i.xpath('./a/img/@data-original').extract_first()
            else:
                item['img'] = i.xpath('./a/img/@src').extract_first()
            item['detail'] = i.xpath('./p[@class="detail"]/text()').extract_first()
            # current_price = i.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').extract_first()
            # item['current_price'] = float(current_price.strip('¥')) if current_price else current_price
            # item['current_price'] = float(i.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').extract_first().strip('¥'))
            item['current_price'] = i.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').re_first(r'[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0')
            # original_price = i.xpath('./p[@class="price"]/span[@class="search_pre_price"]/text()').extract_first()
            # item['original_price'] = float(original_price.strip('¥')) if original_price else original_price
            # item['original_price'] = float(i.xpath('./p[@class="price"]/span[@class="search_pre_price"]/text()').extract_first().strip('¥'))
            item['original_price'] = i.xpath('./p[@class="price"]/span[@class="search_pre_price"]/text()').re_first(r'[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0')
            item['discount'] = i.xpath('./p[@class="price"]/span[@class="search_discount"]/text()').re_first(r'[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0')
            item['e_price'] = i.xpath('./p[@class="price"]/a[@class="search_e_price"]/i/text()').re_first(r'[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0')
            item['comment_num'] = i.xpath('./p[@class="search_star_line"]/a[@class="search_comment_num"]/text()').re_first(r'[1-9]\d*|0')
            item['star'] = i.xpath('./p[@class="search_star_line"]/span[@class="search_star_black"]/span/@style').re_first(r'[1-9]\d*|0')
            item['author'] = i.xpath('./p[@class="search_book_author"]/span[1]/a[1]/@title').extract_first()
            seller = i.xpath('./p[@class="search_shangjia"]/a[@name="itemlist-shop-name"]/text()').extract_first()
            item['seller'] = seller if seller else '当当自营'
            date = i.xpath('./p[@class="search_book_author"]/span[2]/text()').extract_first()
            print('date: {}'.format(date))
            self.logger.debug('date: {}'.format(date))
            if date:
                date = date.split('/')
                item['date'] = date[0] if date[0] != ' ' else date[1]
            else:
                item['date'] = date
            item['press'] = i.xpath('./p[@class="search_book_author"]/span[3]/a/text()').extract_first()
            item['cart'] = i.xpath('.//a[@name="Buy"]/text()').extract_first()
            if item['cart'] == '加入购物车':
                item['in_stock'] = '有货'
            else:
                item['in_stock'] = '无货'
            item['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield item

        le = LinkExtractor(restrict_xpaths='//*[@class="next"]')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('parse_books next_url:', next_url)
            self.logger.debug('parse_books next_url:{}'.format(next_url))
            yield Request(next_url, callback=self.parse_books,
                          meta={'first_category': first_category, 'second_category': second_category,
                                'third_category': third_category, 'forth_category': forth_category})



