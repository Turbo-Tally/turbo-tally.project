import { httpClient } from "@/utils/http-client.js"

export class Validators {
    static required (value) {
        if(value == "" || value == null) {
            return false
        }
        return true
    }

    static username (value) {
        const minLength = value.length >= 3 
        const maxLength = value.length <= 20 
        const regex = 
            (new RegExp("^[A-Za-z0-9\.\_]+$"))
                .test(value) 
        return minLength && maxLength && regex
    }
    
    static email (value) {
        const minLength = value.length >= 4 
        const maxLength = value.length <= 320 
        const regex = 
            /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()\.,;\s@\"]+\.{0,1})+([^<>()\.,;:\s@\"]{2,}|[\d\.]+))$/
                .test(value)
        return minLength && maxLength && regex
    }

    static password (value) {
        const minLength = value.length >= 8 
        const maxLength = value.length <= 255 
        
        const hasNumber = 
            (new RegExp(".*[0-9].*"))
                .test(value) 
            
        const hasBigLetter = 
            (new RegExp(".*[A-Z].*"))
                .test(value) 

        const hasSmallLetter = 
            (new RegExp(".*[a-z].*"))
                .test(value)
 
        const hasSymbol = 
            (new RegExp(
                ".*" +
                "[\\~\\!\\@\\#\\$\\%\\^\\&\\*\\(\\)\\_\\+\\`\\-\\=\\[\\]\\{\\}\\;\\'\\:\"\\,\\.\\/<\\>\\?]" +
                ".*"
            ))
                .test(value) 

        return (
            (minLength && maxLength) && 
            (hasNumber && hasBigLetter && hasSmallLetter && hasSymbol)
        )
    }

    static birthdate (value) {
        // source: https://stackoverflow.com/a/64928191
        function getAge(dob) {
            var today = new Date();
            var birthDate = new Date(dob);
            var age = today.getFullYear() - birthDate.getFullYear();
            var m = today.getMonth() - birthDate.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }    
            return age;
        }

        return getAge(value) >= 18
    }

    static gender (value) {
        return value == "M" || value == "F"
    }

    static mobileNo (value) {
        const is11Characters = value.toString().length == 11 
        const regex = 
            (new RegExp("09[0-9]{9}")) 
        return is11Characters && regex 
    }

    static verifCode (value) {
        const is6Numbers = value.toString().length == 6 
        const regex =  
            (new RegExp("[0-9]{6}")) 
                .test(value)
        return is6Numbers && regex
    }

    static pollTitle (value) {
        return value.length >= 5 && value.length <= 256 
    }

    static pollChoice (value) {
        return value.length >= 1 && value.length <= 64
    }

    static async correctCode (type, handle, code) {
        const response = await httpClient.post("/auth/verify-code", {
            type: type, 
            handle: handle, 
            code: code 
        })
        return response.data["status"] == "VALID_CODE"
    }
    
    static async userExists (handle, value) {
        const response = await httpClient.get("/auth/check-exists", {
            params : {
                handle: handle, 
                value: value 
            }
        })
        return response.data["status"] == "HANDLE_EXISTS"
    }

    static async isCorrectPassword(value) {
        const response = await httpClient.post("/auth/check-password", {
            password: value
        })
        return response.data["status"] == "PASSWORD_CORRECT"
    }
}