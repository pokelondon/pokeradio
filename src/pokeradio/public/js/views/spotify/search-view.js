define(['jquery',
		'backbone',
		'underscore',
		'collections/spotify-tracks',
		'iobind',
		'text!template/spotify/track-listing.html'
		],
		function($, Backbone,_ , SpotifyTracks, ioBind, tl_template){
			var searchView = Backbone.View.extend({
				el: $('.container'),
				
				initialize: function(){
					this.spotifyTracks = new SpotifyTracks();
				},
				events:{
					'submit #searchForm': 'search',
					'click .track-listing-container li': 'add_track'
				},
				search: function(e){
					this.spotifyTracks.fetch({
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
					var track = this.spotifyTracks.get($(e.currentTarget).data('href'));
					console.log(track);
					var track_payload = {
						'name': track.attributes.name,
						'href': track.attributes.href,
						'artist': track.attributes.artists[0].name,
						'length': track.attributes.length,
						'album_href': track.attributes.album.href
					};
					socket.emit('add_track',JSON.stringify(track_payload));
				}
			});
			return searchView;
		});