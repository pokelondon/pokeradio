define([
	'jquery',
	'backbone',
	'urls',
	'models/Track'],
	function($,Backbone,urls,Track){
		var spotifyResults = Backbone.Collection.extend({
			url: urls.track,
			model: Track,
			parse: function(response){
				return response.tracks;
			}

		});
		return spotifyResults;

});