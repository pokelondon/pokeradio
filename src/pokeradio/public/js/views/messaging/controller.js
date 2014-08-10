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
                this.createMessage({
                    text: "An message",
                    modal: true,
                    type: 'bad',
                    timeout: false,
                    promptCallback: function() {
                        console.log(arguments);
                    }
                });
                setTimeout(function() {
                    self.createMessage({
                        text: "An uva message this one is a bit longer to see what happens when its a bit longer than what the other ones are",
                        modal: false,
                        type: 'good'
                    });
                }, 400);

                var self = this;
                setTimeout(function() {
                    self.createMessage({
                        text: "An uva nuva message",
                        type: 'bad'
                    });
                }, 600);
                setTimeout(function() {
                    self.createMessage({
                        text: "An uva aaanuvanuva message"
                    });
                }, 1600);
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
            }
        });
        return new MessageController();
    }
);
