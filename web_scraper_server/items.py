# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_author = scrapy.Field()
    product_price = scrapy.Field()
    product_imagelink = scrapy.Field()

    pass


class ScrapingEbayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_status = scrapy.Field()
    product_price = scrapy.Field()
    product_stars = scrapy.Field()
    product_ratings = scrapy.Field()
    product_url = scrapy.Field()
    product_upc = scrapy.Field()
    product_image = scrapy.Field()
    
    pass
