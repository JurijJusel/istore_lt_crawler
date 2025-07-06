from scrapy.crawler import CrawlerProcess
from crawler.spiders.imac_spider import ImacSpider
from crawler.spiders.iphone_spider import IphoneSpider
from crawler.spiders.akcijos_spider import AkcijosSpider
from crawler.spiders.ipad_spider import IpadSpider
from crawler.spiders.priedai_spider import PriedaiSpider
from crawler.spiders.watch_spider import WatchSpider
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())
process.crawl(ImacSpider)
process.crawl(IphoneSpider)
process.crawl(AkcijosSpider)
process.crawl(IpadSpider)
process.crawl(PriedaiSpider)
process.crawl(WatchSpider)

process.start()
