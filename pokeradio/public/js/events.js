define([],
    function () {
        window.PRAD = window.PRAD || {};

        /**
        * Sniff for a suitably named transition end event
        */
        function whichTransitionEvent() {
            var t;
            var el = document.createElement('fakeelement');
            var transitions = {
                'transition': 'transitionend',
                'MSTransition': 'msTransitionEnd',
                'MozTransition': 'transitionend',
                'WebkitTransition': 'webkitTransitionEnd'
            };
            for(t in transitions){
                if( el.style[t] !== undefined ){
                    return transitions[t];
                }
            }
        }

        function whichAnimationEvent() {
            var t;
            var el = document.createElement('fakeelement');
            var animations = {
                'animation': 'animationend',
                'MSAnimation': 'msanimationEnd',
                'MozAnimation': 'animationend',
                'WebkitAnimation': 'webkitAnimationEnd'
            };
            for(t in animations){
                if( el.style[t] !== undefined ){
                    return animations[t];
                }
            }
        }

        window.PRAD.transitionEndEvent = window.PRAD.transitionEndEvent || whichTransitionEvent();
        window.PRAD.animationEndEvent = window.PRAD.animationEndEvent || whichAnimationEvent();

        return PRAD;
});
