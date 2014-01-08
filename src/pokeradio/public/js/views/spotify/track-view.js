define(['jquery',
        'backbone',
        'underscore',
        'models/spotify-track',
        'text!template/spotify/track.html',
        ],
        function($, Backbone, _ , Track, template){
            var TrackView = Backbone.View.extend({
                tagName: 'li',
                className: 'media',
                events:{
                    'click': 'queueTrack',
                },

                initialize: function(model){
                    this.model = model;
                },

                render: function() {
                    var text = _.template(template, this.model.toJSON());
                    this.$el.html(text);
                    return this;
                },

                /**
                 * When clicked, queue the track via socket message.
                 */
                queueTrack: function(evt) {
                    evt.preventDefault();
                    this.model.queue();
                }
            });
            return TrackView;
        });

