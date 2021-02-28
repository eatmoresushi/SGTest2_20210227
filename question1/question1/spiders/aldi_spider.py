import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

"""
Scrapy tutorial
https://docs.scrapy.org/en/latest/intro/tutorial.html
Error handling:
https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=errback#using-errbacks-to-catch-exceptions-in-request-processing
Feed Export to csv
$ scrapy crawl aldi -O aldi.csv
"""


class AldiSpider(scrapy.Spider):
    name = "aldi"

    start_urls = ["https://www.aldi.com.au/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, errback=self.errback_aldi, dont_filter=True
            )

    def parse(self, response):
        self.logger.info("Got successful response from {}".format(response.url))
        # get all the submenu links of Groceries
        submenu_links = response.xpath(
            "//div[@id='footer-sitemap']/div[2]/div/div/ul/li/a/@href"
        ).getall()
        yield from response.follow_all(submenu_links, self.parse_submenu)

    def errback_aldi(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)

    def parse_submenu(self, response):
        def extract_with_xpath(element, query):
            return element.xpath(query).get(default="").strip()

        product_tiles = response.xpath("//div[@class='tx-aldi-products']/div/a")
        if len(product_tiles) > 0:
            for product in product_tiles:
                # special handing for product title
                all_title_text = product.xpath(
                    "./div/div/div[2]/div[self::*|self::sup]/text()"
                ).getall()
                yield {
                    "Product_title": "".join(_ for _ in all_title_text).strip(),
                    "Product_image": extract_with_xpath(
                        product, "./div/div/div[1]/img/@src"
                    ),
                    "Packsize": extract_with_xpath(
                        product,
                        "./div/div/div[2]/div[2]/span[@class='box--amount']/text()",
                    ),
                    # price includes values before and after the decimal point
                    "Price": extract_with_xpath(
                        product,
                        "./div/div/div[2]/div[2]/span[@class='box--value']/text()",
                    )
                    + extract_with_xpath(
                        product,
                        "./div/div/div[2]/div[2]/span[@class='box--decimal']/text()",
                    ),
                    "Price per unit": extract_with_xpath(
                        product,
                        "./div/div/div[2]/div[2]/span[@class='box--baseprice']/text()",
                    ),
                }
        else:
            # some categories require another click
            sub_submenu_links = response.xpath("//div/div/div/div/div/a/@href").getall()
            yield from response.follow_all(sub_submenu_links, self.parse_submenu)
