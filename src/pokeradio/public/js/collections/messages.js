define(
    [   'jquery',
        'backbone',
        'underscore',
        'models/message'
    ],
    function($, Backbone, _, Message){
        var Collection = Backbone.Collection.extend({
            model: Message,
            initialize: function() {

                // Load in any static messages from the page request
                this.reset(JSON.parse(PRAD.messages));
                this.trigger('reset');
            }
        });
        return new Collection();
    }
);
