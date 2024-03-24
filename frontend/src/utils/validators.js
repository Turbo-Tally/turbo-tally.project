

export class Validations {
    static required (value) {
        if(value == "" || value == null) {
            return false
        }
        return true
    }
}