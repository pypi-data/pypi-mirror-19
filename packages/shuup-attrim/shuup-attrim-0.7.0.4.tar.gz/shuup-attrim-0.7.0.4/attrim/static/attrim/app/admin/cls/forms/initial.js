System.register(["app/admin/cls/forms/fields"], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var fields_1, OptionFormInitial;
    return {
        setters: [
            function (fields_1_1) {
                fields_1 = fields_1_1;
            }
        ],
        execute: function () {
            OptionFormInitial = (function () {
                function OptionFormInitial(type, form_container, form_number) {
                    this.type = type;
                    this.form_container = form_container;
                    this.form_number = form_number;
                    if (type === 20 /* TRANS_STR */) {
                        this.trans_text_values = new fields_1.default(this.form_container, this.form_number);
                    }
                }
                OptionFormInitial.prototype.remove = function () {
                };
                return OptionFormInitial;
            }());
            exports_1("default", OptionFormInitial);
        }
    };
});
//# sourceMappingURL=initial.js.map