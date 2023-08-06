System.register(['admin/cls/css_classes'], function(exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var classes;
    var cls_type, cls_has_options, formset_total_forms, formset, formset_form_add, formset_form, field_value, field_lang_switch, field_order, field_delete;
    return {
        setters:[
            function (classes_1) {
                classes = classes_1;
            }],
        execute: function() {
            exports_1("cls_type", cls_type = '#id_type');
            exports_1("cls_has_options", cls_has_options = '#id_has_options');
            exports_1("formset_total_forms", formset_total_forms = '#id_form-TOTAL_FORMS');
            exports_1("formset", formset = '#formset');
            exports_1("formset_form_add", formset_form_add = '#formset-form-add');
            exports_1("formset_form", formset_form = "." + classes.formset_form);
            exports_1("field_value", field_value = "." + classes.field_value);
            exports_1("field_lang_switch", field_lang_switch = "." + classes.field_lang_switch);
            exports_1("field_order", field_order = "." + classes.field_order);
            exports_1("field_delete", field_delete = "." + classes.field_delete);
        }
    }
});
