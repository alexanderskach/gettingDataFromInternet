import scrapy
from scrapy.http import HtmlResponse
from hhru.items import JobparserItem


class SuperjSpider(scrapy.Spider):
    name = 'superJ'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/inzhener.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        # print('-------------->NEXT_PAGE: ', next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@target="_blank"]/@href').getall()
        # print('-------------->LINK: ', links)
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        print('-------------->NAME: ', name)
        # salary = response.xpath("//div[@class='vacancy-salary']//text()").getall()
        salary = response.xpath("//span[@class='_2Wp8I _1BiPY _26ig7 _18w_0']/text()").getall()
        print('-------------->SALARY: ', salary)
        link = response.url
        print('-------------->LINK: ', link)
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
