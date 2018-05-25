# -*- coding: utf-8 -*-

import pymysql
import codecs,json
from scrapy.http import Request

from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline

class SpidermanPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    '''
    自定义json文件的导出
    '''
    def __init__(self,item,spider):
        self.file = codecs.open('article.json')

    def process_item(self,item,spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return

    def spider_closed(self,spider):
        self.file.close()


class JsonExporterPipleline(object):
    '''
    调用scrapy提供的JsonItemExporter,导出json
    '''
    def __init__(self):
        self.file = open('export.json','wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item()
        return item


class MyImagePipeline(ImagesPipeline):
    '''
    处理图片的pipeline,jobbole爬虫
    '''
    def item_completed(self, results, item, info):
        front_image_path = [x['path'] for ok, x in results if ok]
        if not front_image_path:
            raise DropItem("Item contains no images")
        item['front_image_path'] = front_image_path
        return item

    def file_path(self, request, response=None, info=None):
      # 按照图片名称进行保存
        image_http_url = request.url
        # image_http_url   http://jbcdn2.b0.upaiyun.com/2016/09/cfb878cc788ffd38bb744dd98d83c4fb.jpg
        image_guid = str(image_http_url).replace('http://','')
        return '/image/%s'%(image_guid)


class MysqlTwistedPipeline(object):
    '''
        插入数据
    '''
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("pymysql",**dbparms)

        return cls(dbpool)

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(1111)
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常



class MMImagePipeline(ImagesPipeline):
    '''
    处理MM图片的pipeline
    '''

    def get_media_requests(self, item, info):
        for image_url in item['front_image_url']:
            referer=image_url  # 处理防盗链
            yield Request(image_url,meta={'item': item,'referer':referer})#配合get_media_requests传递meta，不然拿不到item的.不会下载


    def file_path(self, request, response=None, info=None):
        #图片保存路径
        item = request.meta['item']
        folder = item['title']
        folder_strip = folder.strip()   # strip()消除空格
        image_type = request.url.split('/')[-1]  # 取图片名称
        filename = '/{0}/{1}'.format(folder_strip,image_type)
        return filename


    def item_completed(self, results, item, info):
        front_image_path = [x['path'] for ok, x in results if ok]
        if not front_image_path:
            raise DropItem("Item contains no images")
        item['front_image_path'] = front_image_path
        return item
