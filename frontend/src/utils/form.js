import { ref, watch } from "vue"

export class Form 
{
    constructor() {
        this.inputs = {}
        this._validators = {}
        this._errors = {}
        this.allowSubmission = ref(true)
    }

    requireAll(isRequired) {
        if(isRequired) {
            this.disableSubmission()  
            const self = this
            
            for(let input of Object.values(this.inputs)) {
                watch(input, () => {
                    const containsEmptyFields = self.containsEmptyFields()
                    const hasErrors = self.hasErrors() 
                    if(containsEmptyFields || hasErrors) {
                        self.disableSubmission() 
                    } else {
                        self.enableSubmission()
                    }
                })
            }
        } else {
            this.enableSubmission() 
        }
    }

    addField(input, validate) {
        this.inputs[input] = ref(null)
        this._validators[input] = (value) => {
            return validate(value)
        }
        this._errors[input] = false
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

    containsEmptyFields() {
        const values = Object.values(this.inputs).map(x => x.value)
        for(let value of values) {
            if(value == null || value == "") {
                return true 
            }
        }
        return false
    }

    hasErrors() {
        const errors = Object.values(this._errors) 
        for(let error of errors) {
            if(error) {
                return true 
            }
        }
        return false
    }

    handle(field) {
        const fieldValue = this.inputs[field].value 
        this._errors[field] = !this._validators[field](fieldValue)
        console.log(this._errors)
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

