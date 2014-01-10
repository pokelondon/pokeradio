define(['jquery',
        'backbone',
        'underscore',
        ],
        function($,Backbone,_){
            MopidyTrack = Backbone.Model.extend({
                idAttribute: "id",
                wasPlaying: false,
                defaults: {
                    isPlaying: false
                },

                initialize: function() {
                    this.collection.on('change:played', this.checkIsPlaying, this);
                    console.log(this.attributes);
                },

                checkIsPlaying: function() {
                    // Find next unplayed track
                    var current_track = this.collection.findWhere({played: false });
                    if(this.id == current_track.id) {
                        this.set('isPlaying', true);
                    }else{
                        this.set('isPlaying', false);
                    }
                }
            });
            return MopidyTrack;
        });
