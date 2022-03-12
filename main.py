import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

YOUR_APP_CLIENT_ID = ""
YOUR_APP_CLIENT_SECRET = ""

time = input("What year do you want to travel to? Type in the format YYYY-MM-DD: ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{time}/")
data_songs = response.text

soup = BeautifulSoup(data_songs, "html.parser")
class_name ="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 " \
            "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 " \
            "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
data = soup.find_all("h3", id="title-of-a-story", class_=class_name)
songs_list = []
for song in data:
    text = song.getText()
    stripped_text = text.strip()
    songs_list.append(stripped_text)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=YOUR_APP_CLIENT_ID,
        client_secret=YOUR_APP_CLIENT_SECRET,
        redirect_uri="https://example.com/callback/",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
# year = date.split("-")[0]
year = time.split("-")[0]

for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{time} Billboard 100", collaborative=False,public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)