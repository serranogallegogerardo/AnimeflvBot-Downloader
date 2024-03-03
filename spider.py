import scrapy
from scrapy.crawler import CrawlerProcess
from lxml import html
import json

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

        # Save the download links to a JSON file
        with open('download_links.json', 'w') as f:
            json.dump(download_links, f)

process = CrawlerProcess()
process.crawl(AnimeFLVSpider)
process.start()
