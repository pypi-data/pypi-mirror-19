import * as api from 'app/api'
import {HTMLElementLS} from 'app/ls-interface'
import {EventTargetLS} from 'app/ls-interface'

import * as selectors from 'app/admin/cls/selectors'
import * as classes from 'app/admin/cls/css_classes'


declare const LANGUAGES_LIST: Array<string>
declare const DEFAULT_LANG_CODE: string


export default class TransTextValues {
    private form_container: HTMLElementLS
    private form_number: number
    private text_inputs: Array<HTMLElementLS> = []
    
    
    constructor(form_container: HTMLElementLS, form_number: number) {
        this.form_container = form_container
        this.form_number = form_number
        
        this.initTextInputs()
        this.createLangSwitch()
    }

    /**
     * Get input from `form_container` and save them in `text_inputs`.
     * And show the default input (by default language).
     */
    private initTextInputs() {
        for (let lang_code of LANGUAGES_LIST) {
            let text_input = this.form_container.querySelector(
                `input[name="form-${this.form_number}-value_${lang_code}"]`
            )
            this.text_inputs.push(text_input)
            
            if (lang_code === DEFAULT_LANG_CODE) {
                // show input with default lang
                api.show(text_input)
            }
        }
    }

    private createLangSwitch() {
        // create language select input (choices i.e. ['en', 'fr', 'sw'])
        let lang_switch = api.createSelectInput({
            select_class: classes.field_lang_switch,
            option_values: LANGUAGES_LIST,
        })
        
        lang_switch.addEventListener('change', (event: any) => {
            let selected_lang_code: EventTargetLS = event.currentTarget
            let lang_code = selected_lang_code.value
            this.showElementByLanguageKey(lang_code)
        })
        
        let value_inputs = this.form_container.querySelector(
            selectors.field_value
        )
        value_inputs.appendChild(lang_switch)
    }

    private showElementByLanguageKey(lang_code: string) {
        for (let text_input of this.text_inputs) {
            // match regex by text input name
            // formset_form-0-value_en, formset_form-1-value_fr, ...
            let match = /form-([0-9]+)-value_(\w+)/i.exec(text_input.name)

            let matched_lang_code = match[2]
            if (matched_lang_code === lang_code) {
                // show chosen by user element
                api.show(text_input)
            } else {
                // and hide all others text elements
                api.hide(text_input)
            }
        }
    }
}