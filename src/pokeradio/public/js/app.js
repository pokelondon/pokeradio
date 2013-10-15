define(['jquery',
		'backbone',
		'underscore',
		'views/spotify/search-view'
		],
		function($,Backbone,_,searchView){

			app ={
				init:function(){
					this.searchView = new searchView();
					console.log(this.searchView);
				}
			}
			return app;

		});