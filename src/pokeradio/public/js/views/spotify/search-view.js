define(['jquery',
<<<<<<< HEAD
        'backbone',
        'underscore',
        'collections/spotify-tracks',
        'iobind',
        'utils',
        'views/spotify/track'
        ],
        function($, Backbone,_ , SpotifyTracks, ioBind, utils, TrackView){
            var SearchView = Backbone.View.extend({
                el: $('#AddTrackView'),
                events:{
                    'submit #searchForm': 'search',
                    'click .exit-icon': 'closeView'
                },

                initialize: function(){
                    this.collection = new SpotifyTracks();
                    this.collection.on('results', this.render, this);
                    this.$list = this.$el.find('.track-listing-container');
                },

                /**
                 * Repopulate listign with new track view instances when the
                 * collection changes
                 */
                render: function() {
                    var self = this;
                    this.$list.html('');
                    _(this.collection.models).each(function(model) {
                        var view = new TrackView(model);
                        self.$list.append(view.render().el);
                    });
                    return this;
                },

                /**
                 * DO search query
                 */
                search: function(evt){
                    this.collection.search($('#searchInput').val());
                    evt.preventDefault();
                },

                closeView: function(){
                    utils.toggleFade(this.$el);
                }
            });
            return SearchView;
        });
=======
		'backbone',
		'underscore',
		'collections/spotify-tracks',
		'iobind',
		'text!template/spotify/list.html',
		'utils'
		],
		function($,
				Backbone,
				_,
				SpotifyTracks,
				ioBind,
				tl_template,
				utils) {

	var searchView = Backbone.View.extend({
		el: $('#addTrackView'),
		initialize: function(){
			_.bindAll(this, 'renderNextpage');
			this.spotifyTracks = new SpotifyTracks();
			utils.on('pageBottom', this.renderNextpage);
			
		},
		events:{
			'submit #searchForm': 'render',
			'click .track-listing-container li': 'addTrack',
			'click .exit-icon': 'closeView'
		},
		render: function(e){
			this.query = {q: $('#searchInput').val(), page: 1};
			this.writeToPage(false);
			return false;
		},
		renderNextpage: function(){
			var info = this.spotifyTracks.info;
			info.pageTotal = Math.ceil(info.num_results/info.limit);
			if (info.page < info.pageTotal){
				this.query.page++;
				this.writeToPage(true);

			}
			console.log(info);

		},
		writeToPage: function(append){

			this.spotifyTracks.fetch({
				data : $.param(this.query),
				success:function(data){
					var template = _.template(tl_template, {metadata:data.models, append:append});
					if(append){
						$('#mediaListHits').append(template);
					}else{
						$('.track-listing-container').html(template);
					}
					
				}
			});
		},
		addTrack:function(e){
			if($(e.currentTarget).hasClass('selected')){
				alert('You have already added this track');
				return;
			}
			$(e.currentTarget).addClass('selected');
			var track_payload = this.spotifyTracks.getTrack($(e.currentTarget).data('href'));
			$(e.currentTarget).find('.add-icon-wrap').html('<span class="minus-icon"></span>');
			socket.emit('add_track',JSON.stringify(track_payload));
		},
		closeView: function(){
			$('body').removeClass('modal-open');
			utils.toggleFade($('#addTrackView'));
			$(this.el).unbind('scroll',utils.onPageBottom);
		},
	});

	return searchView;

});
>>>>>>> master
