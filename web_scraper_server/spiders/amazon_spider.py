import scrapy
import urllib.parse


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.ca']
    start_urls = [
        'https://www.amazon.ca']

    # Allow a custom parameter (-a flag in the scrapy command)
    def __init__(self, search=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.search_string = search

    def start_requests(self):
        meta = {
            "proxy": "http://scraperapi:8831186ef0337b788b1d16870c894d2c@proxy-server.scraperapi.com:8001"
        }

        argUrl = urllib.parse.quote_plus(self.search_string)

        yield scrapy.Request('https://www.amazon.ca/s?k=' + str(argUrl) + '&ref=nb_sb_noss_2',
                             callback=self.parse, meta=meta)

    def parse(self, response):
        results = response.css("div.s-result-item")
        limit = 0

        for result in results:
            if limit < 15:

                product_name = result.css(
                    '.a-color-base.a-text-normal::text').extract_first()
                product_price = result.css('.sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-text-price , .sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-price:nth-child(1) .a-offscreen+ span , #nav-logo-sprites , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css('::text').extract_first()
                product_imagelink = result.css('.s-image::attr(src)').extract_first()
                product_productlink = result.css('.a-link-normal::attr(href)').extract_first()


                if (product_price is not None):
                    yield{'Product Name': product_name, 'Product Author': "Amazon", 'Product Price': "$" + str(product_price), 'Product Image': product_imagelink, 'Product Link': "amazon.ca" + str(product_productlink)}
                    limit = limit + 1
                else:
                    continue
