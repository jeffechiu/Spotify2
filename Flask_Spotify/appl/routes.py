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
	return render_template('view.html', pid=playlist_id, tracks=trks)

@app.route('/recommendations/<playlist_id>')
def rec(playlist_id):
	tracks = p.get_tracks(sp, playlist_id)
	allPoss = p.get_sets_of_5(sp, tracks)
	recs = p.get_recs_all(sp, allPoss)
	disp = p.display(recs)
	corres = p.correspond(sp, disp)
	addRecsToDatabase(sp, corres)
	return render_template('rec.html', corres=corres)

@app.route('/song/<track_id>')
def vtrack(track_id):
	#track = Track.query.get_or_404(track_id)
	td = p.track_details(sp, track_id)
	artists = p.get_artists(sp, td)
	features = sp.audio_features(track_id)
	return render_template('vsong.html', tid = track_id, td=td, artists=artists, features=features)