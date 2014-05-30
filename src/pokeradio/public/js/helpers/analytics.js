define([],
    function() {
        var Analytics = {
            trackEvent: function(category, action, label, value) {
                if (typeof ga !== 'undefined') {
                    ga('send', 'event', category, action, label, value);
                }
            },
            trackPageview: function(url) {
                if (typeof ga !== 'undefined') {
                    ga('send', 'pageview', url);
                }
            },
            trackException: function(description) {
                if (typeof ga !== 'undefined') {
                    ga('send', 'exception', {
                        'exDescription': description
                    });
                }
            }
        };
        return Analytics;
    }
);
