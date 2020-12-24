import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

def get_song_data(results):
    song_list = []
    for idx, item in enumerate(results['items']):
        track = item['track']
        song_data = {
            'artist_name': track['artists'][0]['name'],
            'song_name': track['name'],
            'image_url': track['album']['images'][0]['url'],
            'image_width': track['album']['images'][0]['width'],
            'image_height': track['album']['images'][0]['height']
        }
        song_list.append(song_data)
        #print(idx, track['artists'][0]['name'], " – ", track['name'])
    return song_list

def get_all_user_saved_tracks(sp):
    column_names = [
        'artist_name',
        'song_name',
        'image_url',
        'image_width',
        'image_height'
    ]
    first_page_tracks = 'https://api.spotify.com/v1/me/tracks?offset=0&limit=20'

    df = pd.DataFrame(columns = column_names)

    while True :
        results = sp._get(first_page_tracks)
        df = df.append(get_song_data(results), ignore_index=False)
        if not results['next'] == None:
            first_page_tracks = results['next']
        else:
            break
    
    return df

def main():

    auth_manager = SpotifyOAuth(
        redirect_uri="http://example.com", 
        scope="user-library-read",
        open_browser=False
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    df_result = get_all_user_saved_tracks(sp)

    df_result.to_csv('song_data.csv',index=False)
   

if __name__  == '__main__':
    main()

"""
TODO:
[] Delete duplicated songs
[] Download song from yooutube
[] Change tag mp3
[] Keep csv as database and other with new results, then only process new songs
[] Keep track of some variables for automation.
[] Add support for download mood playlist
"""