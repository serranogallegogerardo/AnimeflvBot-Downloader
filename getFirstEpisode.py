import sys
import json
from requests_html import HTMLSession
import subprocess

if __name__ == "__main__":
    # Obtener la lista de enlaces como argumentos de línea de comandos

    #desarmar rompecabezas comentando esto
    links = sys.argv[1:]
    
    # Tu código para procesar los enlaces
    episode_links_list = []
    session = HTMLSession()

    for link in links:
        r = session.get(link)
        r.html.render()
        episodes = r.html.find('.ListCaps li a')

        if episodes:
            first_episode = episodes[-1]
            episode_link = first_episode.absolute_links.pop()  
            episode_links_list.append(episode_link)
            print("Enlace del primer episodio:", episode_link)
        else:
            print("No se encontraron episodios disponibles para", link)

    session.close()

    # Pasar episode_links_list a otro script usando subprocess

    print(episode_links_list)
    subprocess.run(["python", "getAllLInks.py"] + episode_links_list)
