import spotipy
import sys
import dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from youtube_videos import youtube_search
import youtube_dl

load_dotenv()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
song_list = []


def show_tracks(tracks):
    for item in enumerate(tracks['items']):
        track = item[1]['track']
        song = "%32.32s - %s" % (track['artists'][0]['name'],
                                 track['name'])
        song_list.append(song.strip())


sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = sp.playlist(sys.argv[1], fields="tracks,next")
tracks = results['tracks']
show_tracks(tracks)
while tracks['next']:
    tracks = sp.next(tracks)
    show_tracks(tracks)

for song in song_list:
    video = youtube_search(song)[1][0]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(
            ["https://www.youtube.com/watch?v={}".format(video['id']['videoId'])])
