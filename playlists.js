var request = require("request");
//Jeffrey's Spotify User ID
var user_id = "1215747131";
//Access token to be changed every time
var token = "Bearer BQBfQK0r3q4WfE5zBFwrOE-LS2DhqFEEKs_yYk5fZHk-QetjpWQgR8dFuZWwYWOdBWroIfhy4rQ66jYqt448K7Kv6dW-hm0SUmsxEup-j5_smh2cP4gmWRE0jPYUEwpHJxx69AGuj_tOiIhFNCBdNBB92qDYWNc";
var playlists_url = "https://api.spotify.com/v1/users/"+user_id+"/playlists";

request({url: playlists_url, headers:{"Authorization":token}}, function(err, res){
	if (res){
		var playlists = JSON.parse(res.body);
		//console.log(JSON.stringify(playlists.items, null, " "));
		var playlist_url = playlists.items[0].href;
		request({url: playlist_url, headers:{"Authorization":token}}, function(err, res){
			if (res){
				var playlist = JSON.parse(res.body);
				console.log("playlist: "+playlist.name);
				//console.log(playlist.tracks)
				playlist.tracks.items.forEach(function(track){
					console.log(track.track.name);
				});
				//playlist.tracks.forEach(track => console.log(track.track.name));
			}
		})
	}
})