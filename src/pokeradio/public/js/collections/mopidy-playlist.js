define([
    'jquery',
    'backbone',
    'urls',
    'underscore',
    'iobind',
    'models/mopidy-track',
    'views/messaging/controller',
    'events'
    ],
    function($, Backbone, urls, _, ioBind, MopidyTrack, MessagingController, _events){
        var Collection = Backbone.Collection.extend({
            url: 'playlist',
            socket: window.socket,
            model: MopidyTrack,
            SHOW_NUM_PLAYED: 1,

            initialize: function(){
                _.bindAll(this, 'playlistFetch', 'playlistUpdate', 'itemDeleted');
                // Socket Events
                this.ioBind('load', this.playlistFetch, this);
                this.ioBind('update', this.playlistUpdate, this);
                this.ioBind('change:played', this.trimPlayed, this);
                this.ioBind('message', this.displayMessage, this);
                this.ioBind('deleted', this.itemDeleted, this);
                this.ioBind('expired', this.sessionExpired, this);

                // Request initial playlist data
                socket.emit('fetch_playlist');
                this.comparator = 'id';
            },

            displayMessage: function(message) {
                // TODO: is this required, or ever used?
                MessagingController.createMessage({
                    text: message
                });
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
                    var item = this.findWhere({id: parseInt(data.id)});
                    item.set('played', true);
                }else {
                    this.add(data);
                }
            },

            /**
             * Trim the played items if necessary
             */
            trimPlayed: function() {
                var count = this.where({ played: true }).length;
                if (count > this.SHOW_NUM_PLAYED) {
                    // might be at risk of an event loop
                    this.shift();
                }
            },

            /**
             * Item has been removed from the remote playlist.
             * Delete it from the collection here
             */
            itemDeleted: function(id) {
                var item = this.findWhere({id: parseInt(id)});
                this.remove(item);
            },

            /**
             * This happens when the socket server realises the session's exipred
             */
            sessionExpired: function() {
                MessagingController.createMessage({
                    text: "Soz, session's expired",
                    modal: true
                });
                // Redirect to logout page just in case, so we don't start a loop
                window.location.href = '/logout/';
            }

        });
        return new Collection();

});
