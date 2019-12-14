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

def get_sets_of_5(sp, tracks):
	ans = []
	loops = len(tracks)-4
	trlen = len(tracks)
	print(trlen)
	for i1 in range(0, loops):
		for i2 in range(i1+1, min(i1+1+loops, trlen)):
			for i3 in range(i2+1, min(i2+1+loops, trlen)):
				for i4 in range(i3+1, min(i3+1+loops, trlen)):
					for i5 in range(i4+1, min(i4+1+loops, trlen)):
						trk = [tracks[i1], tracks[i2], tracks[i3], tracks[i4], tracks[i5]]
						status = "add"
						#print(len(trk))
						for i in range(len(trk)):
							#print(i)
							for j in range(len(trk)):
								if i != j:
									if trk[i] == trk[j]:
										status = "no"
									#if j > i and (trk[i]['id'] > trk[j]['id']):
									#	print("runs", i, j)
										#print(type(trk[i]['id']))
									#	print(trk[i]['id'] > trk[j]['id'])
									#	status = "no"
						if status == "add":
							ans += [trk]
						#print(ans)
	return ans



def audio_id(sp, tracks):
	ids = []
	for track in tracks:
		ids+= [track['id']]
	return ids

def audio_analysis(sp, ids):
	features = sp.audio_features(ids)
	return features

def get_attributes(sp, features, attribute):
	attributes = []
	for track in features:
		attributes += [track[attribute]]
	a = min(attributes)
	b = max(attributes)
	c = sum(attributes)/len(attributes)
	return a, b, c

def get_popularity(sp, tracks):
	popul = []
	for track in tracks:
		popul += [track['popularity']]
	a = min(popul)
	b = max(popul)
	c = sum(popul)/len(popul)
	return a, b, c

def get_recs(sp, ids, recats):
	return sp.recommendations(seed_tracks=ids, country="US", limit=10, min_acousticness=recats[0][0], max_acousticness=recats[0][1], target_acousticness=recats[0][2], min_danceability=recats[1][0], max_danceability=recats[1][1], target_danceability=recats[1][2], min_duration_ms=recats[2][0], max_duration_ms=recats[2][1], target_duration_ms=round(recats[2][2]), min_energy=recats[3][0], max_energy=recats[3][1], target_energy=recats[3][2], min_instrumentalness=recats[4][0], max_instrumentalness=recats[4][1], target_instrumentalness=recats[4][2], min_key=recats[5][0], max_key=recats[5][1], target_key=round(recats[5][2]), min_liveness=recats[6][0], max_liveness=recats[6][1], target_liveness=recats[6][2], min_loudness=recats[7][0], max_loudness=recats[7][1], target_loudness=recats[7][2], min_mode=recats[8][0], max_mode=recats[8][1], target_mode=round(recats[8][2]), min_speechiness=recats[9][0], max_speechiness=recats[9][1], target_speechiness=recats[9][2], min_tempo=recats[10][0], max_tempo=recats[10][1], target_tempo=recats[10][2], min_time_signature=recats[11][0], max_time_signature=recats[11][1], target_time_signature=round(recats[11][2]), min_valence=recats[12][0], max_valence=recats[12][1], target_valence=recats[12][2], min_popularity=recats[13][0], max_popularity=recats[13][1], target_popularity=round(recats[13][2]))

if token:
	sp=spotipy.Spotify(auth=token)
	p = get_playlist(sp)
	#print(p)
	#print(type(p))
	trks = get_tracks(sp, p)
	#print(trks)
	#print(len(trks))
	#print(type(trks))
	ans = get_sets_of_5(sp, trks)
	#ans = get_sets_of_5(sp, [0, 1, 2, 3, 4, 5, 6])
	#print(len(ans))
	print(len(ans))
	ids = audio_id(sp, trks)
	features = audio_analysis(sp, ids)
	#print(ids)
	attributes = ["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature", "valence"]
	lenat = len(attributes)
	recats = []
	for i in range(lenat):
		recats += [get_attributes(sp, features, attributes[i])]
	recats += [get_popularity(sp, trks)] 
	#print(recats)
	#print(features)
	#print(len(features))
	#print(type(features))
	#recs = get_recs(sp, ids, recats)
	#for track in recs['tracks']:
		#print(track['name'])
	#print(ids)
else:
	print("can't get token for", username)

