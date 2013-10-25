define(['jquery',
		'backbone',
		'underscore',
		],
		function($,Backbone,_){
			Track = Backbone.Model.extend({
				idAttribute: "href"
			});
			return Track;
			
		});