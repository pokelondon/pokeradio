/**
 * Progress Bar view
 */
define(['jquery',
        'backbone',
        'underscore',
        'collections/progress-proxy'
        ],
        function($, Backbone, _, Collection){
            var View = Backbone.View.extend({
                tagName: 'progress',
                className: 'progress-bar',
                interval: null,
                percentage_interpolated: 0,
                period: 1000, // MS period between prog bar updates (interpolated)

                initialize: function() {
                    _.bindAll(this, 'update', 'updateProgressBar');
                    this.collection = new Collection();

                    // Get events from the collection, which gets them from the
                    // socket connection.
                    this.listenTo(this.collection, 'play:progress', this.update);
                    this.on('play:progress:interpolated', this.updateProgressBar, this);
                    this.on('play:progress:interpolated', this.updateVar, this);
                },

                // TODO unload
                // Clear interval and remove $el

                render: function() {
                    this.$el.attr('max', 100);
                    return this;
                },

                /**
                 * Update the progress bar from the message back from the server
                 * Between updates, interpolate the value to keep the bar moving.
                 * Using Maffs (TM)
                 */
                update: function(data) {
                    var self = this;
                    this.percent_per_ms = 1 / data['length'] * 100;
                    var increment_per_period = this.percent_per_ms * this.period;

                    this.updatePlayState(data['playback_state']);

                    clearInterval(this.interval);

                    // Only continue to animate if the state is playing
                    if('playing' !== data['playback_state']) {
                        return;
                    }

                    // Update with real figure
                    this.percentage_interpolated = data.percentage;

                    // Start new interval to carry on interpolating
                    this.interval = setInterval(function() {
                        self.trigger('play:progress:interpolated', self.percentage_interpolated);
                        self.percentage_interpolated += increment_per_period;
                        if(self.percentage_interpolated > 100) {
                            self.percentage_interpolated = 0;
                            clearInterval(self.interval);
                        }
                    }, self.period);
                },

                updateProgressBar: function(percentage) {
                    this.$el.attr('value', percentage);
                },

                /**
                 * Trigger an event for each interpolated progress event
                 * for the estimated time elapsed through the current track
                 */
                updateVar: function(percentage) {
                    var time = 1 / this.percent_per_ms * percentage / 1000;
                    $(window).trigger('play:progress:interpolated:seconds', time);
                },

                updatePlayState: function(state) {
                    this.$el.removeClass('playing, paused, stopped').addClass(state);
                }
            });
            return View;
        });

