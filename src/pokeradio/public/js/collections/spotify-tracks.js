define([
    'jquery',
    'backbone',
    'urls',
    'models/spotify-track'],
    function($, Backbone, urls, Track){
        var Collection = Backbone.Collection.extend({
            url: urls.track,
            model: Track,
            teritory: 'GB',

            /**
             * Filter out results which are not locally available
             */
            parse: function(response){
                var self = this;
                var filtered = _(response.tracks).filter(function(track) {
                    var territories = track.album.availability.territories.split(' ');
                    return territories.indexOf(self.teritory) > 0;
                });
                return filtered;
            },

            getAlbumArt: function(models, resp){

            },

            /**
             * Perform search query on spotify API
             */
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
        return new Collection();
});
