define([
    'jquery',
    'backbone',
    'urls',
    'underscore',
    'iobind',
    'models/mopidy-track'
    ],
    function($, Backbone, urls, _, ioBind, MopidyTrack){
        var playlistResults = Backbone.Collection.extend({
            url: 'playlist',
            socket: window.socket,
            model: MopidyTrack,

            initialize: function(){
                _.bindAll(this, 'playlistFetch', 'playlistUpdate', 'progress');
                // Socket Events
                this.ioBind('fetch', this.playlistFetch, this);
                this.ioBind('update', this.playlistUpdate, this);
                this.ioBind('progress', this.progress, this);
                //
                // Request initial playlist data
                socket.emit('playlist', 'fetch');
                this.comparator = 'id';
            },

            /**
             * Gets all items in the playlist
             * for use on init
             */
            playlistFetch: function(data){
                this.reset($.parseJSON(data));
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
            },

            /**
             * Progress update
             * TODO Move this and socket binding to the view
             */
            progress: function(data){
                this.trigger('progressUpdate', $.parseJSON(data));
            }

        });
        return playlistResults;

});
