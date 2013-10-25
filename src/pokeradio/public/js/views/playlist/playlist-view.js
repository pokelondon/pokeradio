define(['jquery',
		'backbone',
		'underscore',
		'collections/Playlist',
		'text!template/playlist.html',
		],
		function($, Backbone, _, Playlist, pl_template){
			var playlistView = Backbone.View.extend({
				el: $('.container'),

				initialize: function(){
					_.bindAll(this, "render");
					this.Playlist = new Playlist();
					this.Playlist.on('reset', this.append, this);
				},
				append: function(data){
					console.log(data);
					var template = _.template(pl_template, {metadata:data.models});
					$('.playlist').html(template);
				}
			
			});
			return playlistView;
		});