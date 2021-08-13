import scrapy
import urllib.parse


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.ca']
    start_urls = [
        'https://www.amazon.ca']

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 29
    }

    # Allow a custom parameter (-a flag in the scrapy command)
    def __init__(self, search=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.search_string = search

    def start_requests(self):
        meta = {
            "proxy": "http://scraperapi:80bff441326bec92821b8f614366e13c@proxy-server.scraperapi.com:8001"
        }

        argUrl = urllib.parse.quote_plus(self.search_string)

        yield scrapy.Request('https://www.amazon.ca/s?k=' + argUrl + '&ref=nb_sb_noss_2',
                             callback=self.parse, meta=meta)

    def parse(self, response):
        results = response.css("div.s-result-item")
        limit = 0

        for result in results:
            if limit < 15:
                limit = limit + 1
                product_name = result.css(
                    '.a-color-base.a-text-normal::text').extract_first()
                product_location = result.css(
                    '.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract_first()
                product_price = result.css('.sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-text-price , .sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-price:nth-child(1) .a-offscreen+ span , #nav-logo-sprites , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css('::text').extract_first()
                product_imagelink = result.css(
                    '.s-image::attr(src)').extract_first()

                yield{'Product Name': product_name, 'Product Author': product_location, 'Product Price': product_price, 'Product Image': product_imagelink, 'Product Link': "N/A"}
