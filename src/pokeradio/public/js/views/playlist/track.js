define(['jquery',
        'backbone',
        'underscore',
        'views/_base_track',
        'text!template/playlist/track.html',
        'views/progress-bar',
        'models/app_state'
        ],
        function($, Backbone, _, BaseTrackView, template, ProgressBar, appState){
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
                    'mouseenter .media-wrapper': 'start_ttp_countdown',
                },

                initialize: function(model) {
                    BaseTrackView.prototype.initialize.apply(this, arguments);

                    _.bindAll(this, 'removeTrack', 'likeTrack', 'dislikeTrack', 'onVote', 'setVotedClasses', 'start_ttp_countdown', 'attachProgressBar');
                    this.model.on('change:played change:isPlaying', this.updatePlayedState, this);
                    this.model.on('remove', this.onTrackRemoved, this);
                    this.model.on('change:liked', this.onVote, this);
                    this.model.on('change:disliked', this.onVote, this);
                    this.on('render', this.setVotedClasses, this);
                    this.on('render', this.attachProgressBar, this);

                    this.listenTo(Backbone, 'play:progress', this.updateProgress);

                    // Get inital State
                    this.updatePlayedState();

                    Backbone.on('stop_ttp_countdown', this.stop_ttp_countdown, this);
                },

                attachProgressBar: function() {
                    this.progressbar = new ProgressBar();
                    this.$el.append(this.progressbar.render().$el);
                },

                detachProgressBar: function() {
                    if(!this.progressbar) {
                        return;
                    }
                    console.log('detaching progress bar');
                    this.progressbar.$el.remove();
                    this.progressbar = null;
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

                    if(this.model.checkIsPlaying()) {
                        this.$el.addClass('is-playing');
                        this.attachProgressBar();
                    } else {
                        this.$el.removeClass('is-playing');
                        this.detachProgressBar();
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
                    this.$el.addClass('is-removed');
                    this.$el.on(PRAD.transitionEndEvent, function() {
                        self.$el.remove();
                    });
                },


                /**
                 * Mouse goes over this element, so start the countodowner
                 */
                start_ttp_countdown: function(evt) {
                    var self = this;

                    var update = function(seconds) {
                        seconds = seconds | appState.get('time');
                        var ttp = self.model.timeTillPlay();
                        // Check track isnt already played or playing
                        if (ttp === false ) return false;

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
                    // Event from the progressbar interpolator
                    this.listenTo(appState, 'change:progress', function() {
                        update();
                    }, this);

                    // Update if the playlist changes (delete or played)
                    this.model.collection.on('change', function() {
                        update();
                    }, this);

                    // Trigger 'in' event to close other counters
                    Backbone.trigger('stop_ttp_countdown', this.model.get('id'));
                },

                /**
                 * Triggered on the mouse enter event of all tracks
                 * Only use this to do the hide sequence if its not this
                 * one being mouseovered.
                 */
                stop_ttp_countdown: function(id) {
                    if(this.model.get('id') === id) {
                        return;
                    }
                    this.$playingin.fadeOut();
                }
            });
            return TrackView;
        });
