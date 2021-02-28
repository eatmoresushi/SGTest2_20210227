import scrapy

"""
Scrapy tutorial
https://docs.scrapy.org/en/latest/intro/tutorial.html
Feed Export to csv
$ scrapy crawl aldi -O aldi.csv
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
        def extract_with_xpath(element, query):
            return element.xpath(query).get(default="").strip()

        product_tiles = response.xpath(
            "//div[@class='tx-aldi-products']/div/a"
        )
        if len(product_tiles) > 0:
            for product in product_tiles:
                # special handing for product title
                all_title_text = product.xpath(
                    "./div/div/div[2]/div[self::*|self::sup]/text()"
                ).getall()
                yield {
                    "Product_title": "".join(
                        _ for _ in all_title_text
                    ).strip(),
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
            sub_submenu_links = response.xpath(
                "//div/div/div/div/div/a/@href"
            ).getall()
            yield from response.follow_all(
                sub_submenu_links, self.parse_submenu
            )
