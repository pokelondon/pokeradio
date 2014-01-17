/**
 * Colleciton to proxy progress events to the view
 * Used with ioBind to recieve websocket events
 * */
define([
    'jquery',
    'backbone',
    'urls',
    'underscore',
    'iobind'
    ],
    function($, Backbone, urls, _, ioBind){
        var Collection = Backbone.Collection.extend({
            url: 'playlist',
            socket: window.socket,

            initialize: function(){
                var self = this;
                // Socket Events
                this.ioBind('progress', function(data) {
                    var data = JSON.parse(data);
                    self.trigger('play:progress', data);
                }, this);
            }
        });
        return Collection;
});

