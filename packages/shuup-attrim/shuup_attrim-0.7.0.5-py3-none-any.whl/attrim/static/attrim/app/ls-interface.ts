/**
 * For some reason `lib.es6.d.ts` doesn't define currently valid methods of
 * DOM objects. So... I decided to extend default TS interface to fix this.
 *
 * `LS` - stands for Living Standard (AFAIK it is)
 */


export interface HTMLElementLS extends HTMLElement {
    name: string
    dataset: any
    style: CSSStyleDeclaration

    // Why `any` return type? Well, because I sick of this freaking default TS
    // interface. It is just wrong (at least on the moment of the note it's
    // goddamn mess).
    //
    // I hope that some day I will be able to declare it just like `HTMLElement`,
    // but this day still didn't came yet.
    querySelector(selectors: string): any
    querySelectorAll(selectors: string): NodeListOf<any>
}

export interface EventTargetLS extends EventTarget {
    value: string
}
