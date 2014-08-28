define(
    [   'jquery',
        'backbone',
        'underscore'
    ],
    function($, Backbone, _) {
        var Message = Backbone.Model.extend({
            // TODO: availableTypes is currently unused
            availableTypes: ['info', 'error', 'warning', 'success'],
            defaults: {
                text: 'N/A',
                type: 'info', // affects appearance
                modal: false, // affects display method and appearance
                promptCallback: false, // supply a callback and this message becomes a prompt
                timeout: 20000, // message will auto-hide in this many ms, or pass false to persist
                closable: false
            },

            // override methods to allow using this model in the Messages collection
            // which has no `url`, as no persistence is required
            sync: function() { return null; },
            fetch: function() { return null; },
            save: function() { return null; }
        });
        return Message;
    }
);
