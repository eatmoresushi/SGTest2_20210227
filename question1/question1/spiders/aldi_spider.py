import scrapy

"""
Scrapy tutorial
https://docs.scrapy.org/en/latest/intro/tutorial.html
"""


class AldiSpider(scrapy.Spider):
    name = "aldi"

    start_urls = ["https://www.aldi.com.au/"]

    def parse(self, response):
        # get all the submenu links of Groceries
        submenu_links = response.xpath(
            "//div[@id='footer-sitemap']/div[2]/div/div/ul/li/a/@href"
        ).getall()
        yield from response.follow_all(submenu_links, self.parse_submenu)

    def parse_submenu(self, response):
        product_tiles = response.xpath("//div[@class='tx-aldi-products']/div/a")
        if len(product_tiles) > 0:
            for product in product_tiles:
                yield {
                    "Product_title": product.xpath("./div/div/div[2]/div/text()")
                    .get()
                    .strip(),
                    "Product_image": product.xpath("./div/div/div[1]/img/@src").get(),
                    "Packsize": product.xpath(
                        "./div/div/div[2]/div[2]/span[@class='box--amount']/text()"
                    )
                    .get()
                    .strip(),
                    "Price": product.xpath(
                        "./div/div/div[2]/div[2]/span[@class='box--value']/text()"
                    )
                    .get()
                    .strip()
                    + product.xpath(
                        "./div/div/div[2]/div[2]/span[@class='box--decimal']/text()"
                    )
                    .get()
                    .strip(),
                    "Price per unit": product.xpath(
                        "./div/div/div[2]/div[2]/span[@class='box--baseprice']/text()"
                    )
                    .get()
                    .strip(),
                }
