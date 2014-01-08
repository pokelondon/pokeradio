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
                className: 'media not-played',
                events:{
                    //'click': 'queueTrack',
                },

                initialize: function(model) {
                    this.model = model; // TODO super this
                    this.model.on('change:played', this.updatePlayedState, this);

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
                }
            });
            return TrackView;
        });

