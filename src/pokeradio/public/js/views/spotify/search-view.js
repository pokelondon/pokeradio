define(['jquery',
		'backbone',
		'underscore',
		'collections/Tracks',
		'text!template/spotify/track-listing.html'
		],
		function($,Backbone,_,Tracks,tl_template){
			var searchView = Backbone.View.extend({
				el: $('.container'),
				
				initialize: function(){
					this.tracks = new Tracks();
				},
				events:{
					'submit #searchForm': 'search',
					'click .track-listing-container li': 'add_track'
				},
				search: function(e){
					this.tracks.fetch({
						data : $.param(
							{q: $('#searchInput').val()}
						),
						success:function(data){
							var template = _.template(tl_template, {metadata:data.models});
							$('.track-listing-container').html(template);
						}
					});
					return false;
				},
				add_track:function(e){
					var track = this.tracks.get($(e.currentTarget).data('href'));
					var track_payload = {};
					track_payload.name = track.attributes.name;
					track_payload.href = track.attributes.href;
					track_payload.artist = track.attributes.artists[0].name;
					socket.emit('add_track',JSON.stringify(track_payload));
				}
			});
			return searchView;
		});