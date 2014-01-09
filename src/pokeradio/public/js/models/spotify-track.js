define(['jquery',
        'backbone',
        'underscore',
        ],
        function($,Backbone,_){
            var Track = Backbone.Model.extend({
                idAttribute: "href",
                defaults: {
                    selected: false
                },
                queue: function() {
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
                }
        });
        return Track;
    });
