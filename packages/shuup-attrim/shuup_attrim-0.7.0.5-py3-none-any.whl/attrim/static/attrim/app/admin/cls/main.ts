import OptionFormSet from 'app/admin/cls/formset'
import * as selectors from 'app/admin/cls/selectors'



let formset = new OptionFormSet({
    cls_type:            selectors.cls_type,
    cls_has_options:     selectors.cls_has_options,

    formset_total_forms: selectors.formset_total_forms,
    formset:             selectors.formset,
    formset_form_add:    selectors.formset_form_add,
})
