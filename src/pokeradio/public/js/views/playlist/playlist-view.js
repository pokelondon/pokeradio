define(['jquery',
		'backbone',
		'underscore',
		'collections/mopidy-playlist',
		'text!template/playlist.html',
		],
		function($, Backbone, _, MopidyPlaylist, pl_template){
			var playlistView = Backbone.View.extend({
				el: $('.container'),

				initialize: function(){
					_.bindAll(this, "render");
					this.MopidyPlaylist = new MopidyPlaylist();
					this.MopidyPlaylist.on('reset', this.render, this);
					this.MopidyPlaylist.on('add', this.append, this);
					this.MopidyPlaylist.on('remove', this.remove, this);
					this.MopidyPlaylist.on('progressUpdate', this.progress, this);
				},
				render: function(collection){
					console.log(collection);
					var template = _.template(pl_template, {metadata:collection.models, collection: this.MopidyPlaylist});
					$('#playlist').html(template);
				},
				append: function(model){
					var template = _.template(pl_template, {metadata:[model], collection: this.MopidyPlaylist});
					$('#playlist').append(template);
				},
				remove: function(model){
					$( "li[data-playlist-id='"+model.id+"']" ).remove();
					next_track = this.MopidyPlaylist.at(0);
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
				}
			
			});
			return playlistView;
		});