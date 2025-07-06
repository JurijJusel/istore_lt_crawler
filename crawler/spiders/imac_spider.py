import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from rich import print
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from models.imac_model import ImacItemModel
import datetime


log_path = Path('logs')
log_path.mkdir(parents=True, exist_ok=True)


class ImacSpider(scrapy.Spider):
    name = "imac_spider"
    allowed_domains = ['istore.lt']
    url = "https://istore.lt/apple-mac-kompiuteriai"

    custom_settings = {
        'LOG_FILE': 'logs/imac_logs.log',
        'FEEDS': {
            'data/imac_output.jsonl' : {
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
            product_info = product.css('h2.product-name a::text').get(default='N/A')
            parsed_info = self.parse_imac_product_info(product_info)
            if isinstance(parsed_info, dict):
                product_name = parsed_info.get('name', 'N/A')
                processor = parsed_info.get('processor', 'N/A')
                ram = parsed_info.get('ram', 'N/A')
                disc = parsed_info.get('disc', 'N/A')
                gpu = parsed_info.get('gpu', 'N/A')
                system = parsed_info.get('system', 'N/A')
                color = parsed_info.get('color', 'N/A')

            url = product.css('a.product-image::attr(href)').get(default='N/A')
            img_url = response.css('a.product-image img::attr(src)').get(default='N/A')
            availability = product.css('p.availability.in-stock span::text').get(default='N/A')
            price = product.css('span.price::text').get(default='N/A')
            downloaded_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data = {
                'name': product_name,
                'proc': processor,
                'ram': ram,
                'disc': disc,
                'gpu': gpu,
                'system': system,
                'color': color,
                'price': price,
                'downloaded_date': downloaded_date_time,
                'availability': availability,
                'url': url,
                'image_url': img_url
            }

            item = ImacItemModel(**data)
            yield item.model_dump()

        next_page = response.css('div.pages li a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_imac_product_info(self, product_string):
        """
        Parses the product string to extract relevant information.
        Args:
            product_string (str): The product string to parse.
        Returns:
            dict: A dictionary containing the parsed product information.
            EXP:
            {
                'name': 'MacBook Pro 16"',
                'processor': 'M4 Max 16C CPU',
                'ram': '128GB',
                'disc': '2TB',
                'gpu': '40C GPU',
                'system': 'Mac OS',
                'color': 'Space Black'
            }
        """
        parts = [part.strip() for part in product_string.split(',')]
        fields = ['name', 'processor', 'ram', 'disc', 'gpu', 'system', 'color']
        prod_info = {field: 'N/A' for field in fields}

        for i, part in enumerate(parts):
            if i < len(fields):
                prod_info[fields[i]] = part

        return prod_info

    def closed(self, reason):
        print("\n\n--- istore.lt iMac products Crawl Finished ---")
        print(f"Reason for closure: {reason}\n\n")


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(ImacSpider)
    process.start()
