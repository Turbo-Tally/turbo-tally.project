import { ref, watch, nextTick } from "vue"

export class Form 
{
    constructor() {
        this.inputs = ref({})
        this._validators = {}
        this._errors = ref({})
        this.allowSubmission = ref(true)
        this.guardMode = "watch"
    }

    requireAll(isRequired, guardFn = () => { return true }) {
        const self = this
        if(!isRequired) {
            self.enableSubmission()
        } else {
            self.disableSubmission()
            self.guardSubmission(guardFn)
        }
    }

    handleChange(guardFn = () => { return true }) {
        let self = this
        if(
            !self.containsEmptyFields() && 
            !self.hasErrors() && 
            guardFn()    
        ) {
            self.allowSubmission.value = true
        } else {
            self.allowSubmission.value = false
        }
    }

    guardSubmission(guardFn = () => { return true }) {
        const self = this
        if(this.guardMode == "watch") {
            watch(self.inputs, () => {
                self.handleChange(guardFn)
            }, {
                deep: true
            })
        } else if (this.guardMode == "change") {
            self.onItemChange = (value) => {
                self.handleChange(guardFn)
            }
        }
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
        this._validators[input] = validate
        this._errors.value[input] = {}

        if(typeof(validate) == "function") {
            this._errors.value[input] = false
        } else {
            for(let key in validate) {
                this._errors.value[input][key] = false
            }
        }
    }


    // source: https://stackoverflow.com/a/54246516
    camelToUnderscore(key) {
        var result = key.replace( /([A-Z])/g, " $1" );
        return result.split(' ').join('_').toLowerCase();
    }

    json(convertToSnakeCase = true) {
        const json = {}
    
        
        for(let key in this.inputs.value) {
            const origKey = key
            let newKey = origKey
            if(convertToSnakeCase)
                newKey = this.camelToUnderscore(key)
            json[newKey] = this.inputs.value[origKey]
        }

        return json
    }

    errors() {
        return this._errors
    }

    hasError(field, suberror = null) {
        if(suberror != null) {
            if(typeof(this._errors.value[field]) == "object") {
                return this._errors.value[field][suberror] != false
            }
            return false
        } else {
            return this._errors.value[field] != false
        }
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
            if(typeof(error) == "boolean") {
                if(error) {
                    return true
                } 
            } else {
                for(let suberror of Object.values(error)) {
                    if(suberror) {
                        return true
                    }
                }
            }
        }
        return false
    }

    async handle(field) {
        const fieldValue = this.inputs.value[field]
        const validators = this._validators[field]
        if(typeof(validators) == "function") {
            const errorValue = !(await validators(fieldValue))
            this._errors.value[field] = errorValue
        } else {
            if(!(field in this._errors.value)) {
                this._errors.value[field] = {}
            }

            if(this._errors.value[field] == false) {
                this._errors.value[field] = {}
            }

            for(let validatorName in validators) {
                this._errors.value[field][validatorName] = 
                    !(await validators[validatorName](fieldValue))
                if(this.guardMode == "change")
                    this.onItemChange(fieldValue)
            }
        }
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
