/**
 * Badge ListView
 */

define(
    [   'jquery',
        'backbone',
        'underscore',
        'collections/badges',
        'views/badge/badge-item',
        'views/messaging/controller',
        'jquery.cookie'
        ],
    function($, Backbone, _, Collection, ItemView, MessagingController){
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

                var lastSeen = $.cookie('lastSeenBadge', Number); // passing in function performs type conversion on the value
                if (typeof lastSeen === 'undefined' || parseInt(model.get('id'), 10) > lastSeen) {
                    $.cookie('lastSeenBadge', model.get('id'));

                    MessagingController.createMessage({
                        text: 'You just gained the ' + model.get('name') + ' badge!',
                        type: 'success',
                        timeout: false
                    });
                }
            }
        });

        // Single instance
        return new View();
    }
);
