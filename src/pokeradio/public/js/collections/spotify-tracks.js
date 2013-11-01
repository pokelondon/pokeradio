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
				return response.tracks;
			},
			getAlbumArt: function(models, resp){

			}


		});
		return spotifyResults;

});