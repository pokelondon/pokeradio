define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'views/progress-bar',
    'helpers/analytics'
    ],
    function($, Backbone, _, SearchView, PlaylistView, ProgressBar, Analytics){
        window.PRAD = window.PRAD || {};
        window.PRAD.is_fox = (navigator.appVersion.indexOf("Win")!=-1);
        window.PRAD.app = {
            init: function(){
                this.searchview = new SearchView();
                this.playlistview = new PlaylistView();
                this.progressbar = new ProgressBar();
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
