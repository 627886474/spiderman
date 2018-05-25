#@Time :2018/5/23 下午4:18
#@Author : zl

from scrapy.http import Request
from urllib import parse
from items import JobBoleArticleItem

import scrapy,re


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//*[@id="archive"]/div')
        # 因为获取的post_urls和image_url 在同一个div下，这里需要一一对应的关系
        # 所以使用meta 来保存字典，以保证一一对应
        # post_nodes 作为节点，是post_urls和image_url 共同的xpath可以共用
        # response.xpath 可以链式的取值
        for post_node in post_nodes:
            post_urls = post_node.xpath('div[2]/p/a[1]/@href').extract_first()
            image_url = post_node.xpath('div/a/img/@src').extract_first()
            yield Request(url=parse.urljoin(response.url,post_urls),
                          meta={'front_image_url':image_url},
                          callback=self.parse_detail)
            #直接将Request交给scrapy进行下载
            # callback 执行回调函数,执行双向爬去

        next_url = response.xpath('//*[@class="next page-numbers"]/@href').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self,response):
        article_item = JobBoleArticleItem()

        title = response.xpath('//div[@class="entry-header"]/h1').extract_first()
        parise_nums=response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        tags = response.xpath('//*[@id="wrapper"]/div[3]/div[1]/div[2]/p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[0]
        front_image = response.meta["front_image_url"]  # 获取parse 中提取到的url

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["parise_nums"] = parise_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["front_image_url"] = [front_image]
        article_item["front_image_path"] = response.meta.get("front_image_path")

        yield article_item

