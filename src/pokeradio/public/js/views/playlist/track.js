define(['jquery',
        'backbone',
        'underscore',
        'views/_base_track',
        'text!template/playlist/track.html',
        'bootstrap'
        ],
        function($, Backbone, _, BaseTrackView, template){
            var TrackView = BaseTrackView.extend({
                tagName: 'li',
                template: template,
                secondOffset: 0,
                className: 'Playlist-item media not-played',
                events:{
                    'click .btn-remove-track': 'removeTrack',
                    'click .btn-like': 'likeTrack',
                    'click .btn-dislike': 'dislikeTrack',
                    'mouseover': 'timeTillPlay',
                    'mouseout': 'tooltipClose'
                },

                initialize: function(model) {
                    BaseTrackView.prototype.initialize.apply(this, arguments);

                    _.bindAll(this, 'removeTrack', 'likeTrack', 'dislikeTrack', 'onVote', 'setVotedClasses', 'timeTillPlay');
                    this.model.on('change:played', this.updatePlayedState, this);
                    this.model.on('remove', this.onTrackRemoved, this);
                    this.model.on('change:liked', this.onVote, this);
                    this.model.on('change:disliked', this.onVote, this);
                    this.on('render', this.setVotedClasses, this);

                    // Get inital State
                    this.updatePlayedState();
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
                    this.$playingin = this.$('.js-playing-in');
                },

                onTrackRemoved: function() {
                    var self = this;
                    this.$el.slideUp(function() {
                        self.$el.remove();
                    });
                },

                timeTillPlay: function() {
                    var self = this;
                    var ttp = this.model.timeTillPlay();
                    self.$playingin.fadeIn();
                    $(window).on('play:progress:interpolated:seconds', function(el, seconds) {
                        var text = '';
                        if(1 > ttp) {
                            text = 'Playing';
                        }else{
                            text = 'Playing in: ' + _(ttp - seconds).convertToMinutes();
                        }
                        self.$playingin.text(text);
                    });
                },

                tooltipClose: function() {
                    this.$playingin.fadeOut();
                    $(window).off('play:progress:interpolated:seconds');
                }
            });
            return TrackView;
        });

