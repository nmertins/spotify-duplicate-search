import calendar
from collections import Counter

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def print_usage():
    print("usage: python search_playlists.py username")


def print_playlist_tracks(playlist):
    print(playlist['name'])
    print('-----------------')
    track_items = playlist['tracks']['items']
    for item in track_items:
        track = item['track']
        if track:
            print(track['name'])
    print('')


def is_monthly_playlist(playlist_name):
    return playlist_name.split()[0] in calendar.month_name


username = 'nathanwm'

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists(username)
tracks_dict = {}
for playlist in playlists['items']:
    if is_monthly_playlist(playlist['name']):
        playlist = sp.user_playlist(username, playlist['id'])
        for track_item in playlist['tracks']['items']:
            if track_item['track']:
                track_name = track_item['track']['name']
                if track_name not in tracks_dict.keys():
                    tracks_dict[track_name] = []
                tracks_dict[track_name].append(track_item['track']['artists'][0]['name'])

potential_duplicate_tracks = [track for track in tracks_dict.keys() if len(tracks_dict[track]) > 1]
duplicate_tracks = []
for track in potential_duplicate_tracks:
    artist_counter = Counter(tracks_dict[track])
    for artist, count in artist_counter.items():
        if count > 1:
            duplicate_tracks.append(track)

print("Duplicate tracks:", duplicate_tracks)

for track in duplicate_tracks:
    for playlist in playlists['items']:
        if is_monthly_playlist(playlist['name']):
            playlist = sp.user_playlist(username, playlist['id'])
            track_names = {item['track']['name'] for item in playlist['tracks']['items'] if item['track']}
            if track in track_names:
                print(track, "is in", playlist['name'])
