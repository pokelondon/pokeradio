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
				
			},
			parse: function(response){
				this.info =  response.info;
				return response.tracks;
			},
			getTrack: function(id){
				track = this.get(id);
				return {
					'name': track.attributes.name,
					'href': track.attributes.href,
					'artist': track.attributes.artists[0].name,
					'length': track.attributes.length,
					'album': {
						'href': track.attributes.album.href,
					}
				};
			},
			searchNextPage: function(e){
				
			},


		});
		return spotifyResults;

});