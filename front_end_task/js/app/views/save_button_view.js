// Conversion of CommonJS modul to work with RequireJS (example: node r.js -convert path/to/commonjs/modules/ path/to/output)
define(function (require, exports, module) {
    //CommonJS modul content
    var Backbone            = require('backbone');
    var save_button_view = Backbone.View.extend({
        initialize: function(args) {
            _.bindAll(this, 'status');
            this.model.bind('change:status', this.status);
        },
        status: function() {
            var state = this.model.get('status');
            if(state == "cancel")
            {
                this.el.style.display = "none";
            }
            else if(state == "refresh")
            {
                this.el.style.display = "inline-block";
            }
            
        },
        el : document.getElementById('save_button'),
        events : {
            "click" : "ok"  
        },
        ok : function() {              
            this.el.style.display = "none";
            this.model.set({"status" : "ok"});
        }
    });

    module.exports = save_button_view;
});
