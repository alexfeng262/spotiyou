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
logging.basicConfig(level=logging.INFO, 
                    #bfilename=cfg.LOG_FILE_DIR, #'../logs/myfirstlog.log',
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

base_url = 'https://www.youtube.com/watch?v='
SAVE_PATH = 'tmp'
SONG_PATH = 'songs/liked_songs/'  
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'outtmpl':SAVE_PATH + '/%(title)s.%(ext)s'
}
def download_youtube(song_name):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        test = ydl.extract_info(f'ytsearch1: {song_name}',download=False)
        ydl.download([base_url+test['entries'][0]['id']])
            
def get_song_data(results):
    song_list = []
    for item in results['items']:
        track = item['track']
        song_data = {
            'artist_name': track['artists'][0]['name'],
            'song_name': track['name'],
            'album_name': track['album']['name'],
            'spotify_id': track['id'],
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
        'album_name',
        'spotify_id',
        'image_url',
        'image_width',
        'image_height'
    ]
    first_page_tracks = 'https://api.spotify.com/v1/me/tracks?offset=0&limit=20'

    df = pd.DataFrame(columns = column_names)
    logger.info('Getting all user saved tracks, please wait...')
    while True :
        results = sp._get(first_page_tracks)
        df = df.append(get_song_data(results), ignore_index=False)
        if not results['next'] == None:
            first_page_tracks = results['next']
        else:
            logger.info('Finished')
            break
    
    return df

def set_song_tag(song_filename, row):
    audiofile = eyed3.load(song_filename)
    audiofile.tag.artist = row['artist_name'].values[0]
    audiofile.tag.title = row['song_name'].values[0]
    audiofile.tag.album = row['album_name'].values[0]
    audiofile.tag.save()

def download_song(row):
    # for idx, row in db.iterrows():
    song_name = f"{row['artist_name'].values[0]} - {row['song_name'].values[0]}"
    download_youtube(song_name)
    downloaded_filename = os.listdir(SAVE_PATH)[0]
    
    song_name = re.sub('[^A-Za-z0-9\-\s\'\(\)ñÑ]', '_', song_name)

    shutil.move(
        os.path.join(SAVE_PATH,downloaded_filename),
        os.path.join(SONG_PATH,song_name+'.mp3')
    )
    set_song_tag(os.path.join(SONG_PATH,song_name+'.mp3'), row)
    logger.info(f'Search for --> {song_name}')
    logger.info(f'Downloaded audio title -> {downloaded_filename}')



if __name__  == '__main__':
    df_database = pd.read_csv('database.csv')
    
    auth_manager = SpotifyOAuth(
        redirect_uri="http://example.com", 
        scope="user-library-read",
        open_browser=False
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    df_query = get_all_user_saved_tracks(sp)
    df_query = df_query.drop_duplicates(subset=['artist_name','song_name'])
    
    # Create set of ids
    set_database = set(df_database['spotify_id'])
    set_query = set(df_query['spotify_id'])

    # Get difference between sets
    diff = set_query.difference(set_database)
    
    for idx in diff:
        row = df_query[df_query['spotify_id']==idx]
        
        df_database = df_database.append(row)
        download_song( row)
    #print(df_database)
    df_database.to_csv('database.csv',index=False)
    logger.info(f'Added {len(diff)} songs to database')
    #download_from_database(df_database)
    
"""
TODO:
[x] Delete duplicated songs
[x] Download song from youtube
[x] Rename downloaded song
[x] Add album info
[x] Change tag mp3
[x] Keep csv as database and other with new results, then only process new songs
[] Keep track of some variables for automation.
[] Add support for download mood playlist
"""