define(
    [   'jquery',
        'backbone',
        'underscore',
        'models/badge'
    ],
    function($, Backbone, _, Badge){
        var Collection = Backbone.Collection.extend({
            model: Badge,
            url: 'api/badges/' + PRAD.user_id + '/',

            initialize: function() {
                _.bindAll(this, 'badgeAdded');
                this.listenTo(Backbone, 'badge:add', this.badgeAdded);
                this.fetch();
            },
            badgeAdded: function(user_id) {
                if(user_id === PRAD.user_id) {
                    this.fetch();
                }
            }
        });
        return Collection;
    }
);
