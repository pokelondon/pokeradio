require.config({
    paths: {
        jquery: '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min',
        backbone: 'lib/backbone/backbone.min',
        underscore: 'lib/underscore/underscore',
        iobind: 'lib/backbone/backbone.iobind.min',
        iosync: 'lib/backbone/backbone.iosync.min',
        'jquery.cookie': '//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min'
    },
    shim:{
        'backbone': {
            deps: ['underscore','jquery'],
            exports: 'Backbone'
        },
        'underscore': {
            deps: ['jquery'],
            exports: '_'
        },
        'iosync': {
            deps: ['jquery', 'underscore', 'backbone'],
            exports: 'iosync'
        },
        'iobind': {
            deps: ['jquery', 'underscore', 'backbone', 'iosync'],
            exports: 'iobind'
        }
    }
});

require(['app'], function(app) {
    app.init();
});
