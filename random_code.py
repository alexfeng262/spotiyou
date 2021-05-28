import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import logging
import youtube_dl
import os
import shutil
import re
import eyed3

playlist_id = '37i9dQZF1DX5Ejj0EkURtP'
url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
auth_manager = SpotifyOAuth(
        redirect_uri="http://example.com", 
        scope="user-library-read",
        open_browser=False
    )
sp = spotipy.Spotify(auth_manager=auth_manager)

results = sp._get(url)
print(results)
