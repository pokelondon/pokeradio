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

        if(socket) {
            Backbone.trigger('socket:connected');

            socket.on('disconnect', function(){
                console.log('disconnected');
                $('.Header-logo').css('opacity', '0.3');
                Backbone.trigger('socket:disconnected');
            });

            socket.on('play:progress', function(data) {
                data = JSON.parse(data);
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

            socket.on('playlist:skip', function(data) {
                data = JSON.parse(data);
                Backbone.trigger('playlist:skip', data);
            });

            socket.on('playlist:scratch', function(data) {
                data = JSON.parse(data);
                Backbone.trigger('playlist:scratch', data);
            });

            socket.on('error', function(data) {
                console.error(data);
            });

            socket.on('connect_error', function(data) {
                console.error(data);
            });

            socket.on('reconnecting', function() {
                $('.Header-logo').css('opacity', '0.8');
            });

            socket.on('reconnect', function() {
                $('.Header-logo').css('opacity', '1');
            });

        } else {
            $('.Header-logo').css('opacity', '0.3');
            Backbone.trigger('socket:disconnected');
        }

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
