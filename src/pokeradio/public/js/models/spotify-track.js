define(['jquery',
        'backbone',
        'underscore',
        ],
        function($,Backbone,_){
            var Track = Backbone.Model.extend({
                idAttribute: "href",
                queue: function() {
                    console.log('Queuing track');
                    console.table(this.attributes);

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
                }
        });
        return Track;
    });
