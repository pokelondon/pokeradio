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
                searchKey: 191, // '/' search key
                events:{
                    'submit #searchForm': 'search',
                    'click .Search-wrapper': 'closeView',
                    'click .Search-wrapper form, .Search-items': 'catchEvent'
                },

                initialize: function(){
                    this.collection = spotifyTracks;
                    this.collection.on('results', this.render, this);

                    this.$container = this.$('.js-search-results-wrapper');
                    this.$list = this.$('.js-search-items');
                    this.$input = this.$('#searchInput');

                    // Click event for open button,
                    // not a child of this.$el so dont delegate events
                    $('.add-track').on('click', _(this.openView).bind(this));

                    this.on('open', this.focusInput, this);
                    this.bindKeys();
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
                    this.$el.fadeOut();
                    this.trigger('close');
                },

                openView: function(){
                    this.$el.fadeIn();
                    this.trigger('open');
                },

                /**
                 * When inner parts of the view are clicked,
                 * dont let the event get back to the container,
                 * which would close the view
                 */
                catchEvent: function(evt) {
                    evt.stopPropagation();
                },

                focusInput: function(evt) {
                    this.$input.focus();
                },

                /**
                 * Listen to window keyup events to open the view if
                 * the search key is pressed
                 */
                windowKeyup: function(evt) {
                    if(this.searchKey === evt.keyCode) {
                        this.openView();
                    }
                    if(27 === evt.keyCode) {
                        this.closeView();
                    }
                },

                /**
                 * Bind search key to open this view.
                 */
                bindKeys: function() {
                    $(window).on('keyup', _(this.windowKeyup).bind(this));
                }
            });
            return SearchView;
        });
