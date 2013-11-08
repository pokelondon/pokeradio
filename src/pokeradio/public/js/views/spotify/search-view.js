define(['jquery',
		'backbone',
		'underscore',
		'collections/spotify-tracks',
		'iobind',
		'text!template/spotify/list.html',
		'utils'
		],
		function($, Backbone,_ , SpotifyTracks, ioBind, tl_template,utils){
			var searchView = Backbone.View.extend({
				el: $('#AddTrackView'),
				
				initialize: function(){
					this.spotifyTracks = new SpotifyTracks();
					
				},
				events:{
					'submit #searchForm': 'search',
					'click .track-listing-container li': 'addTrack',
					'click .exit-icon': 'closeView'
				},
				render: function(){

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
				addTrack:function(e){
					var track = this.spotifyTracks.get($(e.currentTarget).data('href'));
					console.log(track);
					var track_payload = {
						'name': track.attributes.name,
						'href': track.attributes.href,
						'artist': track.attributes.artists[0].name,
						'length': track.attributes.length,
						'album': {
							'href': track.attributes.album.href,

						}
					};
					socket.emit('add_track',JSON.stringify(track_payload));
				},
				closeView: function(){
					utils.toggleFade($('#AddTrackView'));
				},
			});
			return searchView;
		});