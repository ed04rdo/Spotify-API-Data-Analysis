'''spotipy = Python library for handling API requests (wrapper)'''
''''''
import spotipy
import pandas as pd
import json
from cfg import REDIRECT_URI,CLIENT_SECRET,CLIENT_ID
from spotipy.oauth2 import SpotifyOAuth

playlist_id = '37i9dQZF1EJDMW9b00hM9s'
playlist_features_list = ["added_by","artist", "album", "track_name", "track_id", 
                             "danceability", "energy", "key", "loudness", "mode", "speechiness",
                             "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]

def auth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI))
    return sp


def retrieve_playlist(sp):
    data = sp.user_playlist_tracks(playlist_id=playlist_id)
    
    return data

def song_analysis():
    song = 'One more time'
    track_id = sp.search(song)['tracks']['items'][0]['id']
    bars = sp.audio_analysis(track_id)['bars']
    beats = sp.audio_analysis(track_id)['beats']
    sections = sp.audio_analysis(track_id)['sections']
    df = pd.DataFrame(bars)
    df.insert(0,'song',[song]*len(bars))
    df2 = pd.DataFrame(beats)
    df2.insert(0,'song',[song]*len(beats))
    df3 = pd.DataFrame(sections)
    df3.insert(0,'song',[song]*len(sections))

    df.to_csv('{}_bars.csv'.format(song),index=False)
    df2.to_csv('{}_beats.csv'.format(song),index=False)
    df3.to_csv('{}_sections.csv'.format(song),index=False)

def pd_analysis(data):
    pretty = json.dumps(data,indent=4)
    #print(pretty)
    #print(data['items'][0]['played_at'])
    playlist_df = pd.DataFrame(columns = playlist_features_list)

    for item in data['items']: 
        added_by = item['added_by']['id']
        artist = item['track']['album']['artists'][0]['name']
        album = item['track']['album']['name']
        track_name = item['track']['name']
        track_id = item["track"]["id"]
        track = sp.audio_features(track_id)[0]
        track_features = [track[feature] for feature in playlist_features_list[5:]]
        playlist_df.loc[len(playlist_df)] = [added_by,artist,album,track_name,track_id]+track_features
    
    playlist_df.to_csv('Fusion.csv',encoding='utf-8',index=False)

if __name__ == '__main__':
    sp = auth()
    #data = retrieve_playlist(sp)
    #pd_analysis(data)
    song_analysis()
