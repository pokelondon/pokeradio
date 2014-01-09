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
                    'click .minus-icon': 'queueTrack',
                    'click .btn-preview': 'preview'
                },

                initialize: function() {
                    BaseTrackView.prototype.initialize.apply(this, arguments);
                    this.model.on('change:selected', this.onSelect, this);
                },

                /**
                 * When rendering, add a class if the song is aready queued.
                 */
                render: function() {
                    if(this.model.get('inQueue')) {
                        this.$el.addClass('disabled');
                    }
                    return BaseTrackView.prototype.render.call(this);
                },

                /**
                 * When clicked, queue the track via socket message.
                 */
                queueTrack: function(evt) {
                    evt.preventDefault();
                    this.model.queue();
                },

                preview: function(evt) {
                    evt.preventDefault();
                    evt.stopPropagation();
                    var $iframe = $('<iframe width="80" height="80" frameborder="0" allowtransparency="true"></iframe>');
                    $iframe.attr('src', 'https://embed.spotify.com/?uri=' + this.model.get('href'));
                    this.$('.preview').html($iframe);
                },

                onSelect: function() {
                    if(this.model.get('selected')) {
                        this.$el.addClass('selected');
                    } else {
                        this.$el.removeClass('selected');
                    }
                }
            });
            return TrackView;
        });
