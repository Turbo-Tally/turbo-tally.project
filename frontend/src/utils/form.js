import { ref, watch, nextTick } from "vue"

export class Form 
{
    constructor() {
        this.inputs = ref({})
        this._validators = {}
        this._errors = ref({})
        this.allowSubmission = ref(true)
    }

    requireAll(isRequired) {
        const self = this
        if(!isRequired) {
            self.enableSubmission()
        } else {
            self.disableSubmission()
            self.guardSubmission()
        }
    }

    handleChange() {
        let self = this
        if(!self.containsEmptyFields() && !self.hasErrors()) {
            self.allowSubmission.value = true
        } else {
            self.allowSubmission.value = false
        }
    }

    guardSubmission() {
        const self = this
        watch(self.inputs, () => {
            self.handleChange()
        }, {
            deep: true
        })
    }

    values() {
        const values = {} 
        for(let key in this.inputs.value) {
            values[key] = this.inputs.value[key]
        }
        return values
    }

    addField(input, validate) {
        this.inputs.value[input] = null
        this._validators[input] = (value) => {
            return validate(value)
        }
        this._errors.value[input] = false
    }

    field(input) {
        return this.inputs[input].value
    }

    json() {
        const json = {}
        for(let key in this.inputs) {
            json[key] = this.inputs[key].value
        }
        return json
    }

    errors() {
        return this._errors
    }

    hasError(field) {
        return this._errors.value[field]
    }

    containsEmptyFields() {
        const values = Object.values(this.inputs.value).map(x => x)
        for(let value of values) {
            if(value == null || value == "") {
                return true 
            }
        }
        return false
    }

    hasErrors() {
        const errors = Object.values(this._errors.value)
        for(let error of errors) {
            if(error) {
                return true 
            }
        }
        return false
    }

    handle(field) {
        const fieldValue = this.inputs.value[field] 
        this._errors.value[field] = !this._validators[field](fieldValue)
        this.handleChange()
    }

    enableSubmission() {
        this.allowSubmission.value = true 
    }

    disableSubmission() {
        this.allowSubmission.value = false
    }

    canSubmit() {
        return this.allowSubmission.value
    }
}

