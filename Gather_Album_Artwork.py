import sys
sys.path.insert(1, '../Spotify_Release_Pi/src/')

import General_Spotify_Helpers as gsh

import sqlite3
from PIL import Image, ImageStat
from io import BytesIO
import glob
import requests

# Grab every track from Master Playlist
# populate track_info_db
# Keep a unique set of album_id's
# Grab every unique album_id image in max resolution

SCOPE = "playlist-read-private " \
        "playlist-read-collaborative "

TRACK_INFO_DB = "track_info.db"
MASTER_PLAYLIST_ID = "6kGQQoelXM2YDOSmqUUzRw"
# Smaller playlist to test with
# MASTER_PLAYLIST_ID = "196H9SeTzhVNDf5rBtTUuu"

spotify = gsh.GeneralSpotifyHelpers(SCOPE)

conn = sqlite3.connect(TRACK_INFO_DB)
conn.execute(f'''CREATE TABLE IF NOT EXISTS 'info'(
        track_name TEXT NOT NULL,
        artist_name TEXT NOT NULL,
        album_name TEXT NOT NULL,
        album_id TEXT NOT NULL);''')

tracks_data = spotify.get_playlist_tracks(MASTER_PLAYLIST_ID, track_info=['name'], album_info=['id', 'name', 'images'], artist_info=['name'])

album_ids = []
for track in tracks_data:
    print(f"Getting {track['name']} - { track['artists'][0]['name']} - {track['album_name']} {track['album_id']}")
    # Skip local tracks
    if track['album_id'] is None:
        continue
    conn.execute('INSERT INTO info (track_name,artist_name,album_name,album_id) VALUES (?,?,?,?)',
                 (track['name'], track['artists'][0]['name'], track['album_name'], track['album_id']))
    if track['album_id'] not in album_ids:
        print("\t Grabbing Image")
        album_ids.append(track['album_id'])
        img = Image.open(BytesIO(requests.get(track["album_images"][0]['url']).content))
        img.save(f"Albums/{track['album_id']}.png")

conn.commit()
conn.close()