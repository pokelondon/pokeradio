define(['jquery',
        'backbone',
        'underscore',
        'collections/mopidy-playlist',
        'utils',
        'views/playlist/track'
        ],
        function($, Backbone, _, mopidyPlaylist, utils, TrackView){
            var playlistView = Backbone.View.extend({
                el: $('.container'),

                initialize: function(){
                    _.bindAll(this, 'render');
                    // Singleton instance provided by require
                    this.collection = mopidyPlaylist;

                    // Collection events
                    this.collection.on('reset', this.render, this);
                    this.collection.on('add', this.append, this);

                    this.$list = this.$('#playlist');

                    _.mixin({
                        convertToMinutes: utils.convertToMinutes
                    });
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
                }

            });
            return playlistView;
        });
