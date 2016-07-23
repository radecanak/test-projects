// Conversion of CommonJS modul to work with RequireJS (example: node r.js -convert path/to/commonjs/modules/ path/to/output)
define(function (require, exports, module) {
    //CommonJS modul content
    var Backbone            = require('backbone');
    var saved_button = Backbone.View.extend({
        initialize: function(args) {
            _.bindAll(this, 'status');
            this.model.bind('change:status', this.status);
        },
        el : document.getElementById('saved_button'),
        status: function() {
            var state = this.model.get('status');
            if(state == "ok")
            {
                this.el.style.display = "inline-block";
            }
            else if(state == "refresh" || state == "cancel")
            {
                this.el.style.display = "none";
            }
        },
    });

    module.exports = saved_button;    
});