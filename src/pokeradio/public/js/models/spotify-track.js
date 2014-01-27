define(['jquery',
        'backbone',
        'underscore',
        'collections/mopidy-playlist'
        ],
        function($, Backbone, _, mopidyPlaylist){
            var Track = Backbone.Model.extend({
                idAttribute: "href",
                defaults: {
                    'is-selected': false
                },

                initialize: function() {
                    this.setSelected();
                },

                setSelected: function() {
                    // Initial value for inqueue to dim out stuff when
                    // a new search is made
                    this.set('is-selected', this.checkInPlaylist());
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
                        'artist_href': this.get('artists')[0].href,
                        'length': this.get('length'),
                        'album': {
                            'href': this.get('album').href,
                        }
                    };
                    socket.emit('add_track', JSON.stringify(track_payload));
                    this.set('is-selected', true);
                    this.collection.trigger('queued');
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
