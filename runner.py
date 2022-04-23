# from scrapy import settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from opendata import settings
from opendata.spiders.culturedata import CulturedataSpider

crawler_settings = Settings()
crawler_settings.setmodule(settings)

process = CrawlerProcess(settings=crawler_settings)
# search = input('')

process.crawl(CulturedataSpider)
process.start()