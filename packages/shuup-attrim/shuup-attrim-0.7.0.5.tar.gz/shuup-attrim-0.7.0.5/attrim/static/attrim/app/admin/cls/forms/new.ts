import * as api from 'app/api'
import {HTMLElementLS} from 'app/ls-interface'

import * as classes from 'app/admin/cls/css_classes'
import {Type} from 'app/admin/cls/types'
import OptionFormSet from 'app/admin/cls/formset'
import TransTextValues from 'app/admin/cls/forms/fields'
import {OptionFormInterface} from 'app/admin/cls/forms/interface'


declare const LANGUAGES_LIST: Array<string>
declare const DEFAULT_LANG_CODE: string


export default class OptionFormNew implements OptionFormInterface {
    private formset: OptionFormSet
    private form_container: HTMLElementLS
    private form_type: Type
    private form_number: number
    
    private fields: Array<HTMLElementLS> = []

    constructor(args: {
        formset: OptionFormSet,
        form_number: number, 
        form_type: Type,
    }) {
        this.formset = args.formset
        this.form_container = this.createFormContainer()
        this.form_type = args.form_type
        this.form_number = args.form_number

        switch (this.form_type) {
            case Type.INT: 
            case Type.FLOAT:
                this.createFieldNumber()
                break
            case Type.STR:
                this.createFieldText()
                break
            case Type.TRANS_STR:
                this.createFieldTransText()
                break
        }
        this.createFieldOrder()
        this.createFieldDelete()
        
        this.formset.total_forms_count += 1
    }

    public appendTo(element: HTMLElementLS) {
        for (let input of this.fields) {
            this.form_container.appendChild(input)
        }
        element.appendChild(this.form_container)
        
        if (this.form_type === Type.TRANS_STR) {
            // construct `TransTextValues` for it's lang switch
            // call should be placed here
            new TransTextValues(
                this.form_container, 
                this.form_number
            )
        }
    }

    public remove() {
        if (this.isNotTheLastOption()) {
            return alert(
                'You cant delete in-the-middle option. If you want to delete ' +
                'this option - you need to delete all options below it.' + 
                'In other words: you can delete only the last option.'
            )
        }
        
        this.formset.total_forms_count -= 1
        this.form_container.remove()
    }

    private createFieldTransText() {
        let trans_text_field = api.createElement({
            tag: 'td',
            cls: classes.field_value,
        })
        
        // create inputs for the field
        for (let lang_code of LANGUAGES_LIST) {
            let text_field_input = api.createInput({
                type: 'text',
                name: `form-${this.form_number}-value_${lang_code}`,
                hidden: true,
            })
            if (lang_code === DEFAULT_LANG_CODE) {
                // if it will be allowed to be empty, then `django-parler` will
                // panic on attempt to get default field translation
                text_field_input.required = true
            }
            trans_text_field.appendChild(text_field_input)
        }
        
        this.fields.push(trans_text_field)
    }

    private createFieldNumber() {
        this.createField({
            css_class: classes.field_value,
            input_type: 'number',
            input_name: `form-${this.form_number}-value`,
            input_step: 'any',
        })
    }
    
    private createFieldText() {
        this.createField({
            css_class: classes.field_value,
            input_type: 'text',
            input_name: `form-${this.form_number}-value`,
        })
    }

    private createFieldDelete() {
        let field_delete = this.createField({
            css_class: classes.field_delete,
            input_type: 'button',
            input_name: `form-${this.form_number}-DELETE`,
        })
        field_delete.addEventListener('click', () => {
            this.remove()
        })
    }

    private createFieldOrder() {
        this.createField({
            css_class: classes.field_order,
            input_type: 'number',
            input_name: `form-${this.form_number}-order`,
        })
    }
    
    private createField(args: {
        css_class:     string,
        input_type:    string,
        input_name:    string,
        input_hidden?: boolean,
        input_step?:   string,
    }): HTMLElementLS {
        let field = api.createElement({
            tag: 'td',
            cls: args.css_class,
        })
        
        let field_input = api.createInput({
            type:   args.input_type,
            name:   args.input_name,
            hidden: args.input_hidden,
            step:   args.input_step,
        })
        field.appendChild(field_input)
        
        this.fields.push(field)
        
        return field
    }

    private createFormContainer(): HTMLElementLS {
        let form_container = api.createElement({
            tag: 'tr',
            cls: classes.formset_form,
        })
        return form_container
    }
    
    private isNotTheLastOption(): boolean {
        return (this.formset.total_forms_count !== this.form_number)
    }
}