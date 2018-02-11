import sys
import json
import collections
import calendar

from functools import reduce

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

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Too many arguments")
    print_usage()
    sys.exit()

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists(username)
list_of_tracks = []
for playlist in playlists['items']:
    playlist_name = playlist['name']
    if is_monthly_playlist(playlist_name):
        playlist = sp.user_playlist(username, playlist['id'])
        # print_playlist_tracks(playlist)
        track_names = {item['track']['name'] for item in playlist['tracks']['items']
                                              if item['track']}
        list_of_tracks.extend(track_names)
# print("List of tracks length:", len(list_of_tracks))
duplicate_tracks = [track for track, count in collections.Counter(list_of_tracks).items() if count > 1]
print("Duplicate tracks:", duplicate_tracks)

