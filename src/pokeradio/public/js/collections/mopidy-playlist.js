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
            url: 'api/playlist/',
            model: MopidyTrack,
            SHOW_NUM_PLAYED: 1,

            initialize: function(){
                _.bindAll(this, 'itemAdded', 'itemDeleted');

                // Socket Events
                //this.ioBind('playlist:add', this.playlistUpdate, this);
                //this.ioBind('playlist:played', this.playlistUpdate, this);
                //this.ioBind('change:played', this.trimPlayed, this);
                //this.ioBind('expired', this.sessionExpired, this);

                // Socket events, via the mediator
                this.listenTo(Backbone, 'playlist:delete', this.itemDeleted, this);
                this.listenTo(Backbone, 'playlist:add', this.itemAdded, this);

                this.on('change', function() {
                    console.log('playlist changed');
                });
                this.on('add', function() {
                    // Tracks not added to the UI yet, they should listen for the socket event playlist:add
                    console.log('playlist add');
                });

                this.comparator = 'id';
            },

            parseInitialData: function() {
                //parse the initial data into the collection
                this.reset(window.PRAD.playlist);
                // this works too!
                //this.fetch();
            },

            //displayMessage: function(message) {
                //// TODO: is this required, or ever used?
                //MessagingController.createMessage({
                    //text: message
                //});
            //},

            /**
             * Remote playlist has been updated. Add new item
             */
            playlistupdate: function(data){
                // single track is passed so we check if its a new track or played track.
                data = $.parsejson(data);
                if(data.played){
                    var item = this.findwhere({id: parseint(data.id)});
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

            itemAdded: function(data){
                // single track is passed so we check if its a new track or played track.
                data = $.parsejson(data);
                this.add(data);
            },

            /**
             * Item has been removed from the remote playlist.
             * Delete it from the collection here
             */
            itemDeleted: function(id) {
                console.log('item deleted');
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
