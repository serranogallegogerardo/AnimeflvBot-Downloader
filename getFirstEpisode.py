import sys
import json
from requests_html import HTMLSession
import subprocess

if __name__ == "__main__":
    # Check if links were provided as command-line arguments
    if len(sys.argv) < 2:
        print("Please provide links as command-line arguments.")
        sys.exit(1)

    links = sys.argv[1:]

    episode_links_list = []
    session = HTMLSession()

    for link in links:
        # Check if the link is valid
        if not link:
            print(f"Skipping empty link.")
            continue

        try:
            r = session.get(link)
            r.html.render()
            episodes = r.html.find('.ListCaps li a')
        except Exception as e:
            print(f"Error processing link {link}: {e}")
            continue

        # Check if any episodes were found
        if not episodes:
            print(f"No episodes found for link {link}")
            continue

        first_episode = episodes[-1]
        episode_link = first_episode.absolute_links.pop()
        episode_links_list.append(episode_link)
        print(f"First episode link: {episode_link}")

    session.close()

    print(episode_links_list)
    subprocess.run(["python", "getAllLInks.py"] + episode_links_list)