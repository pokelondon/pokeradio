require.config({
	paths:{
		jquery: '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min',
		backbone: 'lib/backbone/backbone.min',
		underscore: 'lib/underscore/underscore'
	},
	shim:{
		'backbone':{
			deps:['underscore','jquery'],
			exports: 'Backbone'
		},
		'underscore':{
			deps:['jquery'],
			exports:'_'
		}
	}
})

define(['app'],function(app){
	app.init();	
});