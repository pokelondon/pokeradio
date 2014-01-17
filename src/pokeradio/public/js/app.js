define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'views/progress-bar'
    ],
    function($, Backbone, _, SearchView, PlaylistView, ProgressBar){
        app = {
            init: function(){
                this.searchview = new SearchView();
                this.playlistview = new PlaylistView();
                this.progressbar = new ProgressBar();
            }
        };
        return app;
    }
);
