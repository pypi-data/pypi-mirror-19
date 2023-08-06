import {HTMLElementLS} from 'app/ls-interface'

import {Type} from 'app/admin/cls/types'
import TranslTextValues from 'app/admin/cls/forms/fields'
import {OptionFormInterface} from 'app/admin/cls/forms/interface'


export default class OptionFormInitial implements OptionFormInterface {
    private type: Type
    private form_container: HTMLElementLS
    private form_number: number

    private trans_text_values: TranslTextValues

    constructor(
        type: Type, 
        form_container: HTMLElementLS, 
        form_number: number
    ) {
        this.type = type
        this.form_container = form_container
        this.form_number = form_number
        
        if (type === Type.TRANS_STR) {
            this.trans_text_values = new TranslTextValues(
                this.form_container, 
                this.form_number
            )
        }
    }
    
    public remove() {
        
    }
}