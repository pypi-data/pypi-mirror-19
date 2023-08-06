import * as api from 'api'
import {HTMLElementLS} from 'ls-interface'

import * as selectors from 'admin/cls/selectors'
import OptionFormNew from 'admin/cls/forms/new'
import OptionFormInitial from 'admin/cls/forms/initial'
import {Type} from 'admin/cls/types'
import {OptionFormInterface} from 'admin/cls/forms/interface'


interface FormSetInterface {
    total_forms_count: number
}


// TODO: split OptionFormSet into controller and model?
export default class OptionFormSet implements FormSetInterface {
    private total_forms: number
    private type: number
    
    private cls_type_input: HTMLInputElement
    private cls_has_options: HTMLInputElement
    
    private total_forms_input: HTMLInputElement
    private formset_node: HTMLElementLS
    private formset_form_add: HTMLButtonElement
    private forms: Array<OptionFormInterface> = []

    /* public */
    
    constructor(args: {
        cls_type: string,
        cls_has_options: string,
        
        formset_total_forms: string,
        formset: string,
        formset_form_add: string,
    }) {
        this.cls_type_input    = api.qs(args.cls_type)
        this.cls_has_options   = api.qs(args.cls_has_options)
        
        this.total_forms_input = api.qs(args.formset_total_forms)
        this.formset_node      = api.qs(args.formset)
        this.formset_form_add  = api.qs(args.formset_form_add)
        
        this.total_forms = Number(this.total_forms_input.value) - 1
        this.type = Number(this.cls_type_input.value)
        
        this.initInitialForms()
        
        this.bindAddFormEvent()
        this.bindTypeChangeEvent()
    }

    public get total_forms_count(): number {
        return this.total_forms
    }
    public set total_forms_count(new_count: number) {
        this.total_forms = new_count
        this.total_forms_input.value = String(this.total_forms + 1)
    }
    
    /* events */

    private bindAddFormEvent() {
        this.formset_form_add.addEventListener('click', () => {
            this.addForm()
        })
    }
    
    private bindTypeChangeEvent() {
        this.cls_type_input.addEventListener('change', () => {
            this.type = Number(this.cls_type_input.value)
            this.removeAllForms()
            this.addForm()
        })
    }
    
    /* methods */

    private initInitialForms() {
        let formset_forms = this.formset_node.querySelectorAll(selectors.formset_form)
        let forms_count = formset_forms.length
        for (let form_number = 0; form_number < forms_count; form_number++) {
            // get initial formset_form container
            let form_container = formset_forms[form_number]
            // create new From
            let form = new OptionFormInitial(
                this.type, 
                form_container, 
                form_number
            )
            // push Form to forms
            this.forms.push(form)
        }
    }

    private addForm() {
        if (this.isTypeNotSetted()) {
            return alert('You must set the attribute type')
        }

        let form = this.createOptionForm(this.type)
        this.forms.push(form)
        form.appendTo(this.formset_node)
    }
    
    private createOptionForm(type: Type): OptionFormNew {
        let form_number = this.total_forms + 1
        return new OptionFormNew({
            formset: this,
            form_number: form_number,
            form_type: type,
        })
    }

    private removeAllForms() {
        for (let form of this.forms) {
            // `form` will handle `total_forms_count` itself, so no need
            // to worry about it's reset
            form.remove()
        }
        // reset forms list
        this.forms = []
    }

    private isTypeNotSetted(): boolean {
        if (this.type === 0) {
            return true
        } else {
            return false
        }
    }
}