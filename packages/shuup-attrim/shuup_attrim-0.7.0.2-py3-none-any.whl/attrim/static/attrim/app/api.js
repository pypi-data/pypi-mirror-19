System.register([], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    function qs(query) {
        return document.querySelector(query);
    }
    /**
     * By default `querySelector` returns `NodeList`,
     * so to use `for (let _ of _)` we need to copy it into an array.
     */
    function qsAll(query) {
        var array = [];
        var node_list = document.querySelectorAll(query);
        for (var i = 0; i < node_list.length; i++) {
            array.push(node_list[i]);
        }
        return array;
    }
    function show(element) {
        element.removeAttribute('hidden');
    }
    function hide(element) {
        element.setAttribute('hidden', 'hidden');
    }
    function insertAfter(new_node, reference_node) {
        reference_node.parentNode.insertBefore(new_node, reference_node.nextSibling);
    }
    function createElement(args) {
        var element = document.createElement(args.tag);
        if (args.cls) {
            element.className = args.cls;
        }
        return element;
    }
    function createSelectInput(_a) {
        var select_class = _a.select_class, option_values = _a.option_values;
        var select_node = createElement({ tag: 'select' });
        select_node.className = select_class;
        for (var _i = 0, option_values_1 = option_values; _i < option_values_1.length; _i++) {
            var option_value = option_values_1[_i];
            var option_node = createElement({ tag: 'option' });
            option_node.value = option_value;
            option_node.text = option_value;
            select_node.appendChild(option_node);
        }
        return select_node;
    }
    function createInput(args) {
        var input = createElement({ tag: 'input' });
        input.type = args.type;
        if (args.name) {
            input.name = args.name;
        }
        if (args.hidden) {
            input.hidden = args.hidden;
        }
        if (args.class_name) {
            input.className = args.class_name;
        }
        if (args.value) {
            input.value = args.value;
        }
        if (args.step) {
            input.step = args.step;
        }
        return input;
    }
    function l(value) {
        console.log(value);
    }
    exports_1("qs", qs);
    exports_1("qsAll", qsAll);
    exports_1("show", show);
    exports_1("hide", hide);
    exports_1("insertAfter", insertAfter);
    exports_1("createElement", createElement);
    exports_1("createSelectInput", createSelectInput);
    exports_1("createInput", createInput);
    exports_1("l", l);
    return {
        setters: [],
        execute: function () {
        }
    };
});
//# sourceMappingURL=api.js.map