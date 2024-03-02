import scrapy
from scrapy.crawler import CrawlerProcess
from lxml import html

class AnimeFLVSpider(scrapy.Spider):
    name = 'animeflv'
    start_urls = ['https://www3.animeflv.net/ver/86-eighty-six-1']

    def parse(self, response):
        tree = html.fromstring(response.text)
        download_links = tree.xpath('//table[@class="RTbl Dwnl"]//a[@class="Button Sm fa-download"]/@href')
        for link in download_links:
            yield {
                'download_link': link
            }

process = CrawlerProcess()
process.crawl(AnimeFLVSpider)
process.start()
