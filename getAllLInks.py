import scrapy
from scrapy.crawler import CrawlerProcess
from lxml import html
from scrapy.utils.project import get_project_settings
import sys
import json
import re


class AnimeFLVSpider(scrapy.Spider):
    name = 'animeflv'
    
    # Define start_urls como una lista vacía
    start_urls = []

    def start_requests(self):
        # Itera sobre los enlaces de episodios en episode_links_list y crea solicitudes para cada uno
        for url in self.start_urls:
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

# Obtener episode_links_list de los argumentos de línea de comandos
episode_links_list = sys.argv[1:]

print(episode_links_list)

# Asignar episode_links_list a start_urls
AnimeFLVSpider.start_urls = episode_links_list

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
all_series_sorted = dict(sorted(all_series.items()))

# Ordenar los capítulos dentro de cada serie por número de capítulo
for serie_name, chapters in all_series_sorted.items():
    if len(chapters) > 1:
        all_series_sorted[serie_name] = dict(sorted(chapters.items(), key=lambda x: int(x[0])))
    else:
        all_series_sorted[serie_name] = chapters

# Crear un diccionario para almacenar todos los capítulos
all_chapters = {}

# Intentar leer el contenido del archivo JSON existente
try:
    with open("all_chapters.json", 'r', encoding='utf-8') as f:
        all_chapters = json.load(f)
except FileNotFoundError:
    pass  # Si el archivo no existe, simplemente continuamos con un diccionario vacío

# Actualizar el diccionario con los nuevos capítulos
for anime, chapters in all_series_sorted.items():
    if anime in all_chapters:
        all_chapters[anime].update(chapters)
    else:
        all_chapters[anime] = chapters

# Guardar todos los capítulos en el mismo archivo JSON
with open("all_chapters.json", 'w', encoding='utf-8') as f:
    json.dump(all_chapters, f, ensure_ascii=False, indent=4)