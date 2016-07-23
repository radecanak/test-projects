define(function (require) { 
    var StateModel = require('app/models/statemodel');
    var SaveButtonView = require('app/views/save_button_view');
    var SavedButtonView = require('app/views/saved_button_view');
    var CancelButtonView = require('app/views/cancel_button_view');
    var LaunchMinimizedView = require('app/views/launch_minimized_view');
    var LaunchStartView = require('app/views/launch_start_view');
    
    var stateModel = new StateModel;
    var saveButtonView = new SaveButtonView({model : stateModel});
    var savedButtonView = new SavedButtonView({model : stateModel});
    var cancelButtonView = new CancelButtonView({model : stateModel});
    var launchMinimizedView = new LaunchMinimizedView({model : stateModel});
    var launchStartView = new LaunchStartView({model : stateModel});
    
});