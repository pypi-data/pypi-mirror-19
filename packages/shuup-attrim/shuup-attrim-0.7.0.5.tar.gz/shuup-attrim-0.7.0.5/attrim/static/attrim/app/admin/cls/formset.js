System.register(["app/api", "app/admin/cls/selectors", "app/admin/cls/forms/new", "app/admin/cls/forms/initial"], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var api, selectors, new_1, initial_1, OptionFormSet;
    return {
        setters: [
            function (api_1) {
                api = api_1;
            },
            function (selectors_1) {
                selectors = selectors_1;
            },
            function (new_1_1) {
                new_1 = new_1_1;
            },
            function (initial_1_1) {
                initial_1 = initial_1_1;
            }
        ],
        execute: function () {
            OptionFormSet = (function () {
                /* public */
                function OptionFormSet(args) {
                    this.forms = [];
                    this.cls_type_input = api.qs(args.cls_type);
                    this.cls_has_options = api.qs(args.cls_has_options);
                    this.total_forms_input = api.qs(args.formset_total_forms);
                    this.formset_node = api.qs(args.formset);
                    this.formset_form_add = api.qs(args.formset_form_add);
                    this.total_forms = Number(this.total_forms_input.value) - 1;
                    this.type = Number(this.cls_type_input.value);
                    this.initInitialForms();
                    this.bindAddFormEvent();
                    this.bindTypeChangeEvent();
                }
                Object.defineProperty(OptionFormSet.prototype, "total_forms_count", {
                    get: function () {
                        return this.total_forms;
                    },
                    set: function (new_count) {
                        this.total_forms = new_count;
                        this.total_forms_input.value = String(this.total_forms + 1);
                    },
                    enumerable: true,
                    configurable: true
                });
                /* events */
                OptionFormSet.prototype.bindAddFormEvent = function () {
                    var _this = this;
                    this.formset_form_add.addEventListener('click', function () {
                        _this.addForm();
                    });
                };
                OptionFormSet.prototype.bindTypeChangeEvent = function () {
                    var _this = this;
                    this.cls_type_input.addEventListener('change', function () {
                        _this.type = Number(_this.cls_type_input.value);
                        _this.removeAllForms();
                        _this.addForm();
                    });
                };
                /* methods */
                OptionFormSet.prototype.initInitialForms = function () {
                    var formset_forms = this.formset_node.querySelectorAll(selectors.formset_form);
                    var forms_count = formset_forms.length;
                    for (var form_number = 0; form_number < forms_count; form_number++) {
                        // get initial formset_form container
                        var form_container = formset_forms[form_number];
                        // create new From
                        var form = new initial_1.default(this.type, form_container, form_number);
                        // push Form to forms
                        this.forms.push(form);
                    }
                };
                OptionFormSet.prototype.addForm = function () {
                    if (this.isTypeNotSetted()) {
                        return alert('You must set the attribute type');
                    }
                    var form = this.createOptionForm(this.type);
                    this.forms.push(form);
                    form.appendTo(this.formset_node);
                };
                OptionFormSet.prototype.createOptionForm = function (type) {
                    var form_number = this.total_forms + 1;
                    return new new_1.default({
                        formset: this,
                        form_number: form_number,
                        form_type: type,
                    });
                };
                OptionFormSet.prototype.removeAllForms = function () {
                    for (var _i = 0, _a = this.forms; _i < _a.length; _i++) {
                        var form = _a[_i];
                        // `form` will handle `total_forms_count` itself, so no need
                        // to worry about it's reset
                        form.remove();
                    }
                    // reset forms list
                    this.forms = [];
                };
                OptionFormSet.prototype.isTypeNotSetted = function () {
                    if (this.type === 0) {
                        return true;
                    }
                    else {
                        return false;
                    }
                };
                return OptionFormSet;
            }());
            exports_1("default", OptionFormSet);
        }
    };
});
//# sourceMappingURL=formset.js.map