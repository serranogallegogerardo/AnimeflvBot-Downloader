import json
from requests_html import HTMLSession

# Abre el archivo JSON
with open('animeSeasons.json') as f:
    links = json.load(f)

# Inicializa una lista para almacenar los enlaces de los episodios
episode_links_list = []

# Crea una sesión HTML
session = HTMLSession()

# Itera sobre la lista de enlaces
for link in links:
    # Envía una solicitud para obtener el contenido de la página web
    r = session.get(link)

    # Espera a que la página se renderice completamente
    r.html.render()

    # Encuentra los elementos que contienen los enlaces de los capítulos
    episodes = r.html.find('.ListCaps li a')

    # Verifica si hay algún episodio disponible
    if episodes:
        # Obtiene el primer episodio
        first_episode = episodes[-1]
        episode_link = first_episode.absolute_links.pop()  # Extrae el enlace absoluto

        # Agrega el enlace del episodio a la lista
        episode_links_list.append(episode_link)

        print("Enlace del primer episodio:", episode_link)
    else:
        print("No se encontraron episodios disponibles para", link)

# Cierra la sesión
session.close()

# Guarda la lista de enlaces de episodios en un archivo JSON
with open('firstEpisodes.json', 'w') as f:
    json.dump(episode_links_list, f)

# Imprime un mensaje de confirmación
print("Lista de enlaces de episodios guardada en 'firstEpisodes.json'.")
