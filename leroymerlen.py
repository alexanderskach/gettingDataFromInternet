import scrapy
from scrapy.http import HtmlResponse
from leroimerlen.leroimerlen.items import LeroimerlenItem
from scrapy.loader import ItemLoader


class LeroymerlenSpider(scrapy.Spider):
    handle_httpstatus_list = [401]
    name = 'leroymerlen'
    allowed_domains = ['combook.ru']

    def __init__(self, search):

        self.start_urls = [f'https://www.combook.ru/search/?search_str={search}']

    def parse(self, response: HtmlResponse):

        links = response.xpath("//ul[@id='category']/li//a[not (contains(@href, 'javascript'))]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroimerlenItem(), response=response)
        loader.add_xpath('name', "//h1[@class='black']/text()")
        loader.add_xpath('number', "//div[@class ='tovnumb']/text()")
        loader.add_xpath('price', "//div[@class='price']/div[@id='product_price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//a[@style='cursor:pointer;']/@href")
        yield loader.load_item()

