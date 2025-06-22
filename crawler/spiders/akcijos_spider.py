import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from rich import print
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from models.product_model import IstoreItemModel
import datetime

log_path = Path('logs')
log_path.mkdir(parents=True, exist_ok=True)


class AkcijosSpider(scrapy.Spider):
    name = "akcijos_spider"
    allowed_domains = ['istore.lt']
    url ="https://istore.lt/apple-akcijos-nuolaidos"

    custom_settings = {
        'LOG_FILE': 'logs/akcijos_logs.log',
        'FEEDS': {
            'data/akcijos_output.jsonl' : {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': True
            }
        }
    }

    async def start(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        print(f"Parsing page: {response.url}")
        status_code = response.status
        print('status code -', status_code)

        if status_code != 200:
            print(f"error Failed to fetch the page, status code: {status_code}")
            return

        products = response.css('ul.products-grid li.item')
        for product in products:
            name = product.css('h2.product-name a::text').get(default='N/A')
            url = product.css('a.product-image::attr(href)').get(default='N/A')
            img = response.css('a.product-image img::attr(src)').get(default='N/A')
            availability = product.css('p.availability.in-stock span::text').get(default='N/A')
            price = product.css('span.price::text').get(default='N/A')
            downloaded_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data = {
                'name': name,
                'price': price,
                'downloaded_date': downloaded_date_time,
                'availability': availability,
                'url': url,
                'image_url': img
            }
            item = IstoreItemModel(**data)
            yield item.model_dump()

        next_page = response.css('div.pages li a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        print("\n\n--- istore.lt akcijos - nuolaidos products Crawl Finished ---")
        print(f"Reason for closure: {reason}\n\n")


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(AkcijosSpider)
    process.start()
