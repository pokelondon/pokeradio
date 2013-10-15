define([
	'jquery',
	'backbone',
	'underscore',
	'urls'],
	function($,Backbone,_urls){
		console.log(urls)
		var spotifyResults = Backbone.Collection.extend({
			url: urls.track,
			parse: function(response) {
	    		return response.tracks;
	  		}

		});

		return spotifyResults;

});