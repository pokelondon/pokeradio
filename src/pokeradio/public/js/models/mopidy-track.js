define(['jquery',
		'backbone',
		'underscore',
		],
		function($,Backbone,_){
			MopidyTrack = Backbone.Model.extend({
				idAttribute: "id"
			});
			return MopidyTrack;
			
		});