define(['jquery',
		'backbone',
		'underscore',
		'views/spotify/search-view',
		'views/playlist/playlist-view'
		],
		function($,Backbone,_,SearchView, PlaylistView){

			app ={
				init:function(){
					this.searchview = new SearchView();
					this.playlistview = new PlaylistView();
				}
			};
			return app;

		});