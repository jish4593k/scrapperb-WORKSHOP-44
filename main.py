import os
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://freemidi.org/'
genres = ['genre-rock', 'genre-pop', 'genre-dance-eletric', 'genre-jazz']

# Helper function to clean up file names
def clean_file_name(name):
    return name.replace('/', ' ').replace('\t', ' ')

# Create a session for making requests
session = requests.Session()

# Iterate through the specified genres
for genre in genres:
    url = BASE_URL + genre
    folder_name = genre
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Retrieve the web page content
    html = session.get(url).content
    soup = BeautifulSoup(html, 'lxml')

    # Extract links to artists within the genre
    genre_links = soup.select(".genre-link-text > a")

    for genre_link in genre_links:
        artist_id = genre_link['href']
        artist_name = genre_link.text.strip()
        artist_url = BASE_URL + artist_id

        # Retrieve the artist's page content
        html = session.get(artist_url).content
        soup = BeautifulSoup(html, 'lxml')

        # Extract links to songs by the artist
        artist_links = soup.select('.artist-song-cell a')

        for artist_link in artist_links:
            song_url = BASE_URL + artist_link['href']
            song_id = song_url.split('-')[1]
            song_name = artist_link.text.strip()
            song_path = clean_file_name(f'{artist_name} - {song_name}')
            file_name = f'{folder_name}/{song_path}.mid'

            if not os.path.isfile(file_name):
                print(file_name)

                # Retrieve the song page
                session.get(song_url)

                # Download the MIDI file
                download_url = BASE_URL + 'getter-' + song_id
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'
                }
                headers.update({"Referer": song_url})

                r = session.get(download_url, headers=headers)
                with open(file_name, 'wb') as f:
                    f.write(r.content)
