System.register(['api', 'admin/cls/selectors', 'admin/cls/css_classes'], function(exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var api, selectors, classes;
    var TransTextValues;
    return {
        setters:[
            function (api_1) {
                api = api_1;
            },
            function (selectors_1) {
                selectors = selectors_1;
            },
            function (classes_1) {
                classes = classes_1;
            }],
        execute: function() {
            TransTextValues = (function () {
                function TransTextValues(form_container, form_number) {
                    this.text_inputs = [];
                    this.form_container = form_container;
                    this.form_number = form_number;
                    this.initTextInputs();
                    this.createLangSwitch();
                }
                /**
                 * Get input from `form_container` and save them in `text_inputs`.
                 * And show the default input (by default language).
                 */
                TransTextValues.prototype.initTextInputs = function () {
                    for (var _i = 0, LANGUAGES_LIST_1 = LANGUAGES_LIST; _i < LANGUAGES_LIST_1.length; _i++) {
                        var lang_code = LANGUAGES_LIST_1[_i];
                        var text_input = this.form_container.querySelector("input[name=\"form-" + this.form_number + "-value_" + lang_code + "\"]");
                        this.text_inputs.push(text_input);
                        if (lang_code === DEFAULT_LANG_CODE) {
                            // show input with default lang
                            api.show(text_input);
                        }
                    }
                };
                TransTextValues.prototype.createLangSwitch = function () {
                    var _this = this;
                    // create language select input (choices i.e. ['en', 'fr', 'sw'])
                    var lang_switch = api.createSelectInput({
                        select_class: classes.field_lang_switch,
                        option_values: LANGUAGES_LIST,
                    });
                    lang_switch.addEventListener('change', function (event) {
                        var selected_lang_code = event.currentTarget;
                        var lang_code = selected_lang_code.value;
                        _this.showElementByLanguageKey(lang_code);
                    });
                    var value_inputs = this.form_container.querySelector(selectors.field_value);
                    value_inputs.appendChild(lang_switch);
                };
                TransTextValues.prototype.showElementByLanguageKey = function (lang_code) {
                    for (var _i = 0, _a = this.text_inputs; _i < _a.length; _i++) {
                        var text_input = _a[_i];
                        // match regex by text input name
                        // formset_form-0-value_en, formset_form-1-value_fr, ...
                        var match = /form-([0-9]+)-value_(\w+)/i.exec(text_input.name);
                        var matched_lang_code = match[2];
                        if (matched_lang_code === lang_code) {
                            // show chosen by user element
                            api.show(text_input);
                        }
                        else {
                            // and hide all others text elements
                            api.hide(text_input);
                        }
                    }
                };
                return TransTextValues;
            }());
            exports_1("default", TransTextValues);
        }
    }
});
