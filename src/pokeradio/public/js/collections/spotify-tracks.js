define([
	'jquery',
	'backbone',
	'urls',
	'models/spotify-track'],
	function($,Backbone,urls,Track){
		var spotifyResults = Backbone.Collection.extend({
			url: urls.track,
			model: Track,
			initialize: function(){
				this.on('sync', this.getAlbumArt);
			},
			parse: function(response){
				return response.tracks;
			},
			getAlbumArt: function(models, resp){
				href = models.pluck('href');
				console.log(href);
				href = href.replace(/spotify/g,"spotify-WW");
				window.socket.emit('get_album_art', href);

			}


		});
		return spotifyResults;

});