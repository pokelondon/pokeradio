define([
    'jquery',
    'backbone',
    'urls',
    'models/spotify-track'],
    function($, Backbone, urls, Track){
        var spotifyResults = Backbone.Collection.extend({
            url: urls.track,
            model: Track,
            parse: function(response){
                return response.tracks;
            },
            getAlbumArt: function(models, resp){

            },
            search: function(query) {
                var self = this;
                this.fetch({
                    data: $.param({q: query}),
                    success: function(data) {
                        self.trigger('results');
                    }
                });
            }
        });
        return spotifyResults;
});
