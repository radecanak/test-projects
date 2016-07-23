require.config({

    baseUrl: 'js/lib',

    paths: {
        app: '../app',
        jquery: 'jquery-1.12.3.min',
        backbone:'backbone-min',
        underscore : 'underscore-min',
    },
    // Sets the configuration for your third party scripts that are not AMD compatible
    shim: {
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone' //attaches "Backbone" to the window object
        },
    }
});

// Start loading the main app file. 
// Application logic is there.
requirejs(['app/main']);