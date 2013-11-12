define(['jquery',
		'backbone',
		'underscore',
		'collections/mopidy-playlist',
		'text!template/playlist.html',
		'utils',
		],
		function($,
				Backbone,
				_,
				MopidyPlaylist,
				pl_template,
				utils) {
	var playlistView = Backbone.View.extend({
		el: $('.container'),
		initialize: function(){
			_.bindAll(this, 'render','isPlaying');
			this.MopidyPlaylistCollection = new MopidyPlaylist();
			this.MopidyPlaylistCollection.on('reset', this.render, this);
			this.MopidyPlaylistCollection.on('add', this.append, this);
			this.MopidyPlaylistCollection.on('change', this.change, this);
			this.MopidyPlaylistCollection.on('progressUpdate', this.progress, this);
			_.mixin({
				convertToMinutes: utils.convertToMinutes,
				isPlaying: this.isPlaying,
			});
		},
		events: {
			'click .add-track': 'openSearch',

		},
		render: function(collection){
			var template = _.template(pl_template, {metadata:collection.models});
			$('#playlist').html(template);
		},
		append: function(model){
			var template = _.template(pl_template, {metadata:[model]});
			$('#playlist').append(template);
		},
		change: function(model){
			$( "li[data-playlist-id='"+model.id+"']" ).attr('class', 'media played');
			$( "li[data-playlist-id='"+model.id+"'] .progress" ).remove();
			next_track = this.MopidyPlaylistCollection.findWhere({played: false });
			/*Possible to place in a subview??*/
			pt = _.template($('#progress-template').html());
			$( "li[data-playlist-id='"+next_track.id+"']" ).append(pt);
			/* Call the progress function manually because we don't timing of the render bar*/
			data = {time_position: 0, length: next_track.attributes.length * 1000};
			this.progress(data);

		},
		progress: function(data){
			if(_.isNumber(this.interval)){
				clearInterval(this.interval);
			}
			this.interval = setInterval(function(){
				per =   data.time_position / data.length * 100;
				$('.progress-bar').css('transition-duration', '1000ms');
				$('.progress-bar').css('width', per+'%');
				data.time_position = data.time_position + 1000;
			},1000);
		},
		isPlaying: function(model){
			c_model = this.MopidyPlaylistCollection.findWhere({played: false });
			return model == c_model;
		},
		openSearch: function(){
			$('body').addClass('modal-open');
			utils.toggleFade($('#addTrackView'));
			$('#addTrackView').bind('scroll',utils.onPageBottom);

		}
	
	});
	return playlistView;
});