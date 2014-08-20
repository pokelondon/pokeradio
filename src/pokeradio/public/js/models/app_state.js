define(
    [   'jquery',
        'backbone',
        'underscore'
    ],
    function($, Backbone, _) {
        var Model = Backbone.Model.extend({
            interval: null,

            period: 1000, // MS period between prog bar updates (interpolated)

            defaults: {
                state: 'stopped',
                percentage: 0, // Progress as reported from socket
                progress: 0, // Interpolated value for progress
            },

            initialize: function() {
                // Progress event from server
                this.listenTo(Backbone, 'play:progress', this.update, this);

                // Percentage reported from server, update interpolation
                this.on('change:percentage', this.percentage, this);

                this.on('change:time', function() {
                    console.log('Time', this.get('time'));
                }, this);
            },

            /**
             * Handle socket data from server
             */
            update: function(data) {
                // TODO set other props
                this.set('state', data.playback_state);
                this.set('percentage', data.percentage);
                this.set('length', data.track_length);
            },

            /**
             * Percentage has been updated by socket message
             * Set up interpolation till the next one given what we know now
             */
            percentage: function() {
                if (!this.get('length')) {
                    return;
                }
                this.percent_per_ms = 1 / (this.get('length') * 1000);

                this.percent_per_period = this.percent_per_ms * this.period;

                if('playing' !== this.get('state')) {
                    return;
                }

                this.set('progress', this.get('percentage'));

                this.clearInterval().startInterval();
            },

            startInterval: function() {
                var self = this;

                this.interval = setInterval(function() {
                    var time = self.get('length') * (self.get('progress') / 100);
                    self.set('time', time);

                    self.set('progress', self.get('progress', 0) + self.percent_per_period);

                    if(self.get('progress') > 100) {
                        self.set('progress', 0);
                        self.clearInterval();
                    }
                }, this.period);

                return this;
            },

            clearInterval: function() {
                clearInterval(this.interval);
                return this;
            }

        });
        return new Model();
    }
);

