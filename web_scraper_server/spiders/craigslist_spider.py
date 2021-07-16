import scrapy
import urllib.parse


class CraigslistSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['craigslist.org']
    start_urls = [
        'https://www.vancouver.craigslist.org']

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

        for result in results:
            product_name = result.xpath(
                'div[@class="result-info"]/h3[@class="result-heading"]/a/text()').extract_first()
            product_location = result.xpath(
                'div[@class="result-info"]/span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first()
            product_price = result.xpath(
                'div[@class="result-info"]/span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first()
            # TODO: Extract images from craigslist
            # product_imagelink = job.xpath(
            #     'a[1]/div[4]/text()').extract_first()
            product_link = result.xpath(
                'div[@class="result-info"]/h3[@class="result-heading"]/a/@href').extract_first()

            yield{'Product Name': product_name, 'Product Author': product_location, 'Product Price': product_price, 'Product Image': "N/A", 'Product Link': product_link}
