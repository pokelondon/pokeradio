define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'helpers/analytics',
    'views/messaging/controller',
    'views/badge/badges-list',
    'events',
    'models/app_state'
    ],
    function($, Backbone, _, SearchView, PlaylistView, Analytics, messagingController, badgesList, _events, appState){

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

            socket.on('badge:add', function(user_id) {
                Backbone.trigger('badge:add', user_id);
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
                this.messagingcontroller = messagingController; // singleton
                this.badgecontroller = badgesList; // singleton

                //(function() {
                    //var from = new Date('2015-04-01 00:00:00');
                    //var to = new Date('2015-04-01 12:00:00');
                    //var options = ['Scatman (ski-ba-bop-ba-dop-bop)    ... adiba diba dibadib   ',
                                //'Pokémon Theme   ',
                                //'Hakuna Matata   ',
                                //'Everything is AWESOME!!! #LOL #YOLO HAsHTaG #totes   '];
                    //var $input = $('#searchInput');
                    //var getWord = function getWord() {
                        //var key = _.random(0, options.length -1);
                        //return options[key].split("");
                    //};

                    //$(window).on('search:focus', function() {
                        //if(new Date() > to || new Date() < from) {
                            //return;
                        //}
                        //$input.val("");
                        //var word = getWord();
                        //$input.off('keydown').on('keydown', function(evt) {
                            //evt.preventDefault();
                            //var val = $input.val();
                            //var letter = word.shift();
                            //if (!letter) {
                                //return;
                            //}
                            //$input.val(val + letter);
                            //if(!word.length) {
                                //$input.off('keydown');
                            //}
                        //});
                    //});
                //}());
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
