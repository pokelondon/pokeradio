define([
    'jquery',
    'backbone',
    'urls',
    'underscore',
    'models/mopidy-track',
    'views/messaging/controller',
    'events'
    ],
    function($, Backbone, urls, _, MopidyTrack, MessagingController, _events){
        var Collection = Backbone.Collection.extend({
            url: 'api/playlist/',
            model: MopidyTrack,
            SHOW_NUM_PLAYED: 1,

            initialize: function(){
                _.bindAll(this, 'itemAdded', 'itemDeleted', 'itemPlayed');

                // Socket events, via the mediator
                this.listenTo(Backbone, 'playlist:delete', this.itemDeleted, this);
                this.listenTo(Backbone, 'playlist:add', this.itemAdded, this);
                this.listenTo(Backbone, 'playlist:played', this.itemPlayed, this);

                this.listenTo(Backbone, 'playlist:skip', this.itemSkipped, this);
                this.listenTo(Backbone, 'playlist:scratch', this.itemScratched, this);

                this.on('change:played', this.trimPlayed, this)

                this.comparator = 'id';
            },

            parseInitialData: function() {
                //parse the initial data into the collection
                this.reset(window.PRAD.playlist);
                // this works too!
                //this.fetch();
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
                this.add(data);
            },

            /**
             * Item has been removed from the remote playlist.
             * Delete it from the collection here
             */
            itemDeleted: function(id) {
                var item = this.findWhere({id: parseInt(id)});
                this.remove(item);
            },

            itemPlayed: function(data) {
                var item = this.findWhere({id: parseInt(data['id'])});
                item.set('played', true);
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
            },

            itemScratched: function(item) {
                if(item.user.id === PRAD.user_id) {
                    MessagingController.createMessage({
                        title: 'Scratch',
                        text: 'Oh dear, ' + item.name + ' didn\'t go down too well :(',
                        type: 'bad'
                    });
                }
            },

            itemSkipped: function(item) {
                if(item.user.id === PRAD.user_id) {
                    MessagingController.createMessage({
                        title: 'Skipped',
                        text: item.name + ' never saw the light of day! Try harder :-p',
                        type: 'bad'
                    });
                }

            }

        });
        return new Collection();

});
