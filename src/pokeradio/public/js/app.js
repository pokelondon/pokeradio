define([
    'jquery',
    'backbone',
    'underscore',
    'views/spotify/search-view',
    'views/playlist/playlist-view',
    'views/progress-bar'
    ],
    function($, Backbone, _, SearchView, PlaylistView, ProgressBar){
        window.PRAD = window.PRAD || {};
        window.PRAD.is_fox = (navigator.appVersion.indexOf("Win")!=-1);
        window.PRAD.app = {
            init: function(){
                this.searchview = new SearchView();
                this.playlistview = new PlaylistView();
                this.progressbar = new ProgressBar();

                var cutouff = new Date('2014-04-01 12:00:00');
                var options = ['Scatman (ski-ba-bop-ba-dop-bop)    ... adiba diba dibadib   ',
                               'Pokémon Theme   ',
                               'Hakuna Matata   ',
                               'Everything is AWESOME!!! #LOL #YOLO HAsHTaG #totes   '];
                var $input = $('#searchInput');
                var getWord = function getWord() {
                    var key = _.random(0, options.length -1);
                    return options[key].split("");
                };

                $(window).on('search:focus', function() {
                    if(cutouff < new Date()) {
                        return;
                    }
                    $input.val("");
                    var word = getWord();
                    $input.off('keydown').on('keydown', function(evt) {
                        evt.preventDefault();
                        var val = $input.val();
                        var letter = word.shift();
                        if (!letter) {
                            return;
                        }
                        $input.val(val + letter);
                        if(!word.length) {
                            $input.off('keydown');
                        }
                    });
                });
            }
        };
        return window.PRAD.app;
    }
);
