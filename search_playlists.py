import sys
import json
import collections

from functools import reduce

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


playlists_to_ignore = ["Bass-ic Bitches",
                       "SoBo's Loco Mojo",
                       "Hotline Miami Mix",
                       "Discover Weekly",
                       "My Shazam Tracks",
                       "Daily Mix 3 - MADE FOR NATHANWM:11/21/17"]

seasonal_playlist_names = ["Spring", "Summer", "Fall", "Winter"]

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
    if playlist_name in playlists_to_ignore:
        return False

    if 'Year of' in playlist_name:
        return False

    is_seasonal_playlist = list(filter(lambda x: x in playlist_name, seasonal_playlist_names))
    if is_seasonal_playlist:
      return False
    
    return True

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

