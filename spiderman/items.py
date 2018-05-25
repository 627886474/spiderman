# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidermanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    # 伯乐在线
    title = scrapy.Field()
    # create_date = scrapy.Field()
    parise_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into jobbole_spider(title, url,parise_nums,front_image_url,tags,fav_nums,front_image_path)
            VALUES (%s, %s, %s, %s,%s,%s,%s)"""

        params = (self["title"], self["url"],self["parise_nums"],self["front_image_url"],self["tags"],self["fav_nums"],self["front_image_path"])

        return insert_sql, params


class MMItem(scrapy.Item):
    # mm图片
    title = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()

    def get_insert_sql(self):
        insert_sql ="""insert into mm_spider (title,front_image_url,front_image_path)
                      VALUES (%s,%s,%s)"""

        params = (self['title'],self['front_image_url'],self['front_image_path'])

        return insert_sql, params

