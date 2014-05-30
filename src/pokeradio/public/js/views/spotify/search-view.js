define(['jquery',
        'backbone',
        'underscore',
        'collections/spotify-tracks',
        'iobind',
        'utils',
        'views/spotify/track',
        'helpers/analytics'
        ],
        function($, Backbone,_ , spotifyTracks, ioBind, utils, TrackView, Analytics){
            var SearchView = Backbone.View.extend({
                el: $('#addTrackView'),
                searchKey: 191, // '/' search key
                enterToQueue: false,
                events:{
                    'submit #searchForm': 'search',
                    'click': 'closeView',
                    'click .Search-wrapper form, .Search-items': 'catchEvent',
                    'keyup #searchInput': 'arrowKeys'
                },

                initialize: function() {
                    _.bindAll(this, 'arrowKeys');
                    this.collection = spotifyTracks;
                    this.collection.on('results', this.render, this);

                    this.$container = this.$('.js-search-results-wrapper');
                    this.$list = this.$('.js-search-items');
                    this.$input = this.$('#searchInput');

                    // Click event for open button,
                    // not a child of this.$el so dont delegate events
                    $('.add-track').on('click', _(this.openView).bind(this));

                    this.on('open', this.focusInput, this);
                    // Non [backbone] delegated event bind for opening and closing the search view
                    this.bindKeys();
                    $('html').on('drag dragenter dragover dragleave drop', 'body', this.ignoreEvent);

                    $('html').on('drop', 'body', _(this.drop).bind(this));

                    //Validate spotify uris
                    this.spotify_validate = new RegExp('^spotify:track:([a-zA-Z0-9]{22})$', 'i');
                },

                /**
                 * While the text input is in focus, listen to keyup events
                 * If they are arrows, toggle the selected item in the collection
                 */
                arrowKeys: function(evt) {
                    var self = this;
                    var UP = 38;
                    var DOWN = 40;
                    var ENTER = 13;

                    if([UP, DOWN, ENTER].indexOf(evt.keyCode) < 0) {
                        return;
                    }
                    return {
                        38: function(evt) {
                            evt.preventDefault();
                            self.collection.selectPrev();
                            self.enterToQueue = true;
                        },
                        40: function(evt) {
                            evt.preventDefault();
                            self.collection.selectNext();
                            self.enterToQueue = true;
                        },
                        13: function(evt) {
                            // Check the flag, only attempt to queue if its not already been done
                            // Or it might be an enter press for closing an alert (that would cause more to show)
                            if(!self.enterToQueue) {
                                return;
                            }
                            evt.preventDefault();
                            evt.stopPropagation();
                            var model = self.collection.findWhere({'is-focused': true});
                            if(model) {
                                Analytics.trackEvent('track', 'queue', 'source: search');
                                model.queue();
                                self.enterToQueue = false;
                            }
                        }
                    }[evt.keyCode](evt);
                },

                /**
                 * Repopulate listign with new track view instances when the
                 * collection changes
                 */
                render: function(opts) {
                    if (typeof opts === undefined) opts = {};
                    opts = $.extend({}, { queue: false }, opts);

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

                        // trigger queueTrack on this track if it was dropped in
                        // (it'll be the only track in the result set)
                        if (opts.queue) {
                            Analytics.trackEvent('track', 'queue', 'source: drag');
                            view.queueTrack();
                            self.closeView();
                        }
                    });
                    if(this.collection.endpoint == 'lookup') {
                        $('#searchInput').val(this.collection.at(0).attributes.name);
                    }
                    return this;
                },

                /**
                 * DO search query
                 */
                search: function(evt){
                    Analytics.trackEvent('track', 'search');
                    this.collection.search($('#searchInput').val());
                    evt.preventDefault();
                },

                closeView: function(){
                    this.$el.fadeOut();
                    this.trigger('close');
                },

                openView: function(){
                    Analytics.trackPageview('/search/');
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
                },
                /**
                 * Drop
                 */
                drop: function(evt) {
                    if($(evt.target).parents('.js-dropzone').length) {
                        evt.stopPropagation();
                        evt.preventDefault();
                        uri = this.parseSpotifyUri(evt);
                        if(uri) {
                            this.collection.lookup(uri);
                            this.openView();
                        }else {
                            alert('Only single tracks from Spotify\xAE are allowed');
                        }
                    }
                    $('.js-Search-dragDrop').fadeOut(300, function(){
                        $('body').removeClass('on-drag');
                    });
                },
                ignoreEvent: function(evt) {
                    switch (evt.type) {
                        case 'dragenter':
                            lastenter = evt.target;
                            $('.js-Search-dragDrop').fadeIn();
                             $('body').addClass('on-drag');
                            break;
                        case 'dragleave':
                            if (lastenter === evt.target) {
                                $('.js-Search-dragDrop').fadeOut(300, function(){
                                    $('body').removeClass('on-drag');
                                });
                            }
                            break;
                    }
                    evt.stopPropagation();
                    evt.preventDefault();
                },
                parseSpotifyUri: function(evt){
                    var uri = evt.originalEvent.dataTransfer.getData('text/uri-list');
                    if(this.spotify_validate.test(uri)) {
                        return uri;
                    } else {
                        var dndData = evt.originalEvent.dataTransfer.getData('Text');
                        dndData_uri = (dndData.split('/'));
                        // removing "http://open.spotify.com/"
                        dndData_uri.splice(0,3);
                        dndData_uri.splice(0,0,'spotify');
                        uri = dndData_uri.join(':');

                        if (this.spotify_validate.test(uri)) {
                         return uri;
                        }
                    }
                    return false;
                }
            });
            return SearchView;
        });
