define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'helpers/analytics',
    'views/messaging/controller',
    'events',
    'models/app_state'
    ],
    function($, Backbone, _, SearchView, PlaylistView, Analytics, MessagingController, _events, appState){

        Backbone.trigger('socket:connected');

        socket.on('disconnect', function(){
            console.log('disconnected');
            Backbone.trigger('socket:disconnected');
        });

        socket.on('play:progress', function(data) {
            data = JSON.parse(data);
            console.log(data);
            Backbone.trigger('play:progress', data);
        });

        socket.on('playlist:add', function(data) {
            data = JSON.parse(data);
            Backbone.trigger('playlist:add', data);
        });

        socket.on('playlist:played', function(data) {
            data = JSON.parse(data);
            Backbone.trigger('playlist:played', data);
        });

        socket.on('playlist:delete', function(data) {
            data = JSON.parse(data);
            Backbone.trigger('playlist:delete', data);
        });

        socket.on('error', function(data) {
            console.error(data);
        });

        socket.on('connect_error', function(data) {
            data = JSON.parse(data);
            console.error(data);
        });

        socket.on('reconnecting', function() {
            console.error('reconnection');
        });

        window.PRAD = window.PRAD || {};
        window.PRAD.is_fox = (navigator.appVersion.indexOf("Win")!=-1);
        window.PRAD.app = {
            init: function(){
                this.appState = appState;
                this.searchview = new SearchView();
                this.playlistview = new PlaylistView();
                this.messagingcontroller = MessagingController; // singleton
            }
        };

        // global handler for outbound spotify links
        $(document).on('click', 'a.js-spotify-link', function(e) {
            var $link = $(this),
                label;
            if ($link.hasClass('js-spotifyLink--track')) label = 'track';
            else if ($link.hasClass('js-spotifyLink--artist')) label = 'artist';
            Analytics.trackEvent('track', 'spotifyLinkClick', label);
        });

        // global handler for JS exceptions
        window.onerror = function(message, file, line) {
            Analytics.trackException(file + " (" + line + "): " + message);
        };

        return window.PRAD.app;
    }
);
