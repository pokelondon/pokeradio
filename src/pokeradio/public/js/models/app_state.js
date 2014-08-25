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
                this.on('change:progress', this.updateTime, this);
            },

            /**
             * Handle socket data from server
             */
            update: function(data) {
                // TODO set other props
                this.set('state', data.playback_state);
                this.set('percentage', data.percentage);
                this.set('length', data['length']);
            },

            /**
             * Percentage has been updated by socket message
             * Set up interpolation till the next one given what we know now
             */
            percentage: function() {
                if (!this.get('length')) {
                    return;
                }
                this.percent_per_ms = 1 / (this.get('length') * 10);

                this.percent_per_period = this.percent_per_ms * this.period * 100;

                if('playing' !== this.get('state')) {
                    return;
                }

                this.set('progress', this.get('percentage'));

                this.clearInterval().startInterval();
            },

            startInterval: function() {
                var self = this;

                this.interval = setInterval(_.bind(function() {

                    this.set('progress', this.get('progress', 0) + this.percent_per_period);

                    if(this.get('progress') > 100) {
                        this.set('progress', 0);
                        this.clearInterval();
                    }
                }, this), this.period);

                return this;
            },

            /**
             * Whenever progress changes (interpolated or from socket)
             * update time property
             */
            updateTime: function() {
                var time = this.get('length') * (this.get('progress') / 100);
                this.set('time', time);
            },

            clearInterval: function() {
                clearInterval(this.interval);
                return this;
            }

        });
        return new Model();
    }
);

