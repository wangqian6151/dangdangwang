# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from pprint import pprint

from scrapy import Field, Item


class DangdangBookItem(Item):
    collection = table = 'dangdang_book'

    first_category = Field()
    second_category = Field()
    third_category = Field()
    forth_category = Field()
    title = Field()
    url = Field()
    id = Field()
    current_price = Field()
    original_price = Field()
    discount = Field()
    author = Field()
    press = Field()
    date = Field()
    comment_num = Field()
    star = Field()
    seller = Field()
    cart = Field()
    in_stock = Field()
    e_price = Field()
    img = Field()
    detail = Field()
    crawl_time = Field()
