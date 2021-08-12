# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapingEbayItem


class EbaySpider(scrapy.Spider):

    name = "ebay"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com"]

    # Allow a custom parameter (-a flag in the scrapy command)
    def __init__(self, search="nintendo switch console"):
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
                status = product.xpath(
                    './/*[@class="SECONDARY_INFO"]/text()').extract_first()
                seller_level = product.xpath(
                    './/*[@class="s-item__etrs-text"]/text()').extract_first()
                location = product.xpath(
                    './/*[@class="s-item__location s-item__itemLocation"]/text()').extract_first()
                product_url = product.xpath(
                    './/a[@class="s-item__link"]/@href').extract_first()
                product_image = product.css(
                    '.s-image__image-img::attr(src)').extract_first()

                # Set default values
                stars = 0
                ratings = 0

                stars_text = product.xpath(
                    './/*[@class="clipped"]/text()').extract_first()
                if stars_text:
                    stars = stars_text[:3]
                ratings_text = product.xpath(
                    './/*[@aria-hidden="true"]/text()').extract_first()
                if ratings_text:
                    ratings = ratings_text.split(' ')[0]

                # yield items
                yield{'Product Name': name, 'Product Author': "N/A", 'Product Price': price, 'Product Image': product_image, 'Product Link': product_url}

        # Get the next page
        next_page_url = response.xpath(
            '//*/a[@class="x-pagination__control"][2]/@href').extract_first()

        # The last page do not have a valid url and ends with '#'
        if next_page_url == None or str(next_page_url).endswith("#"):
            self.log("eBay products collected successfully !!!")
        else:
            print('\n'+'-'*30)
            print('Next page: {}'.format(next_page_url))
            yield scrapy.Request(next_page_url, callback=self.parse_link)

    # Parse details page for each product

    def parse_product_details(self, response):

        # Get the summary data
        data = response.meta['summary_data']

        # Add more data from details page
        data['UPC'] = response.xpath(
            '//h2[@itemprop="gtin13"]/text()').extract_first()

        yield data
