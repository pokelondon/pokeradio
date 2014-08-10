define(
    [   'jquery',
        'backbone',
        'underscore',
        'models/message'
        ],
    function($, Backbone,_ , Message){
        var MessageView = Backbone.View.extend({
            model: Message,
            tagName: 'div',
            className: 'Alert',
            timer: false,
            events: {
                'click': 'click'
            },

            initialize: function() {

                _.bindAll(this, 'hide');

                this.listenTo(this.model, 'remove', this.onRemove);
            },

            render: function() {
                // TODO: render behaviour
                this.$el.addClass('Alert--' + this.model.get('type'));
                if (this.model.get('modal') === true) {
                    this.$el.addClass('Alert--modal');
                }
                this.$el.html('<p>' + this.model.get('text') + '</p>');

                if('good' === this.model.get('type')) {
                    this.$el.prepend($('<i class="fa fa-thumbs-up"></i>'));
                } else if('bad' === this.model.get('type')) {
                    this.$el.prepend($('<i class="fa fa-thumbs-down"></i>'));
                }

                if (typeof this.model.get('promptCallback') === 'function') {
                    this.$el.append(
                        this.renderPromptButtons(
                            this.model.get('promptCallback')
                        )
                    );
                }
                return this;
            },

            show: function() {
                // TODO: show behaviour
                // `modal` is different
                this.$el.addClass('show');

                if (this.model.get('modal') === true) {
                    $('body').addClass('modal-open');
                }

                // hide after a short interval if a timeout is set
                if (typeof this.model.get('timeout') === 'number') {
                    this.timer = window.setTimeout($.proxy(function() {
                        this.hide();
                    }, this), this.model.get('timeout'));
                }
                return this;
            },

            hide: function() {
                if (this.timer !== false) window.clearTimeout(this.timer);
                this.model.destroy();
                return this;
            },

            click: function() {
                if (!this.model.get('modal')) {
                    this.hide();
                }
            },

            /**
             * Responds to model deletion by removing the view via animation
             */
            onRemove: function() {
                var self = this;
                this.$el.addClass('remove');
                this.$el.on(PRAD.animationEndEvent, function() {
                    self.$el.remove();
                });

                if (this.model.get('modal')) {
                    $('body').removeClass('modal-open');
                }
            },

            renderPromptButtons: function(callback) {
                // TODO: some nicer markup would be good
                var $buttons = $("<div class='MessageItem-buttons' />"),
                    $yes = $("<button class='btn'>Yes</button>"),
                    $no = $("<button class='btn btn-danger'>No</button>");
                $yes.on('click', $.proxy(function(e) {
                    callback();
                    this.hide();
                }, this));
                $no.on('click', $.proxy(function(e) {
                    this.hide();
                }, this));
                $buttons.append($yes, $no);
                return $buttons;
            }
        });
        return MessageView;
    }
);
