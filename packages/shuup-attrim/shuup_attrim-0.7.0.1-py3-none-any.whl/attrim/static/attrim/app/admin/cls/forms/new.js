System.register(["app/api", "app/admin/cls/css_classes", "app/admin/cls/forms/fields"], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var api, classes, fields_1, OptionFormNew;
    return {
        setters: [
            function (api_1) {
                api = api_1;
            },
            function (classes_1) {
                classes = classes_1;
            },
            function (fields_1_1) {
                fields_1 = fields_1_1;
            }
        ],
        execute: function () {
            OptionFormNew = (function () {
                function OptionFormNew(args) {
                    this.fields = [];
                    this.formset = args.formset;
                    this.form_container = this.createFormContainer();
                    this.form_type = args.form_type;
                    this.form_number = args.form_number;
                    switch (this.form_type) {
                        case 1 /* INT */:
                        case 3 /* FLOAT */:
                            this.createFieldNumber();
                            break;
                        case 21 /* STR */:
                            this.createFieldText();
                            break;
                        case 20 /* TRANS_STR */:
                            this.createFieldTransText();
                            break;
                    }
                    this.createFieldOrder();
                    this.createFieldDelete();
                    this.formset.total_forms_count += 1;
                }
                OptionFormNew.prototype.appendTo = function (element) {
                    for (var _i = 0, _a = this.fields; _i < _a.length; _i++) {
                        var input = _a[_i];
                        this.form_container.appendChild(input);
                    }
                    element.appendChild(this.form_container);
                    if (this.form_type === 20 /* TRANS_STR */) {
                        // construct `TransTextValues` for it's lang switch
                        // call should be placed here
                        new fields_1.default(this.form_container, this.form_number);
                    }
                };
                OptionFormNew.prototype.remove = function () {
                    if (this.isNotTheLastOption()) {
                        return alert('You cant delete in-the-middle option. If you want to delete ' +
                            'this option - you need to delete all options below it.' +
                            'In other words: you can delete only the last option.');
                    }
                    this.formset.total_forms_count -= 1;
                    this.form_container.remove();
                };
                OptionFormNew.prototype.createFieldTransText = function () {
                    var trans_text_field = api.createElement({
                        tag: 'td',
                        cls: classes.field_value,
                    });
                    // create inputs for the field
                    for (var _i = 0, LANGUAGES_LIST_1 = LANGUAGES_LIST; _i < LANGUAGES_LIST_1.length; _i++) {
                        var lang_code = LANGUAGES_LIST_1[_i];
                        var text_field_input = api.createInput({
                            type: 'text',
                            name: "form-" + this.form_number + "-value_" + lang_code,
                            hidden: true,
                        });
                        if (lang_code === DEFAULT_LANG_CODE) {
                            // if it will be allowed to be empty, then `django-parler` will
                            // panic on attempt to get default field translation
                            text_field_input.required = true;
                        }
                        trans_text_field.appendChild(text_field_input);
                    }
                    this.fields.push(trans_text_field);
                };
                OptionFormNew.prototype.createFieldNumber = function () {
                    this.createField({
                        css_class: classes.field_value,
                        input_type: 'number',
                        input_name: "form-" + this.form_number + "-value",
                        input_step: 'any',
                    });
                };
                OptionFormNew.prototype.createFieldText = function () {
                    this.createField({
                        css_class: classes.field_value,
                        input_type: 'text',
                        input_name: "form-" + this.form_number + "-value",
                    });
                };
                OptionFormNew.prototype.createFieldDelete = function () {
                    var _this = this;
                    var field_delete = this.createField({
                        css_class: classes.field_delete,
                        input_type: 'button',
                        input_name: "form-" + this.form_number + "-DELETE",
                    });
                    field_delete.addEventListener('click', function () {
                        _this.remove();
                    });
                };
                OptionFormNew.prototype.createFieldOrder = function () {
                    this.createField({
                        css_class: classes.field_order,
                        input_type: 'number',
                        input_name: "form-" + this.form_number + "-order",
                    });
                };
                OptionFormNew.prototype.createField = function (args) {
                    var field = api.createElement({
                        tag: 'td',
                        cls: args.css_class,
                    });
                    var field_input = api.createInput({
                        type: args.input_type,
                        name: args.input_name,
                        hidden: args.input_hidden,
                        step: args.input_step,
                    });
                    field.appendChild(field_input);
                    this.fields.push(field);
                    return field;
                };
                OptionFormNew.prototype.createFormContainer = function () {
                    var form_container = api.createElement({
                        tag: 'tr',
                        cls: classes.formset_form,
                    });
                    return form_container;
                };
                OptionFormNew.prototype.isNotTheLastOption = function () {
                    return (this.formset.total_forms_count !== this.form_number);
                };
                return OptionFormNew;
            }());
            exports_1("default", OptionFormNew);
        }
    };
});
//# sourceMappingURL=new.js.map