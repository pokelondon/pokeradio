define(
    [   'jquery',
        'backbone',
        'underscore',
        'models/badge',
        'events'
        ],
    function($, Backbone,_ , Badge, _events){
        var View = Backbone.View.extend({
            tagName: 'div',
            className: 'Badge is-new',

            initialize: function(options) {
                this.model = options.model;
            },

            render: function() {
                this.$el.addClass('Badge--' + this.model.get('type'));
                this.$el.html($('<div></div>').addClass('Badge-title').text(this.model.get('type')));
                return this;
            },

            inserted: function() {
                this.$el.removeClass('is-new');
                console.log(this.$el);
                return this;
            }
        });
        return View;
    }
);
