define(['jquery',
        'backbone',
        'underscore',
        'collections/spotify-tracks',
        'iobind',
        'utils',
        'views/spotify/track'
        ],
        function($, Backbone,_ , spotifyTracks, ioBind, utils, TrackView){
            var SearchView = Backbone.View.extend({
                el: $('#addTrackView'),
                events:{
                    'submit #searchForm': 'search',
                    'click .exit-icon': 'closeView'
                },

                initialize: function(){
                    this.collection = spotifyTracks;
                    this.collection.on('results', this.render, this);
                    this.$container = this.$('.track-listing-container');
                    this.$list = this.$('.track-listing-container .items');
                },

                /**
                 * Repopulate listign with new track view instances when the
                 * collection changes
                 */
                render: function() {
                    var self = this;
                    this.$list.html('');
                    if(this.collection.length) {
                        this.$container.addClass('has-results');
                    } else {
                        this.$container.removeClass('has-results');
                    }
                    // Populate items
                    _(this.collection.models).each(function(model) {
                        var view = new TrackView(model);
                        self.$list.append(view.render().el);
                    });
                    return this;
                },

                /**
                 * DO search query
                 */
                search: function(evt){
                    this.collection.search($('#searchInput').val());
                    evt.preventDefault();
                },

                closeView: function(){
                    utils.toggleFade(this.$el);
                }
            });
            return SearchView;
        });
