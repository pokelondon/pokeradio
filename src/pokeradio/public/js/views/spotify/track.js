/**
 * Search result item view
 * Based on _base_track.js
 */
define(['jquery',
        'backbone',
        'underscore',
        'views/_base_track',
        'text!template/spotify/track.html',
        ],
        function($, Backbone, _, BaseTrackView, template){
            var TrackView = BaseTrackView.extend({
                className: 'media Search-item',
                template: template,
                events:{
                    'click .js-queue-track': 'queueTrack',
                    'click .btn-preview': 'preview'
                },

                initialize: function() {
                    BaseTrackView.prototype.initialize.apply(this, arguments);
                    this.model.on('change:is-selected', this.onSelectChange, this);
                    this.model.on('change:is-focused', this.onFocusChange, this);
                    // Initial state for tracks that are already in the playlist
                    // Checked against mopidy playlist on model init
                    this.onSelectChange();
                },

                /**
                 * When clicked, queue the track via socket message.
                 */
                queueTrack: function(evt) {
                    evt && evt.preventDefault();
                    if(this.model.checkInBlacklist()) {
                        alert('Think about what you\'re doing here, ' + window.PRAD.first_name);
                    }
                    if (typeof ga !== 'undefined') {
                        ga('send', 'event', 'track', 'queue', 'source: search');
                    }
                    this.model.queue();
                },

                /**
                 * Embed the spotify iframe player for this track
                 */
                preview: function(evt) {
                    evt.preventDefault();
                    evt.stopPropagation();
                    if (typeof ga !== 'undefined') {
                        ga('send', 'event', 'track', 'preview');
                    }
                    var $iframe = $('<iframe width="80" height="80" frameborder="0" allowtransparency="true"></iframe>');
                    $iframe.attr('src', 'https://embed.spotify.com/?uri=' + this.model.get('href'));
                    this.$('.js-search-item-details-preview').html($iframe);
                },

                /**
                 * Add and remove class for selected state
                 * selected is when a track is in the playlist
                 */
                onSelectChange: function() {
                    if(this.model.get('is-selected')) {
                        this.$el.addClass('is-selected');
                    } else {
                        this.$el.removeClass('is-selected');
                    }
                },

                /**
                 * Add and remove class for focused state
                 * focused state is when a model is considered active
                 * by keyboarding up and down the search results
                 */
                onFocusChange: function() {
                    if(this.model.get('is-focused')) {
                        this.$el.addClass('is-focused');
                    } else {
                        this.$el.removeClass('is-focused');
                    }
                }
            });
            return TrackView;
        });
