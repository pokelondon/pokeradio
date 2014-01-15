define(['jquery',
        'backbone',
        'underscore',
        'views/_base_track',
        'text!template/playlist/track.html',
        ],
        function($, Backbone, _, BaseTrackView, template){
            var TrackView = BaseTrackView.extend({
                tagName: 'li',
                template: template,
                className: 'Playlist-item media not-played',
                events:{
                    'click .btn-remove-track': 'removeTrack',
                },

                initialize: function(model) {
                    BaseTrackView.prototype.initialize.apply(this, arguments);

                    _.bindAll(this, 'removeTrack');
                    this.model.on('change:played', this.updatePlayedState, this);
                    this.model.on('remove', this.onTrackRemoved, this);

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

                onTrackRemoved: function() {
                    var self = this;
                    this.$el.slideUp(function() {
                        self.$el.remove();
                    });
                }
            });
            return TrackView;
        });

