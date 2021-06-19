import scrapy
from ..items import AmazonscraperItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        'https://www.amazon.ca/Books-Last-30-days/s?rh=n%3A916520%2Cp_n_date%3A12035756011'
    ]

    def parse(self, response):
        items = AmazonscraperItem()
#do by using chrome extension
        product_name = response.css('.a-color-base.a-text-normal::text').extract()
        product_author = response.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract()
        product_price = response.css('.sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-text-price , .sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-price:nth-child(1) .a-offscreen+ span , #nav-logo-sprites , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css('::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

        items[ 'product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        yield items
