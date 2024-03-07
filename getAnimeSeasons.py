import scrapy
import json
from scrapy import cmdline

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
        # Solicitar al usuario el nombre del anime
        anime_name = input("Ingrese el nombre del anime: ")

        # Agregar el nombre del anime al URL de búsqueda
        search_url = f"https://www3.animeflv.net/browse?q={anime_name}"

        # Realizar la solicitud GET al URL de búsqueda
        yield scrapy.Request(search_url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        # Encontrar todos los enlaces que coincidan con la búsqueda
        anime_links = response.css('a[href*="/anime/"]::attr(href)').getall()

        # Procesar los enlaces encontrados
        procesar_links(anime_links)

        print(links_procesados)
        

        # Guardar los enlaces procesados en un archivo JSON
        with open('animeSeasons.json', 'w') as file:
            json.dump(list(links_procesados), file)

        # Imprimir un mensaje indicando que se han guardado los enlaces en el archivo JSON
        print("Los enlaces procesados se han guardado en 'anime_links.json'")

if __name__ == "__main__":
    # Ejecutar la araña
    cmdline.execute("scrapy runspider getAnimeSeasons.py".split())
    


