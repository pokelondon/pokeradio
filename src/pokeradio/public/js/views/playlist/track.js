define(['jquery',
        'backbone',
        'underscore',
        'views/_base_track',
        'text!template/playlist/track.html'
        ],
        function($, Backbone, _, BaseTrackView, template){
            var TrackView = BaseTrackView.extend({
                tagName: 'li',
                template: template,
                secondOffset: 0,
                countdownText: '',
                className: 'Playlist-item media not-played',
                events:{
                    'click .btn-remove-track': 'removeTrack',
                    'click .btn-like': 'likeTrack',
                    'click .btn-dislike': 'dislikeTrack',
                    'mouseenter .media-wrapper': 'ttpIn',
                },

                initialize: function(model) {
                    BaseTrackView.prototype.initialize.apply(this, arguments);

                    _.bindAll(this, 'removeTrack', 'likeTrack', 'dislikeTrack', 'onVote', 'setVotedClasses', 'ttpIn');
                    this.model.on('change:played', this.updatePlayedState, this);
                    this.model.on('remove', this.onTrackRemoved, this);
                    this.model.on('change:liked', this.onVote, this);
                    this.model.on('change:disliked', this.onVote, this);
                    this.on('render', this.setVotedClasses, this);

                    // Get inital State
                    this.updatePlayedState();
                    $(window).on('ttpIn', _.bind(this.ttpOut, this));
                    // Proxy event to each instance of this model so it can be unsubed
                    $(window).on('play:progress:interpolated:seconds', _.bind(function(evt, data) {
                        this.trigger('update:countdown', data);
                    }, this));
                },

                /**
                 * Reflect model's played state in UI
                 */
                updatePlayedState: function() {
                    var played = this.model.get('played');
                    if(played) {
                        this.$el.addClass('played').removeClass('not-played');
                    } else {
                        this.$el.addClass('not-played').removeClass('played');
                    }
                },

                /**
                 * Handle remove button event, tell the model to unqueue itself
                 */
                removeTrack: function(evt) {
                    evt.preventDefault();
                    this.model.unQueue();
                },

                /**
                 * Handle like button event
                 */
                likeTrack: function(evt) {
                    evt.preventDefault();
                    this.model.likeTrack();
                },

                /**
                 * Handle dislike button event
                 */
                dislikeTrack: function(evt) {
                    evt.preventDefault();
                    this.model.dislikeTrack();
                },

                /**
                 * Update buttons following a like or dislike event on the model
                 */
                onVote: function() {
                    this.$('.btn-dislike').addClass('disabled');
                    this.$('.btn-like').addClass('disabled');
                    this.setVotedClasses();
                },

                setVotedClasses: function() {
                    var self = this;
                    if(this.model.get('liked')) {
                        this.$('.btn-like').addClass('voted');
                    }
                    if(this.model.get('disliked')) {
                        this.$('.btn-dislike').addClass('voted');
                    }
                    this.$playingin = this.$('.js-playing-in').hide();
                },

                onTrackRemoved: function() {
                    var self = this;
                    this.$el.slideUp(function() {
                        self.$el.remove();
                    });
                },


                ttpIn: function(evt) {
                    var self = this;
                    var update = function(seconds) {
                        var ttp = self.model.timeTillPlay();
                        // Check track isnt already played or playing
                        if(1 > ttp) {
                            if(self.model.get('played')) {
                                self.countdownText = '';
                            } else {
                                self.countdownText = '▶';
                            }
                        }else{
                            self.countdownText = 'Playing in: ' + _(ttp - seconds).convertToMinutes();
                        }
                        self.$playingin.text(self.countdownText);
                    };
                    // Set initial text before a progress event happens
                    update(0);
                    // Display the counting text
                    this.$playingin.fadeIn();
                    // Proxied event from the progressbar interpolator
                    this.on('update:countdown', update, this);
                    // Update if the playlist changes (delete or played)
                    this.model.collection.on('change', update, this);
                    // Trigger 'in' event to close other counters
                    $(window).trigger('ttpIn', this.model.get('id'));
                },

                /**
                 * Triggered on the mouse enter event of all tracks
                 * Only use this to do the hide sequence if its not this
                 * one being mouseovered.
                 */
                ttpOut: function(evt, id) {
                    if(this.model.get('id') === id) {
                        return;
                    }
                    this.$playingin.fadeOut();
                    // Unsubscribe from ticking event
                    this.off('update:countdown');
                }
            });
            return TrackView;
        });

