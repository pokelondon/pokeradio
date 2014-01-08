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
					_.bindAll(this, 'render');
					this.collection = new MopidyPlaylist();

                    // Collection events
					this.collection.on('reset', this.render, this);
					this.collection.on('add', this.append, this);

                    this.$list = this.$('#playlist');

					_.mixin({
						convertToMinutes: utils.convertToMinutes
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

				openSearch: function(){
					utils.toggleFade($('#AddTrackView'));
				}

			});
			return playlistView;
		});
