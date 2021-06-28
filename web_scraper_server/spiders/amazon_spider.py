import scrapy

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        'https://www.amazon.ca/Books-Last-30-days/s?rh=n%3A916520%2Cp_n_date%3A12035756011']

    def parse(self, response):
        
        results = response.css("div.s-result-item")

        for result in results:
            product_name = result.css(
                '.a-color-base.a-text-normal::text').extract_first()
            product_location = result.css(
                '.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract_first()
            product_price = result.css('.sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-text-price , .sg-col-0-of-12:nth-child(1) .a-spacing-mini:nth-child(1) .a-price:nth-child(1) .a-offscreen+ span , #nav-logo-sprites , .a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css('::text').extract_first()
            product_imagelink = result.css('.s-image::attr(src)').extract_first()

            yield{'Product Name': product_name, 'Product Author': product_location, 'Product Price': product_price, 'Product Image': product_imagelink, 'Product Link': "N/A"}