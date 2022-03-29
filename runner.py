# from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerProcess , CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor


from hhru import settings
from spiders.Hhru import HhruSpider
from spiders.superJ import SuperjSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'}) logger

    # process = CrawlerProcess(settings=crawler_settings)
    process = CrawlerRunner(settings=crawler_settings)

    process.crawl(HhruSpider)
    process.crawl(SuperjSpider)

    # process.start()

    d = process.join() #Returns a deferred that is fired when all managed crawlers have completed their executions.
    d.addBoth(lambda _: reactor.stop()) #Convenience method for adding a single callable as both a callback and an errback.
    reactor.run()  # the script will block here until all crawling jobs are finished
