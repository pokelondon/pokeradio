/**
 * Progress Bar view
 */
define(['jquery',
        'backbone',
        'underscore',
        'collections/progress-proxy',
        ],
        function($, Backbone, _, Collection){
            var View = Backbone.View.extend({
                tagName: 'progress',
                interval: null,
                percentage_interpolated: 0,
                period: 100, // MS period between prog bar updates (interpolated)

                initialize: function() {
                    this.$el = $('.progress-bar');
                    _.bindAll(this, 'update');
                    this.collection = new Collection();

                    // Get events from the collection, which gets them from the
                    // socket connection.
                    this.listenTo(this.collection, 'play:progress', this.update);
                },

                /**
                 * Update the progress bar from the message back from the server
                 * Between updates, interpolate the value to keep the bar moving.
                 * Using Maffs (TM)
                 */
                update: function(data) {
                    var self = this;
                    var percent_per_ms = 1 / data['length'] * 100;
                    var increment_per_period = percent_per_ms * this.period;

                    clearInterval(this.interval);

                    // Update with real figure
                    this.percentage_interpolated = data.percentage;

                    // Start new interval to carry on interpolating
                    this.interval = setInterval(function() {
                        self.$el.attr('value', self.percentage_interpolated);
                        self.percentage_interpolated += increment_per_period;
                        if(self.percentage_interpolated > 100) {
                            self.percentage_interpolated = 0;
                        }
                    }, self.period);
                }
            });
            return View;
        });

