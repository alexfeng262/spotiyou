import youtube_dl
base_url = 'https://www.youtube.com/watch?v='
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    test = ydl.extract_info('ytsearch1: Backstreet Boys - I Want It That Way',download=False)
    
    for video in test['entries']:
        #print(video['id'])
        ydl.download([base_url+video['id']])
    