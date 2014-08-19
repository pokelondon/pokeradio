define(
    [   'jquery',
        'backbone',
        'underscore'
    ],
    function($, Backbone, _) {
        var Model = Backbone.Model.extend({
            interval: null,

            percentage_interpolated: 0,
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
            },

            /**
             * Handle socket data from server
             */
            update: function(data) {
                // TODO set other props
                this.set('state', data.playback_state);
                this.set('percentage', data.percentage);
                this.set('length', data.length);
            },

            percentage: function(data) {
                console.log(this.get('percentage'));

                this.percent_per_ms = 1 / this.get('length') * 100;
                var increment_per_period = this.percent_per_ms * this.period;

                if('playing' !== this.get('state')) {
                    return;
                }
                this.set('progress', this.get('percentage'));

                this.clearInterval().startInterval();
            },

            startInterval: function() {
                var self = this;
                this.interval = setInterval(function() {
                    var time = 1 / self.percent_per_ms * self.get('percentage') / 1000;
                    self.set('time', time);

                    self.set('progress', self.get('progress') + increment_per_period);
                    if(self.get('progress') > 100) {
                        self.set('progress', 0);
                        self.clearInterval();
                    }
                }, this.period);

                return this;
            },

            clearInterval: function() {
                clearInterval(this.interval);
            }

        });
        return new Model();
    }
);

