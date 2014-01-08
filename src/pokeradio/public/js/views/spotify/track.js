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
                className: 'media',
                template: template,
                events:{
                    'click': 'queueTrack',
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

