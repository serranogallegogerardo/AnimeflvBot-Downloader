import json
import sys
import scrapy
from scrapy import cmdline
import subprocess

# Conjunto de links procesados (sin duplicados)
links_procesados = set()

def procesar_links(links_originales):
    global links_procesados
    # Procesar los links
    for link in links_originales:
        # Eliminar la parte "/ver/" del link
        link_procesado = f"https://www3.animeflv.net{link.replace('/ver/', '')}"
        # Agregar el link procesado al conjunto de links procesados
        links_procesados.add(link_procesado)

class AnimeflvSpider(scrapy.Spider):
    name = 'animeflv_spider'
    allowed_domains = ['www3.animeflv.net']

    def start_requests(self):
        # Leer el nombre del anime desde la entrada estándar
        anime_name = sys.argv[1] if len(sys.argv) > 1 else input("Ingrese el nombre del anime: ")

        # Agregar el nombre del anime al URL de búsqueda
        search_url = f"https://www3.animeflv.net/browse?q={anime_name}"

        # Realizar la solicitud GET al URL de búsqueda
        yield scrapy.Request(search_url, callback=self.parse_search_results, meta={'anime_name': anime_name})

    def parse_search_results(self, response):
        # Encontrar todos los enlaces que coincidan con la búsqueda
        anime_links = response.css('a[href*="/anime/"]::attr(href)').getall()

        # Procesar los enlaces encontrados
        procesar_links(anime_links)

        # Ejecutar el siguiente script y pasar el nombre del anime como argumento
        for episode_link in links_procesados:
            print(episode_link)
            subprocess.run(["python", "getFirstEpisode.py", episode_link])

        # old code
        # Procesar los enlaces encontrados
        # procesar_links(anime_links)

        # print(links_procesados)

        # # Guardar los enlaces procesados en un archivo JSON
        # with open('animeSeasons.json', 'w') as file:
        #     json.dump(list(links_procesados), file)

        # # Imprimir un mensaje indicando que se han guardado los enlaces en el archivo JSON
        # print("Los enlaces procesados se han guardado en 'anime_links.json'")

        # Imprimir un mensaje indicando que se han guardado los enlaces en el archivo JSON
        print("Los enlaces procesados se pasaron al próximo script.")

if __name__ == "__main__":
    # Ejecutar la araña
    cmdline.execute("scrapy runspider getAnimeSeasons.py".split())
