define(
    [   'jquery',
        'backbone',
        'underscore',
        'collections/messages',
        'views/messaging/message',
        'models/message',
        ],
    function($, Backbone,_ , messages, MessageView, Message){
        var MessageController = Backbone.View.extend({
            el: $('#MessagingContainer'),
            events: {},

            initialize: function() {
                this.collection = messages;
                this.collection.on('add', this.displayMessage, this);

                // TODO: listen for socket events to show messages
            },

            createMessage: function(options) {
                $.extend({}, new Message().defaults, options);
                this.collection.create(options);
                return this;
            },

            displayMessage: function(model) {
                var subview = new MessageView({
                    model: model
                });
                this.$el.append(subview.render().el);
                subview.show();
                return this;
            }
        });
        return MessageController;
    }
);
