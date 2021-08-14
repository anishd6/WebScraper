import scrapy
from ..items import ScrapingEbayItem


class EbaySpider(scrapy.Spider):

    name = "ebay"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com"]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3
    }

    # Allow a custom parameter (-a flag in the scrapy command)
    def __init__(self, search=None, *args, **kwargs):
        super(EbaySpider, self).__init__(*args, **kwargs)
        self.search_string = search

    def parse(self, response):

        meta = {
            "proxy": "http://scraperapi:80bff441326bec92821b8f614366e13c@proxy-server.scraperapi.com:8001"
        }

        # Extrach the trksid to build a search request
        trksid = response.css("input[type='hidden'][name='_trksid']").xpath(
            "@value").extract()[0]

        # Build the url and start the requests
        yield scrapy.Request("http://www.ebay.com/sch/i.html?_from=R40&_trksid=" + trksid +
                             "&_nkw=" +
                             self.search_string.replace(
                                 ' ', '+') + "&_ipg=200",
                             callback=self.parse_link, meta=meta)

    # Parse the search results
    def parse_link(self, response):
        items = ScrapingEbayItem()
        # Extract the list of products
        results = response.xpath(
            '//div/div/ul/li[contains(@class, "s-item" )]')
        limit = 0

        # Extract info for each product
        for product in results:
            if limit < 15:
                limit = limit + 1
                name = product.xpath(
                    './/*[@class="s-item__title"]//text()').extract_first()
                # Sponsored or New Listing links have a different class
                if name == None:
                    name = product.xpath(
                        './/*[@class="s-item__title s-item__title--has-tags"]/text()').extract_first()
                    if name == None:
                        name = product.xpath(
                            './/*[@class="s-item__title s-item__title--has-tags"]//text()').extract_first()
                if name == 'New Listing':
                    name = product.xpath(
                        './/*[@class="s-item__title"]//text()').extract()[1]

                # If this get a None result
                if name == None:
                    name = "ERROR"

                price = product.xpath(
                    './/*[@class="s-item__price"]/text()').extract_first()
                product_url = product.xpath(
                    './/a[@class="s-item__link"]/@href').extract_first()
                product_image = product.css(
                    '.s-item__image-img::attr(src)').extract_first()

                # yield items
                yield{'Product Name': name, 'Product Author': "eBay - " + str(limit), 'Product Price': price, 'Product Image': product_image, 'Product Link': product_url}