# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):

    text = scrapy.Field()
    date = scrapy.Field()
    each_url = scrapy.Field()
    shortcode = scrapy.Field()
    like_count = scrapy.Field()
    explain = scrapy.Field()
    video_view_count = scrapy.Field()
    # location = scrapy.Field()
    # address_json = scrapy.Field()
    # is_video = scrapy.Field()
    # mediaList = scrapy.Field()