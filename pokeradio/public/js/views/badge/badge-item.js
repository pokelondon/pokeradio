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
            className: 'Badge Badge--small is-new',

            initialize: function(options) {
                this.model = options.model;
            },

            render: function() {
                this.$el.addClass('Badge--' + this.model.get('slug'));
                this.$el.html($('<div></div>').addClass('Badge-title').text(this.model.get('name')));
                return this;
            },

            inserted: function() {
                var self = this;
                setTimeout(function() {
                    self.$el.removeClass('is-new');
                }, 200);
                return this;
            }
        });
        return View;
    }
);
