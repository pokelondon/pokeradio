define(
    [],
    function () {
		return {
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
				if ( el.css('display') == 'none' ) {
					el.show();
					setTimeout(function(){
						el.removeClass('fadeout');
					},10);
					
				}else {
					
					el.one('webkitTransitionEnd',function(){
						el.hide();
					});
					el.addClass('fadeout');
				}
			},
		};
		
	}
);


