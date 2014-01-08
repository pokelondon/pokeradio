define(['jquery',
        'backbone',
        'underscore',
        'collections/spotify-tracks',
        'iobind',
        'text!template/spotify/list.html',
        'utils',
        'views/spotify/track-view'
        ],
        function($, Backbone,_ , SpotifyTracks, ioBind, tl_template, utils, TrackView){
            var SearchView = Backbone.View.extend({
                el: $('#AddTrackView'),
                events:{
                    'submit #searchForm': 'search',
                    'click .exit-icon': 'closeView'
                },

                initialize: function(){
                    this.collection = new SpotifyTracks();
                    this.collection.on('results', this.render, this);
                    this.$list = this.$el.find('.track-listing-container');
                },

                /**
                 * Repopulate listign with new track view instances when the
                 * collection changes
                 */
                render: function() {
                    var self = this;
                    this.$list.html('');
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
