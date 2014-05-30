define(['jquery',
        'backbone',
        'underscore',
        'helpers/analytics'
        ],
        function($, Backbone, _, Analytics){
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
                    // Suppress errors from any track that's just been shifted out (see trimPlayed in mopidy-playlist.js)
                    if (!this.collection) return false;

                    var current_track = this.collection.findWhere({played: false});
                    if(!current_track) {
                        return;
                    }
                    if(this.get('id') == current_track.get('id')) {
                        this.set('isPlaying', true);
                        return true;
                    }else{
                        this.set('isPlaying', false);
                        return false;
                    }
                },

                unQueue: function() {
                    Analytics.trackEvent('track', 'unqueue');
                    socket.emit('remove_track', this.get('id'));
                },

                likeTrack: function() {
                    if(this.canLike()) {
                        Analytics.trackEvent('track', 'vote', 'source: web', 1);
                        socket.emit('like_track', this.get('id'));
                        this.set('liked', true);
                    }
                },

                dislikeTrack: function() {
                    if(this.canLike()) {
                        Analytics.trackEvent('track', 'vote', 'source: web', 0);
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
                 * Find the index in the collection of this model
                 * Usefull for splitting off before and after a certain item
                 */
                getCollectionIndex: function() {

                    if (!this.collection) return false;

                    return this.collection.indexOf(this) || 0;
                },

                /**
                 * Find the total time in minutes of tracks preceeding this one in the playlist
                 */
                timeTillPlay: function(mins) {
                    var index = this.getCollectionIndex();
                    if (index === false) return false;
                    var _preceeding_tracks = this.collection.chain().slice(0, index);
                    var _unplayed = _preceeding_tracks.filter(function(i) { return !i.get('played'); });
                    var t = _unplayed.reduce(function(memo, i) { return memo + i.get('length'); }, 0);
                    return (!!mins) ? t.convertToMinutes().value() : t.value();
                }

            });
            return MopidyTrack;
        });
