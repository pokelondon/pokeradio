define(['jquery',
		'backbone',
		'underscore',
		'collections/mopidy-playlist',
		'utils',
        'views/playlist/track'
		],
		function($, Backbone, _, MopidyPlaylist, utils, TrackView){
			var playlistView = Backbone.View.extend({
				el: $('.container'),

				initialize: function(){
					_.bindAll(this, 'render', 'isPlaying');
					this.collection = new MopidyPlaylist();

                    // Collection events
					this.collection.on('reset', this.render, this);
					this.collection.on('add', this.append, this);
					this.collection.on('change', this.change, this);
					//this.collection.on('progressUpdate', this.progress, this);

                    this.$list = this.$('#playlist');

					_.mixin({
						convertToMinutes: utils.convertToMinutes,
						isPlaying: this.isPlaying,
					});
				},
				events: {
					'click .add-track': 'openSearch',
				},

                /**
                 * Render initial track list
                 */
				render: function(collection){
                    var self = this;
                    this.$list.html('');
                    _(this.collection.models).each(function(model) {
                        var view = new TrackView(model);
                        self.$list.append(view.render().el);
                    });
                    return this;
				},

                /**
                 * A new track has been added,
                 * Make a view for it and append it to the list
                 */
				append: function(model){
                    var view = new TrackView(model);
                    this.$list.append(view.render().el);
				},

				change: function(model){
					$( "li[data-playlist-id='"+model.id+"']" ).attr('class', 'media played');
					$( "li[data-playlist-id='"+model.id+"'] .progress" ).remove();
					next_track = this.collection.findWhere({played: false });
					/*Possible to place in a subview??*/
					pt = _.template($('#progress-template').html());
					$( "li[data-playlist-id='"+next_track.id+"']" ).append(pt);
					/* Call the progress function manually because we don't timing of the render bar*/
					data = {time_position: 0, length: next_track.attributes.length * 1000};
					this.progress(data);
				},

                /**
                 * Update progress.
                 * TODO move this to its own view
                 */
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

                /**
                 * Find out if the passed model is playing
                 * TODO make it a model method
                 */
				isPlaying: function(model){
					var current_track = this.collection.findWhere({played: false });
					return model == current_track;
				},

				openSearch: function(){
					utils.toggleFade($('#AddTrackView'));
				}

			});
			return playlistView;
		});
