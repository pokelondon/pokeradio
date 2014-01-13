define(['jquery',
        'backbone',
        'underscore',
        'collections/mopidy-playlist'
        ],
        function($, Backbone, _, mopidyPlaylist){
            var Track = Backbone.Model.extend({
                idAttribute: "href",
                defaults: {
                    selected: false,
                    inQueue: false
                },

                initialize: function() {
                    // Initial value for inqueue to dim out stuff when
                    // a new search is made
                    this.set('inQueue', this.checkInPlaylist());
                },

                /**
                 * Send a socket message to the server to get
                 * this track queued
                 */
                queue: function() {
                    if(this.checkInPlaylist()) {
                        alert(this.get('name') + ' is already queued');
                        return;
                    }
                    var track_payload = {
                        'name': this.attributes.name,
                        'href': this.get('href'),
                        'artist': this.get('artists')[0].name,
                        'length': this.get('length'),
                        'album': {
                            'href': this.get('album').href,
                        }
                    };
                    socket.emit('add_track', JSON.stringify(track_payload));
                    this.set('selected', !this.get('selected'));
                    // TODO Send socket message to remove from queue if re-clicked
                },

                /**
                 * Using the required singleton instance of the mopidy playlist collection
                 * check whether a track with this spotify URI is already queued.
                 */
                checkInPlaylist: function() {
                    var res = mopidyPlaylist.findWhere({href: this.get('href')});
                    return !!res;
                }
        });
        return Track;
    });
