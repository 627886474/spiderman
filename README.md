# scrapy spider
## 项目结构说明
- spiders:存放爬虫目录
- utils:工具类，将一些共用的方法类存放在这个文件夹下
- main文件：运行scrapy爬虫的命令，放在main文件下，以便于使用pycharm进行调试
- pipelines：mysql连接池操作，只需要在items中添加sql语句即可
- items：需要提取的数据，添加get_insert_sql方法，即可被pipelines调用
- settings：scrapy配置文件
### 爬虫列表
>1.伯乐在线爬虫(jobbole)
>>settings中需要打开MyImagePipeline，与MysqlTwistedPipeline。MyImagePipeline的执行优先级需要比与MysqlTwistedPipeline存数据  
的优先级高
>>MyImagePipeline继承ImagesPipeline，重写了图片存储的功能，修改了存储图片名字
>2.美女图库爬虫(mmonly)
>>比伯乐在线的爬虫多一层逻辑，这里保存图片的路径也是通过重写Imagespipeline来实现的。
>3.拉钩网爬虫(lagou)
>>北上广深，语言需求，各种语言工资


