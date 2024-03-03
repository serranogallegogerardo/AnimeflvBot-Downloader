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

        # Obtener el número de capítulo
        chapter_number = response.url.split('-')[-1]

        # Crear un diccionario para almacenar los enlaces de descarga
        chapter_data = {}

        # Agregar los enlaces de descarga al diccionario
        for i, link in enumerate(download_links, start=1):
            chapter_data[f'provedor{i}'] = link

        # Agregar los enlaces de descarga al diccionario de todos los capítulos
        all_chapters[int(chapter_number)] = chapter_data

        # Check if there is a next page link
        next_page_link = tree.xpath('//a[@class="CapNvNx fa-chevron-right"]/@href')
        if next_page_link:
            # Follow the next page link and continue scraping
            yield response.follow(next_page_link[0], callback=self.parse)

# Crear un diccionario para almacenar todos los capítulos
all_chapters = {}

process = CrawlerProcess()
process.crawl(AnimeFLVSpider)
process.start()

# Ordenar los índices del diccionario
all_chapters_sorted = dict(sorted(all_chapters.items()))

# Guardar todos los capítulos en un archivo JSON
with open('download_links.json', 'w') as f:
    json.dump(all_chapters_sorted, f, sort_keys=True, indent=4)
