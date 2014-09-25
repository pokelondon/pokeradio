/**
 * Badg ListView
 */

define(
    [   'jquery',
        'backbone',
        'underscore',
        'collections/badges',
        'views/badge/badge-item'
        ],
    function($, Backbone,_ , Collection, ItemView){
        var View = Backbone.View.extend({

            initialize: function() {
                this.$el = $('.js-badge-container');
                _.bindAll(this, 'added');
                this.collection = new Collection();
                this.listenTo(this.collection, 'add', this.added);
            },

            added: function(model) {
                // make an item view and insert it
                var item = new ItemView({model: model});

                this.$el.append(item.render().el);
                item.inserted();
            }
        });

        // Single instance
        return new View();
    }
);
