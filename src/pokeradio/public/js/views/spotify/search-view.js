define(['jquery',
		'backbone',
		'underscore',
		'collections/spotify',
		'text!template/spotify/track-listing.html'
		],
		function($,Backbone,_,SpotifyCollection,tl_template){
			var searchView = Backbone.View.extend({
				el: $('.container'),
				
				initialize: function(){
					this.spotifyCollection = new SpotifyCollection;
				}, 
				events:{
					'submit #searchForm': 'search',
					'click .track-listing-container li': 'add_to_playlsit'
				},
				search: function(e){
					this.spotifyCollection.fetch({
						data : $.param(
							{q: $('#searchInput').val()}
						),
						success:function(data){
							
							template = _.template(tl_template, {metadata:data.models});
							$('.track-listing-container').html(template);
						}
					});
					return false;
				},
				add_to_playlsit:function(e){
					console.log(e);
					socket.emit('open_uri',$(e.currentTarget).data('uri'));
				}	
			});
			return searchView;
		});