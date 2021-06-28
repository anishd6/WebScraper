import scrapy

class CraigslistSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['craigslist.org']
    start_urls = [
        'https://vancouver.craigslist.org/d/for-sale/search/sss?query=nintendo%20switch%20console&sort=rel']

    def parse(self, response):
        results = response.xpath('//li[@class="result-row"]')

        for result in results:
            product_name = result.xpath(
                'div[@class="result-info"]/h3[@class="result-heading"]/a/text()').extract_first()
            product_location = result.xpath(
                'div[@class="result-info"]/span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first()
            product_price = result.xpath(
                'div[@class="result-info"]/span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first()
            #TODO: Extract images from craigslist
            # product_imagelink = job.xpath(
            #     'a[1]/div[4]/text()').extract_first()
            product_link = result.xpath(
                'div[@class="result-info"]/h3[@class="result-heading"]/a/@href').extract_first()

            yield{'Product Name': product_name, 'Product Author': product_location, 'Product Price': product_price, 'Product Image': "N/A", 'Product Link': product_link}
