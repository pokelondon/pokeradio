define(
    [   'jquery',
        'backbone',
        'underscore',
        'models/message'
    ],
    function($, Backbone, _, Message){
        var Collection = Backbone.Collection.extend({
            model: Message
        });
        return new Collection();
    }
);
