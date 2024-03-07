import json
import scrapy
from scrapy.crawler import CrawlerProcess
from lxml import html
from scrapy.utils.project import get_project_settings

class AnimeFLVSpider(scrapy.Spider):
    name = 'animeflv'

    def start_requests(self):
        with open('firstEpisodes.json', 'r') as f:
            start_urls = json.load(f)
            for url in start_urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tree = html.fromstring(response.text)
        download_links = tree.xpath('//table[@class="RTbl Dwnl"]//a[@class="Button Sm fa-download"]/@href')

        # Obtener el nombre de la serie desde la URL
        serie_name = tree.xpath('//*[@id="XpndCn"]/div[1]/nav/a[2]/text()')[0].strip()

        # Obtener el número de capítulo
        chapter_number = response.url.split('/')[-1].split('-')[-1]

        # Crear un diccionario para almacenar los enlaces de descarga
        chapter_data = {}

        # Agregar los enlaces de descarga al diccionario
        for i, link in enumerate(download_links, start=1):
            chapter_data[f'Proveedor {i}'] = link

        # Agregar los enlaces de descarga al diccionario de todos los capítulos
        if serie_name not in all_series:
            all_series[serie_name] = {}
        if chapter_number not in all_series[serie_name]:
            all_series[serie_name][chapter_number] = []
        all_series[serie_name][chapter_number].append(chapter_data)

        # Check if there is a next page link
        next_page_link = tree.xpath('//a[@class="CapNvNx fa-chevron-right"]/@href')
        if next_page_link:
            # Follow the next page link and continue scraping
            yield response.follow(next_page_link[0], callback=self.parse)


# Crear un diccionario para almacenar todas las series y sus capítulos
all_series = {}

# Configurar las opciones de scraping
settings = get_project_settings()
settings.update({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
})

# Iniciar el proceso de scraping
process = CrawlerProcess(settings)
process.crawl(AnimeFLVSpider)
process.start()

# Ordenar las series alfabéticamente
all_series_sorted = dict(sorted(all_series.items(), key=lambda x: x[0]))

# Ordenar los capítulos dentro de cada serie por número de capítulo
for serie_name, chapters in all_series_sorted.items():
    all_series_sorted[serie_name] = dict(sorted(chapters.items(), key=lambda x: int(x[0])))

# Guardar todos los capítulos en un archivo JSON
data_ordenado = {anime: dict(sorted(capitulos.items(), key=lambda x: int(x[0]))) for anime, capitulos in all_series_sorted.items()}

# Guardar el JSON ordenado en un nuevo archivo
with open('download_links_ordenado.json', 'w', encoding='utf-8') as f:
    json.dump(data_ordenado, f, ensure_ascii=False, indent=4)
