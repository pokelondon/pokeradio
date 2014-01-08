/**
 * Progress Bar view
 */
define(['jquery',
        'backbone',
        'underscore',
        'iobind',
        ],
        function($, Backbone, _, ioBind){
            var View = Backbone.View.extend({
                $el: $('.progres-bar'),
                tagName: 'progress',

                initialize: function() {
                    $(window).on('progress', this.update, this);
                },

                update: function(evt) {
                    console.log(evt);
                    var percentage = 50;
                    this.$el.attr('value', percentage);
                }
            });
            return View;
        });

