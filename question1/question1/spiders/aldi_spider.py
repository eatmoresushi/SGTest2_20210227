import scrapy

"""
Scrapy tutorial
https://docs.scrapy.org/en/latest/intro/tutorial.html
"""


class AldiSpider(scrapy.Spider):
    name = "aldi"

    def start_requests(self):
        urls = ["https://www.aldi.com.au/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "test.txt"
        with open(filename, "w") as f:
            f.write(response.xpath("//div[@id='footer-sitemap']").get())
        self.log("saved")
