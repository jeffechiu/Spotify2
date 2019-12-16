from flask import Flask, render_template, url_for, flash, redirect
from appl import app
from appl.models import Playlist, Track
from appl.models import addRecsToDatabase

from appl import playlists as p

sp = p.sp
playlist = p.get_playlists(sp)

@app.route('/')
def index():
    return render_template('index.html', playlists=playlist)

@app.route('/playlist/<playlist_id>')
def view(playlist_id):
	playlist = Playlist.query.get_or_404(playlist_id)
	trks = p.get_trks(sp, playlist_id)
	tracks = p.get_tracks(sp, playlist_id)
	attributes = ["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature", "valence"]
	ids = p.audio_id(sp, tracks)
	features = p.audio_analysis(sp, ids)
	lenat = len(attributes)
	recats = []
	for i in range(lenat):
		recats += [p.get_attributes(sp, features, attributes[i])]
	recats += [p.get_popularity(sp, tracks)]
	acous, dance, durat, energ, instr, key, liven = recats[0][2], recats[1][2], recats[2][2], recats[3][2], recats[4][2], recats[5][2], recats[6][2]
	loudn, mode, speec, tempo, times, valen, popul = recats[7][2], recats[8][2], recats[9][2], recats[10][2], recats[11][2], recats[12][2], recats[13][2]
	acous1 = str((acous/1)*100)+"%"
	dance1 = str((dance/1)*100)+"%"
	energ1 = str((energ/1)*100)+"%"
	instr1 = str((instr/1)*100)+"%"
	liven1 = str((liven/1)*100)+"%"
	loudn1 = str(((60+loudn)/60)*100)+"%"
	speec1 = str((speec/1)*100)+"%"
	valen1 = str((valen/1)*100)+"%"
	popul1 = str(popul)+"%"
	playlist = sp.user_playlist(p.username, playlist_id)
	return render_template('view.html', pid=playlist_id, tracks=trks, acous=acous, acous1=acous1, dance=dance, durat=durat, energ=energ, instr=instr, key=key, liven=liven, loudn=loudn, mode=mode, speec=speec, tempo=tempo, times=times, valen=valen, popul=popul, dance1=dance1, energ1=energ1, instr1=instr1, liven1=liven1, loudn1=loudn1, speec1=speec1, valen1=valen1, popul1=popul1, playlist=playlist)

@app.route('/recommendations/<playlist_id>')
def rec(playlist_id):
	tracks = p.get_tracks(sp, playlist_id)
	allPoss = p.get_sets_of_5(sp, tracks)
	recs = p.get_recs_all(sp, allPoss)
	disp = p.display(recs)
	corres = p.correspond(sp, disp)
	addRecsToDatabase(sp, corres)
	return render_template('rec.html', corres=corres, pid=playlist_id)

@app.route('/song/<track_id>')
def vtrack(track_id):
	#track = Track.query.get_or_404(track_id)
	td = p.track_details(sp, track_id)
	artists = p.get_artists(sp, td)
	feature = sp.audio_features(track_id)
	attributes = ["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature", "valence"]
	features=feature[0]
	acous1=str((features["acousticness"])*100)+"%"
	dance1=str((features["danceability"])*100)+"%"
	energ1=str((features["energy"])*100)+"%"
	instr1=str(features["instrumentalness"]*100)+"%"
	liven1=str(features["liveness"]*100)+"%"
	loudn1=str(((60+features["loudness"])/60)*100)+"%"
	speec1=str(features["speechiness"]*100)+"%"
	valen1=str(features["valence"]*100)+"%"
	popul1=str(td["popularity"])+"%"
	return render_template('vsong.html', tid = track_id, td=td, artists=artists, features=feature, acous1=acous1, dance1=dance1, energ1=energ1, instr1=instr1, liven1=liven1, loudn1=loudn1, speec1=speec1, valen1=valen1, popul1=popul1)