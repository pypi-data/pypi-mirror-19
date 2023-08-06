System.register(["app/admin/cls/formset", "app/admin/cls/selectors"], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var formset_1, selectors, formset;
    return {
        setters: [
            function (formset_1_1) {
                formset_1 = formset_1_1;
            },
            function (selectors_1) {
                selectors = selectors_1;
            }
        ],
        execute: function () {
            formset = new formset_1.default({
                cls_type: selectors.cls_type,
                cls_has_options: selectors.cls_has_options,
                formset_total_forms: selectors.formset_total_forms,
                formset: selectors.formset,
                formset_form_add: selectors.formset_form_add,
            });
        }
    };
});
//# sourceMappingURL=main.js.map