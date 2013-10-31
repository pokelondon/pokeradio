define([
	'jquery',
	'backbone',
	'urls',
	'underscore',
	'iobind',
	'models/mopidy-track'
	],
	function($, Backbone, urls,_ ,ioBind, MopidyTrack){
		var playlistResults = Backbone.Collection.extend({

            url: 'playlist',
			socket: window.socket,
			model: MopidyTrack,
			initialize: function(){
				_.bindAll(this, 'playlistFetch', 'playlistUpdate', 'progress');
				this.ioBind('fetch', this.playlistFetch, this);
				this.ioBind('update', this.playlistUpdate, this);
				this.ioBind('progress', this.progress, this);
				socket.emit('playlist','fetch');

			},
			playlistFetch: function(data){
				// All tracks passed 
				console.log(data);
				this.reset($.parseJSON(data));
			},
			playlistUpdate: function(data){
				//Single track is passed so we check if its a new track or played track.
				data = $.parseJSON(data);
				console.log(data);
				if(data.played){
					this.remove(this.get(data.id));
				}else {
					this.add(data);
				}
				
			},
			progress: function(data){
				this.trigger('progressUpdate', $.parseJSON(data));

			}

		});
		return playlistResults;

});