define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'views/progress-bar'
    ],
    function($, Backbone, _, SearchView, PlaylistView, ProgressBar){
        window.PRAD = window.PRAD || {};
        window.PRAD.is_fox = (navigator.appVersion.indexOf("Win")!=-1);
        var app = {
            init: function(){
                this.searchview = new SearchView();
                this.playlistview = new PlaylistView();
                this.progressbar = new ProgressBar();
            }
        };
        return app;
    }
);
