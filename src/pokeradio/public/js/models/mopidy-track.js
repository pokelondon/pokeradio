define(['jquery',
        'backbone',
        'underscore',
        ],
        function($,Backbone,_){
            MopidyTrack = Backbone.Model.extend({
                idAttribute: "id",
                wasPlaying: false,
                defaults: {
                    isPlaying: false,
                    isMine: false
                },

                initialize: function() {
                    this.collection.on('change:played', this.checkIsPlaying, this);
                    if(this.get('user')['id'] === PRAD.user_id) {
                        this.set('isMine', true);
                    }
                },

                checkIsPlaying: function() {
                    // Find next unplayed track
                    var current_track = this.collection.findWhere({played: false });
                    if(this.id == current_track.id) {
                        this.set('isPlaying', true);
                    }else{
                        this.set('isPlaying', false);
                    }
                },

                unQueue: function() {
                    socket.emit('remove_track', this.get('id'));
                }

            });
            return MopidyTrack;
        });
