// Conversion of CommonJS modul to work with RequireJS (example: node r.js -convert path/to/commonjs/modules/ path/to/output)
define(function (require, exports, module) {
    //CommonJS modul content
    var Backbone            = require('backbone');
    var cancel_button_view = Backbone.View.extend({
        initialize: function(args) {
            _.bindAll(this, 'status');
            this.model.bind('change:status', this.status);
        },
        el : document.getElementById('cancel_button'),
        events : {
            "click" : "cancel"  
        },
        cancel : function() {          
            this.el.style.display = "none";
            this.model.set({"status" : "cancel"});
        },
        
        status: function() {
            var state = this.model.get('status');
            if(state == "ok")
            {
                this.el.style.display = "none";
            }
            else if(state == "refresh")
            {
                this.el.style.display = "inline-block";
            }
        },
    });

    module.exports = cancel_button_view;
});







