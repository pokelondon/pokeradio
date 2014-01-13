define([
    'jquery',
    'backbone',
    'urls',
    'underscore',
    'iobind',
    'models/mopidy-track'
    ],
    function($, Backbone, urls, _, ioBind, MopidyTrack){
        var Collection = Backbone.Collection.extend({
            url: 'playlist',
            socket: window.socket,
            model: MopidyTrack,

            initialize: function(){
                _.bindAll(this, 'playlistFetch', 'playlistUpdate');
                // Socket Events
                this.ioBind('load', this.playlistFetch, this);
                this.ioBind('update', this.playlistUpdate, this);
                this.ioBind('message', this.displayMessage, this);

                // Request initial playlist data
                socket.emit('fetch_playlist');
                this.comparator = 'id';
            },

            displayMessage: function(message) {
                alert(message);
            },

            /**
             * Gets all items in the playlist
             * for use on init
             */
            playlistFetch: function(data){
                this.reset($.parseJSON(data));
                //console.table(_(this.models).pluck('attributes'));
            },

            /**
             * Remote playlist has been updated. Add new item
             */
            playlistUpdate: function(data){
                // Single track is passed so we check if its a new track or played track.
                data = $.parseJSON(data);
                if(data.played){
                    this.set(data);
                }else {
                    this.add(data);
                }
            }

        });
        return new Collection();

});
