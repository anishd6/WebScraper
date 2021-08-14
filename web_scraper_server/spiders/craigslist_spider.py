import scrapy
import urllib.parse


class CraigslistSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['craigslist.org']
    start_urls = [
        'https://www.vancouver.craigslist.org']

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 5
    }

    # Allow a custom parameter (-a flag in the scrapy command)
    def __init__(self, search=None, *args, **kwargs):
        super(CraigslistSpider, self).__init__(*args, **kwargs)
        self.search_string = search

    def start_requests(self):
        meta = {
            "proxy": "http://scraperapi:80bff441326bec92821b8f614366e13c@proxy-server.scraperapi.com:8001"
        }

        argUrl = urllib.parse.quote(self.search_string)

        yield scrapy.Request('https://vancouver.craigslist.org/d/for-sale/search/sss?query=' + argUrl + '&sort=rel',
                             callback=self.parse, meta=meta)

    def parse(self, response):
        results = response.xpath('//li[@class="result-row"]')
        limit = 0
        
        for result in results:
            if limit < 15:
                limit = limit + 1
                product_name = result.xpath(
                    'div[@class="result-info"]/h3[@class="result-heading"]/a/text()').extract_first()
                product_price = result.xpath(
                    'div[@class="result-info"]/span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first()
                image_id = result.xpath('a/@data-ids').extract_first()
                product_link = result.xpath(
                    'div[@class="result-info"]/h3[@class="result-heading"]/a/@href').extract_first()

                product_imagelink = 'https://images.craigslist.org/' + image_id.split(',')[0].split(":",1)[1] + '_300x300.jpg' if image_id is not None else "None"

                yield{'Product Name': product_name, 'Product Author': "Craigslist - " + limit, 'Product Price': product_price, 'Product Image': product_imagelink, 'Product Link': product_link}
