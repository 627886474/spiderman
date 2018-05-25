#@Time :2018/5/23 下午12:24
#@Author : zl


from scrapy.cmdline import execute


import sys
import os

'''
    scrapy原本没有main.py的文件，
    这里新建main文件，以便于使用pycharm进行调试爬虫
'''
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","mmonly"])