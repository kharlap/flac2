import requests  
from bs4 import BeautifulSoup  
import os  
import re  

url = input("URL альбома flac2.com: ")

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
song_titles = soup.find_all('td', class_="fp_title")
album_title = soup.find('h1', class_="album_title")
artist_title = soup.find('div', class_="artist_title").find('a').find('span')

songs = [song.get_text(strip=True) for song in song_titles]
album = album_title.get_text(strip=True)
artist = artist_title.get_text(strip=True)

album_id = re.findall(r'\d+', url)[1]

num_songs = len(songs) - 1

folder_name = f"{artist} - {album}"

os.makedirs(folder_name, exist_ok=True)

for song_number in range(1, num_songs + 1):
    download_url = f"https://dl.flac2.com/Store/flac.php?id={album_id}&sid=9139835f4689ef0244ce48c4fb5f1769&song={song_number}"
    response = requests.get(download_url)
    song_name = songs[song_number]
    with open(os.path.join(folder_name, f"{song_name}.flac"), "wb") as file:
        file.write(response.content)
    print(f"Скачано: {song_name}")