import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from opendata.items import OpendataItem


class CulturedataSpider(scrapy.Spider):
    name = 'culturedata'
    allowed_domains = ['hubofdata.ru']

    def __init__(self):

        self.start_urls = ['https://www.hubofdata.ru/dataset/vladimir_covid-19/resource/8d87b4c0-cdf3-47a5-947a-9bc1d46e864b']

    def parse(self, response):

        loader = ItemLoader(item=OpendataItem(), response=response)
        loader.add_xpath('urldata', "//a[@class='resource-url-analytics']/@href")
        yield loader.load_item()



