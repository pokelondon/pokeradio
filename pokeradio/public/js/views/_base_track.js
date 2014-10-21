/**
 * Base view for a track item.
 * Overload additional stuff
 */
define(['jquery',
        'backbone',
        'underscore',
        ],
        function($, Backbone, _){
            var TrackView = Backbone.View.extend({
                tagName: 'li',
                className: 'media',

                initialize: function(model, is_new){
                    this.model = model;
                    if(is_new) {
                        this.className += ' is-new';
                    }
                },

                render: function() {
                    var text = _.template(this.template, this.model.toJSON());
                    this.$el.html(text);
                    this.trigger('render');
                    return this;
                }
            });
            return TrackView;
        });


