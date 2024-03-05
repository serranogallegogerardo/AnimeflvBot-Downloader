from requests_html import HTMLSession

# Creamos una sesión HTML
session = HTMLSession()

# Enviamos una solicitud para obtener el contenido de la página web
r = session.get('https://www3.animeflv.net/anime/berserk')

# Esperamos a que la página se renderice completamente
r.html.render()

# Encontramos los elementos que contienen los enlaces de los capítulos
episodes = r.html.find('.ListCaps li a')

# Iteramos sobre los elementos para extraer los enlaces y los títulos de los capítulos
for episode in episodes:
    episode_title = episode.text
    episode_link = episode.absolute_links.pop()  # Extraemos el enlace absoluto
    print("Título del episodio:", episode_title)
    print("Enlace del episodio:", episode_link)

# Cerramos la sesión
session.close()
