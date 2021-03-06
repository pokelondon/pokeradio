/**
 * Search result item view
 * Based on _base_track.js
 */
define(['jquery',
        'backbone',
        'underscore',
        'views/_base_track',
        'views/messaging/controller',
        'text!template/spotify/track.html',
        'helpers/analytics'
        ],
        function($, Backbone, _, BaseTrackView, MessagingController, template, Analytics){
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
                    if (this.model.checkInBlacklist()) {
                        MessagingController.createMessage({
                            text: "Think about what you're doing here, " + window.PRAD.first_name
                        });
                    }
                    Analytics.trackEvent('track', 'queue', 'source: search');
                    this.model.queue();
                },

                /**
                 * Embed the spotify iframe player for this track
                 */
                preview: function(evt) {
                    evt.preventDefault();
                    evt.stopPropagation();
                    Analytics.trackEvent('track', 'preview');
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
