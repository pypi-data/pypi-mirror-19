import {HTMLElementLS} from 'app/ls-interface'


export function qs(query: string): any {
    return document.querySelector(query)
}


/**
 * By default `querySelector` returns `NodeList`,
 * so to use `for (let _ of _)` we need to copy it into an array.
 */
export function qsAll(query: string): Array<any> {
    let array = []

    let node_list = document.querySelectorAll(query)
    for (let i = 0; i < node_list.length; i++) {
        array.push(node_list[i])
    }

    return array
}


export function show(element: HTMLElementLS) {
    element.removeAttribute('hidden')
}
export function hide(element: HTMLElementLS) {
    element.setAttribute('hidden', 'hidden')
}


export function insertAfter(new_node, reference_node) {
    reference_node.parentNode.insertBefore(new_node, reference_node.nextSibling)
}


export function createElement(args: {
    tag: string,
    cls?: string,
}): any {
    let element = document.createElement(args.tag)
    if (args.cls) {
        element.className = args.cls
    }
    return element
}


export function createSelectInput({
    select_class, option_values
}): HTMLSelectElement {
    let select_node = createElement({tag: 'select'})
    select_node.className = select_class
    for (let option_value of option_values) {
        let option_node = createElement({tag: 'option'})
        option_node.value = option_value
        option_node.text = option_value
        select_node.appendChild(option_node)
    }
    return select_node
}


export function createInput(args: {
    type: string,
    class_name?: string,
    name?: string,
    value?: string,
    step?: string,
    hidden?: boolean,
}): HTMLInputElement {
    let input = createElement({tag: 'input'})
    input.type = args.type
    
    if (args.name) {
        input.name = args.name
    }
    if (args.hidden) {
        input.hidden = args.hidden
    }
    if (args.class_name) {
        input.className = args.class_name
    }
    if (args.value) {
        input.value = args.value
    }
    if (args.step) {
        input.step = args.step
    }
    
    return input
}

export function l(value: any) {
    console.log(value)
}

