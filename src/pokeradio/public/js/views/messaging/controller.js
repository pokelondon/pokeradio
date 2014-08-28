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
                this.displayInitial();

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
                if(model.get('modal')) {
                    this.$el.parent().append(subview.render().el);
                } else {
                    this.$el.append(subview.render().el);
                }
                subview.show();
                return this;
            },

            /**
             * On load, display any messages rendered into the page by the view
             */
            displayInitial: function() {
                var self = this;
                _(this.collection.models).each(function(model) {
                    self.displayMessage(model);
                });
            }
        });
        return new MessageController();
    }
);
