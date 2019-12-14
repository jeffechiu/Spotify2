import sys
import spotipy
import spotipy.util as util

username = "1215747131"
client_id = "d3a608860b4f4442ad2b0aebba6afeaa"
client_secret = "2daa692e01234f9ca180f4dccef200f6"
redirect_uri = "https://www.spotify.com/us/"
scope = "playlist-read-private"

token = util.prompt_for_user_token(username, scope = scope, client_id = client_id, client_secret=client_secret, redirect_uri=redirect_uri)

def get_playlist(sp):
	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
		if playlist['name'] == '318 Playlist':
			p = playlist
	return p

def get_tracks(sp, playlist):
	tracks = []
	trks = sp.user_playlist_tracks(username, playlist['id'])
	#print(type(trks))
	for song in trks['items']:
		tracks += [song['track']]
		#print(song['track']['name'])
	return tracks

def audio_id(sp, tracks):
	ids = []
	for track in tracks:
		ids+= [track['id']]
	return ids

def audio_analysis(sp, ids):
	features = sp.audio_features(ids)
	return features

def get_acoustic(sp, features):
	acous = []
	for track in features:
		acous += [track['key']]
	return acous

if token:
	sp=spotipy.Spotify(auth=token)
	p = get_playlist(sp)
	#print(p)
	#print(type(p))
	trks = get_tracks(sp, p)
	ids = audio_id(sp, trks)
	features = audio_analysis(sp, ids)
	#print(ids)
	acous = get_acoustic(sp, features)
	print(acous)
	#print(features)
	#print(len(features))
	#print(type(features))
else:
	print("can't get token for", username)

