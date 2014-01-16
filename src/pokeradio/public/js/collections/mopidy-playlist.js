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
                _.bindAll(this, 'playlistFetch', 'playlistUpdate', 'itemDeleted');
                // Socket Events
                this.ioBind('load', this.playlistFetch, this);
                this.ioBind('update', this.playlistUpdate, this);
                this.ioBind('message', this.displayMessage, this);
                this.ioBind('deleted', this.itemDeleted, this);

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
                var data = $.parseJSON(data);
                if(data.played){
                    var item = this.findWhere({id: parseInt(data.id)});
                    item.set('played', true);
                }else {
                    this.add(data);
                }
            },

            /**
             * Item has been removed from the remote playlist.
             * Delete it from the collection here
             */
            itemDeleted: function(id) {
                var item = this.findWhere({id: parseInt(id)});
                this.remove(item);
            }

        });
        return new Collection();

});
