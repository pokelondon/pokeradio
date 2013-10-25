define([
	'jquery',
	'backbone',
	'urls',
	'underscore',
	'iobind'
	],
	function($, Backbone, urls,_ ,ioBind){
		var playlistResults = Backbone.Collection.extend({

            url: 'playlist',
			socket: window.socket,
			initialize: function(){
				_.bindAll(this, 'playlistUpdate');
				this.ioBind('update', this.playlistUpdate, this);
				socket.emit('get_playlist')

			},
			playlistUpdate: function(data){
				this.reset($.parseJSON(data));
			},
			parse: function(response){
				return response.tracks;
			}

		});
		return playlistResults;

});