import scrapy

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        jobs = response.xpath('//div[@class="result-info"]')

        for job in jobs:
            absolute_url = job.xpath(
                'h3[@class="result-heading"]/a/@href').extract_first()
            title = job.xpath(
                'h3[@class="result-heading"]/a/text()').extract_first()
            address = job.xpath(
                'span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]

            yield{'URL': absolute_url, 'Title': title, 'Address': address}
