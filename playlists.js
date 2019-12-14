var request = require("request");
//Jeffrey's Spotify User ID
var user_id = "1215747131";
//Access token to be changed every time
var token = "Bearer BQCH68Lo48SQAJjRXsP4FdgT7VBPGyJP7yz8qzHaMA1rRi3Jfr1HYiOy3VJDbjeP-VgYWXGC1-p6jmEHlwGCB3yM2mrP0wqqql2rrhaDODimLQmaGaPGsiAmorl9Buz22uy-Pg8509pVQ05vPw";
var playlists_url = "https://api.spotify.com/v1/users/"+user_id+"/playlists";
var tracks = [];

request({url: playlists_url, headers:{"Authorization":token}}, function(err, res){
	if (res){
		var playlists = JSON.parse(res.body);
		//console.log(JSON.stringify(playlists.items, null, " "));
		//get first playlist in list of playlists
		var playlist_url = playlists.items[0].href;
		request({url: playlist_url, headers:{"Authorization":token}}, function(err, res){
			if (res){
				//get all tracks in a playlist and add them to an array variable
				var playlist = JSON.parse(res.body);
				//var trks=[];
				console.log("playlist: "+playlist.name);
				//console.log(playlist.tracks)
				playlist.tracks.items.forEach(function(track){
					tracks.push(track.track);
				});
				//playlist.tracks.forEach(track => console.log(track.track.name));
				console.log(tracks.length);
				//tracks = trks;
				//postman.setGlobalVariable("trks", trks)
			}
		})
		//console.log(trks);
	}
});
console.log(tracks.length);