import sys
import spotipy
import spotipy.util as util
import operator

username = "1215747131"
client_id = "d3a608860b4f4442ad2b0aebba6afeaa"
client_secret = "2daa692e01234f9ca180f4dccef200f6"
redirect_uri = "https://www.spotify.com/us/"
scope = "playlist-read-private"

token = util.prompt_for_user_token(username, scope = scope, client_id = client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp=spotipy.Spotify(auth=token)

def get_playlists(sp):
	playlists = sp.user_playlists(username)
	p = []
	for playlist in playlists['items']:
		p += [{'name': playlist['name'], 'images': playlist['images'][0]['url'], 'href': 'https://open.spotify.com/playlist/'+playlist['id'], 'id': playlist['id'], 'tracks': sp.user_playlist_tracks(username, playlist['id'])['items']}]
	return p

def get_trks(sp, pid):
	tracks = []
	trks = sp.user_playlist_tracks(username, pid)
	for song in trks['items']:
		#print(song)
		tracks += [{'name': song['track']['name'], 'artists': get_artists(sp, song['track']), 'href': 'https://open.spotify.com/track/'+song['track']['id'], 'id': song['track']['id']}]
	return tracks

def get_playlist(sp):
	playlists = sp.user_playlists(username)
	for playlist in playlists['items']:
		if playlist['name'] == '318 Playlist':
			p = playlist
	return p

def get_tracks(sp, pid):
	tracks = []
	trks = sp.user_playlist_tracks(username, pid)
	#print(type(trks))
	for song in trks['items']:
		tracks += [song['track']]
		#print(song['track']['name'])
	return tracks

def get_sets_of_5(sp, tracks):
	ans = []
	loops = len(tracks)-4
	trlen = len(tracks)
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
	return [a, b, c]

def get_popularity(sp, tracks):
	popul = []
	for track in tracks:
		popul += [track['popularity']]
	a = min(popul)
	b = max(popul)
	c = sum(popul)/len(popul)
	return [a, b, c]

def get_recs(sp, ids, recats):
	print("recats is ", recats)
	return sp.recommendations(seed_tracks=ids, country="US", limit=10, min_acousticness=recats[0][0], max_acousticness=recats[0][1], target_acousticness=recats[0][2], min_danceability=recats[1][0], max_danceability=recats[1][1], target_danceability=recats[1][2], min_duration_ms=recats[2][0], max_duration_ms=recats[2][1], target_duration_ms=round(recats[2][2]), min_energy=recats[3][0], max_energy=recats[3][1], target_energy=recats[3][2], min_instrumentalness=recats[4][0], max_instrumentalness=recats[4][1], target_instrumentalness=recats[4][2], min_key=recats[5][0], max_key=recats[5][1], target_key=round(recats[5][2]), min_liveness=recats[6][0], max_liveness=recats[6][1], target_liveness=recats[6][2], min_loudness=recats[7][0], max_loudness=recats[7][1], target_loudness=recats[7][2], min_mode=recats[8][0], max_mode=recats[8][1], target_mode=round(recats[8][2]), min_speechiness=recats[9][0], max_speechiness=recats[9][1], target_speechiness=recats[9][2], min_tempo=recats[10][0], max_tempo=recats[10][1], target_tempo=recats[10][2], min_time_signature=recats[11][0], max_time_signature=recats[11][1], target_time_signature=round(recats[11][2]), min_valence=recats[12][0], max_valence=recats[12][1], target_valence=recats[12][2], min_popularity=recats[13][0], max_popularity=recats[13][1], target_popularity=round(recats[13][2]))

def get_recs_all(sp, allPoss):
	ans = dict()
	attributes = ["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature", "valence"]
	for poss in allPoss:
		ids = audio_id(sp, poss)
		features = audio_analysis(sp, ids)
		lenat = len(attributes)
		recats = []
		for i in range(lenat):
			recats += [get_attributes(sp, features, attributes[i])]
		recats += [get_popularity(sp, poss)] 
		print(recats)
		recs = get_recs(sp, ids, recats)
		for track in recs['tracks']:
			if track['id'] not in ans:
				ans[track['id']] = 0
			ans[track['id']] += 1
		print(ans)
	return ans

def get_artists(sp, track):
	if len(track['artists']) == 1:
		return track['artists'][0]['name']
	else:
		print("else runs")
		a = []
		ans=""
		for artist in track['artists']:
			a += [artist['name']]
		for i in range(len(a)):
			if i == 0:
				ans += a[i]
			else:
				ans += ", "
				ans += a[i]
		return ans

def display(recs):
	l = sorted(recs.items(), key=operator.itemgetter(1), reverse=True)
	ans = '''
	Top 10 Recommended Songs

	'''
	return l

def correspond(sp, s):
	ans = []
	for item in s:
		print("item is ", item)
		i = item[0]
		t = sp.track(i)
		print("t is ", t)
		ans += [{"name": t['name'], "artists": get_artists(sp, t), "id": t["id"], "href": 'https://open.spotify.com/track/'+t["id"]}]
	return ans

def track_details(sp, id):
	return sp.track(id)



#if token:
	#sp=spotipy.Spotify(auth=token)
	#p = get_playlist(sp)
	#print(p)
	#print(type(p))
	#trks = get_tracks(sp, p)
	#print(trks)
	#print(len(trks))
	#print(type(trks))
	#allPoss = get_sets_of_5(sp, trks)
	#print(type(allPoss))
	#print(len(allPoss[0]))
	#ans = get_sets_of_5(sp, [0, 1, 2, 3, 4, 5, 6])
	#print(len(ans))
	#ans = get_recs_all(sp, allPoss)
	#l = display(ans)
	#print(l)
	#print(recats)
	#print(features)
	#print(len(features))
	#print(type(features))
	#recs = get_recs(sp, ids, recats)
	#for track in recs['tracks']:
		#print(track['name'])
	#print(ids)
#else:
	#print("can't get token for", username)

