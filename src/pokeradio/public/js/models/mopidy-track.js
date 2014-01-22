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
                    isMine: false,
                    liked: false,
                    disliked: false
                },

                initialize: function() {
                    this.collection.on('change:played', this.checkIsPlaying, this);
                    if(this.get('user')['id'] === PRAD.user_id) {
                        this.set('isMine', true);
                    }
                    if(_(this.get('liked_ids')).indexOf(PRAD.user_id) >= 0) {
                        this.set('liked', true);
                    }
                    if(_(this.get('disliked_ids')).indexOf(PRAD.user_id) >= 0) {
                        this.set('disliked', true);
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
                },

                likeTrack: function() {
                    if(this.canLike()) {
                        socket.emit('like_track', this.get('id'));
                        this.set('liked', true);
                    }
                },

                dislikeTrack: function() {
                    if(this.canLike()) {
                        socket.emit('dislike_track', this.get('id'));
                        this.set('disliked', true);
                    }
                },

                canLike: function() {
                    if(PRAD.user_id == this.get('user')['id']) {
                        alert('You cant like your own track');
                        return false;
                    }
                    return true;
                },

                /**
                 * Find the total time in minutes of tracks preceeding this one in the playlist
                 */
                timeTillPlay: function(mins) {
                    var index = this.collection.indexOf(this);
                    var _preceeding_tracks = this.collection.chain().slice(0, index);
                    var _unplayed = _preceeding_tracks.filter(function(i) { return !i.get('played'); });
                    var t = _unplayed.reduce(function(memo, i) { return memo + i.get('length'); }, 0);
                    return (!!mins) ? t.convertToMinutes().value() : t.value();
                }

            });
            return MopidyTrack;
        });
