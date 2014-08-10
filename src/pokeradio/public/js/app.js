define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'helpers/analytics',
    'views/messaging/controller',
    ],
    function($, Backbone, _, SearchView, PlaylistView, Analytics, MessagingController){

        /**
        * Sniff for a suitably named transition end event
        */
        function whichTransitionEvent() {
            var t;
            var el = document.createElement('fakeelement');
            var transitions = {
                'transition': 'transitionend',
                'MSTransition': 'msTransitionEnd',
                'MozTransition': 'transitionend',
                'WebkitTransition': 'webkitTransitionEnd'
            };
            for(t in transitions){
                if( el.style[t] !== undefined ){
                    return transitions[t];
                }
            }
        }

        function whichAnimationEvent() {
            var t;
            var el = document.createElement('fakeelement');
            var animations = {
                'animation': 'animationend',
                'MSAnimation': 'msanimationEnd',
                'MozAnimation': 'animationend',
                'WebkitAnimation': 'webkitAnimationEnd'
            };
            for(t in animations){
                if( el.style[t] !== undefined ){
                    return animations[t];
                }
            }
        }

        PRAD.transitionEndEvent = PRAD.transitionEndEvent || whichTransitionEvent();
        PRAD.animationEndEvent = PRAD.animationEndEvent || whichAnimationEvent();

        window.PRAD = window.PRAD || {};
        window.PRAD.is_fox = (navigator.appVersion.indexOf("Win")!=-1);
        window.PRAD.app = {
            init: function(){
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
