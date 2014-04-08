define([
    'jquery',
    'backbone',
    'urls',
    'models/spotify-track'],
    function($, Backbone, urls, Track){
        var Collection = Backbone.Collection.extend({

            model: Track,
            teritory: 'GB',
            arrowIndex: -1,

            url: function() {
                switch(this.endpoint)
                {
                    case 'search':
                        return urls.track;
                    case 'lookup':
                        return urls.lookup;
                    default:
                        return urls.track;
                }

            },
            initialize: function() {
                // Reset keyboard select index when new results are fetched
                this.on('results', function() { this.arrowIndex = -1; }, this);
                this.on('queued', this.defocus, this);

            },

            comparator: function(i) {
                var index = parseFloat(i.get('popularity'));
                return 1 - index;
            },

            /**
             * Filter out results which are not locally available
             */
            parse: function(response){
                var self = this;
                if (this.endpoint == 'lookup') {
                    return response.track;
                }

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
                this.endpoint = 'search';
                var self = this;
                this.fetch({
                    data: $.param({q: query}),
                    success: function(data) {
                        self.trigger('results');
                    }
                });
            },

            lookup: function(query) {
                this.endpoint = 'lookup';
                var self = this;
                this.fetch({
                    data: $.param({uri: query}),
                    success: function(data) {
                        self.trigger('results', { queue: true });
                    }
                });
            },
            selectNext: function() {
                if(this.arrowIndex <= this.length) {
                    this.arrowIndex ++;
                }
                this.focus(this.arrowIndex);
            },

            selectPrev: function() {
                if(this.arrowIndex > 0) {
                    this.arrowIndex --;
                }
                this.focus(this.arrowIndex);
            },

            focus: function(index) {
                var model = this.at(index);
                if(!model) { return false; }
                this.defocus();
                model.set('is-focused', true);
                return true;
            },

            /**
             * Remove keyboard selection 'focus' from all models
             */
            defocus: function() {
                this.invoke('set', 'is-focused', false);
            }
        });
        return new Collection();
});
