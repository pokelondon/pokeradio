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
            className: 'MessageItem',
            timer: false,
            events: {},

            initialize: function() {
                // set initial hidden state
                this.$el.hide();
            },

            render: function() {
                // TODO: render behaviour
                this.$el.addClass('MessageItem--' + this.model.get('type'));
                if (this.model.get('modal') === true) {
                    this.$el.addClass('MessageItem--modal');
                }
                this.$el.text(this.model.get('text'));
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
                this.$el.slideDown();

                // hide after a short interval if a timeout is set
                if (typeof this.model.get('timeout') === 'number') {
                    this.timer = window.setTimeout($.proxy(function() {
                        this.hide();
                    }, this), this.model.get('timeout'));
                }
                return this;
            },

            hide: function() {
                // TODO: hide behaviour
                // `modal` is different
                this.$el.slideUp();
                if (this.timer !== false) window.clearTimeout(this.timer);
                this.model.destroy();
                this.unbind();
                this.remove();
                return this;
            },

            renderPromptButtons: function(callback) {
                // TODO: some nicer markup would be good
                var $buttons = $("<div class='MessageItem-buttons' />"),
                    $yes = $("<button>Yes</button>"),
                    $no = $("<button>No</button>");
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
