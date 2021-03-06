define(['jquery',
        'underscore',
        'backbone'],
    function ($, _, Backbone) {
        obj = _.extend({
            convertToMinutes: function(length){
                //Length in seconds given
                toseconds = Math.ceil(length);
                minutes = Math.floor(toseconds / 60);
                seconds = toseconds%60;
                if (10 > seconds){
                    seconds = '0'+seconds;
                }

                return minutes + ':' + seconds;
            },
            toggleFade: function(el){
                el.fadeToggle();
            },
            onPageBottom: function(e){
                h = $('#addTrackView').scrollTop() + $('#addTrackView').height() - $('.add-track-view-wrapper').height();
                if (h === 0){
                    this.trigger("pageBottom");
                    console.log(e);
                }
            }

        }, Backbone.Events);

        _.bindAll(obj, 'onPageBottom');

        return obj;
    }
);
