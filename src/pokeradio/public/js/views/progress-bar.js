/**
 * Progress Bar view
 */
define(['jquery',
        'backbone',
        'underscore',
        'models/app_state'
        ],
        function($, Backbone, _, appState){
            var View = Backbone.View.extend({
                tagName: 'progress',
                className: 'progress-bar',

                initialize: function() {
                    _.bindAll(this, 'update');

                    // Global Mediator events triggered by socket message
                    this.listenTo(appState, 'change:progress', this.update);
                    this.listenTo(appState, 'change:state', this.updatePlayState);
                },

                render: function() {
                    this.$el.attr('max', 100);
                    return this;
                },

                /**
                 * Update the progress bar from the message from the server
                 */
                update: function() {
                    this.$el.attr('value', appState.get('progress'));
                },

                updatePlayState: function() {
                    this.$el.removeClass('playing, paused, stopped').addClass(appState.get('state'));
                }
            });
            return View;
        });

