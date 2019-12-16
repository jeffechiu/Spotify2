from appl import db
from appl import playlists as p

class Playlist(db.Model):
	id = db.Column(db.String(200), primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	tracks = db.relationship('Track', backref='owner')

	def __repr__(self):
		return f"Playlist('{self.name}')"

class Track(db.Model):
	id = db.Column(db.String(200), primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	playlist_id = db.Column(db.String(200), db.ForeignKey('playlist.id'), nullable=True)

	def __repr__(self):
		return f"Track('{self.name}')"

db.drop_all()
db.create_all()

sp = p.sp
playlists = p.get_playlists(sp)
for playlist in playlists:
	p1 = Playlist(id=playlist['id'], name = playlist['name'])
	db.session.add(p1)
	#print(playlist['tracks'])
	for track in playlist['tracks']:
		print(track)
		if db.session.query(Track.id).filter_by(name=track['track']['name']).scalar() is not None:
			t1 = Track(id=track['track']['id'], name=track['track']['name'], playlist_id=p1.id)
			db.session.add(t1)

	db.session.commit()

def addRecsToDatabase(sp, corres):
	for track in corres:
		td = p.track_details(sp, track['id'])
		if db.session.query(Track.id).filter_by(name=td['name']).scalar() is not None:
			t1 = Track(id=track['id'], name=td['name'], playlist_id=None)
			db.session.add(t1)
	db.session.commit()
