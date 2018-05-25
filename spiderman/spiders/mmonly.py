#@Time :2018/5/24 下午4:56
#@Author : zl

import scrapy
from scrapy.http import Request
from urllib import parse
from spiderman.items import MMItem

class MMonlySpider(scrapy.Spider):
    name = "mmonly"
    allowed_domains = ["www.mmonly.cc"]
    start_urls = ['http://www.mmonly.cc/mmtp/']


    def parse(self, response):
        post_nodes = response.xpath("//div[@class='ABox']")
        for post_node in post_nodes:
            post_url = post_node.xpath("a/@href").extract_first()
            img_url  = post_node.xpath("a/img/@src").extract_first()
            yield Request(url=parse.urljoin(response.url, post_url),
                      meta={'front_image_url': img_url},
                      callback=self.parse_detail)    # 执行parse_detail 方法

        #下一页url
        next_url = response.xpath("//div[@id='pageNum']/a[last()-1]/@href").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        mmItem = MMItem()
        title = response.xpath("//div[@class='wrapper clearfix imgtitle']/h1/text()").extract()[0]
        img_url = response.xpath("//div[@id='big-pic']/p/a/img/@src").extract()[0]
        front_image_path = response.meta.get("front_image_path")

        mmItem['title'] = title
        mmItem['front_image_url'] = [img_url]
        mmItem['front_image_path'] = front_image_path
        yield mmItem
        #下一页url
        next_url = response.xpath("//li[@id='nl']/a/@href").extract()[0]
        next_url_html = str(next_url).split('.')[-1]
        print(next_url_html)
        if next_url_html == "html":
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse_detail)

