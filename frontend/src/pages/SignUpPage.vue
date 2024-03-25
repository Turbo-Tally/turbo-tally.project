<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import DatePicker from "../components/DatePicker.vue"

import { onMounted, ref, watch } from "vue"
import { httpClient } from "@/utils/http-client.js"

import { Form } from "@/utils/form.js"
import { Validators } from "@/utils/validators.js"
import { Helpers }  from "@/utils/helpers.js"
import { Locations } from "@/utils/locations.js"

import RegionPicker from "@/components/locations/RegionPicker.vue"
import ProvincePicker from "@/components/locations/ProvincePicker.vue"

/**
 * Set-up Sub-Page 
 */
const subPage = ref("form")         // form or success message

/**
 * Create Form
 */
const form = new Form()

form.addField("username", {
    validFormat : async (value) => {
        return Validators.username(value) 
    }, 
    existsAlready : async (value) => {
        return !(await Validators.userExists("auth.username", value))
    }
})

form.addField("email",  {
    validFormat : async (value) => {
        return Validators.email(value)
    },
    existsAlready : async (value) => {
        return !(await Validators.userExists("auth.email", value))
    }
})

form.addField("password", async (value) => {
    return Validators.password(value)
})

form.addField("confirmPassword", async (value) => {
    return value == form.inputs.value.password
})

form.addField("birthdate", async (value) => {
    return Validators.birthdate(value)
})

form.addField("gender", async (value) => {
    return Validators.gender(value)
})

form.addField("region", async (value) => {
    return true
})

form.addField("province", async (value) => {
    return true 
})

form.addField("emailCode", async (value) => {
    const validCode = Validators.verifCode(value) 
    const correctCode = await Validators.correctCode(
        "email-verif", 
        form.inputs.value.email, 
        value
    )
    return validCode && correctCode
})

form.addField("mobileNo", {
    validFormat : async (value) => {
        const validCode = Validators.mobileNo(value) 
        return true 
    },
    existsAlready : async (value) => {
        return !(await Validators.userExists("info.mobile_no", value))
    }
})

form.addField("smsCode", async (value) => {
    const validCode = Validators.verifCode(value) 
    const correctCode = await Validators.correctCode(
        "mobile-verif", 
        form.inputs.value.mobileNo, 
        value
    )
    return validCode && correctCode
})

form.addField("termsAndConditions", async (value) => {
    return true 
})

form.addField("privacyPolicy", async (value) => {
    return true
})

form.requireAll(true)

form.isSubmitting = ref(false)


/**
 * Set-up Default Values
 */
form.inputs.value.username = "johndoe"
form.inputs.value.email = "johndoe@example.com" 
form.inputs.value.password = "@JohnDoe1234();" 
form.inputs.value.confirmPassword = "@JohnDoe1234();" 
form.inputs.value.birthdate = "1990-01-01"
form.inputs.value.gender = "M"
form.inputs.value.region = "V"
form.inputs.value.province = "CAS"
// form.inputs.value.emailCode = "289899" 
form.inputs.value.mobileNo = "09123456789"
// form.inputs.value.smsCode = "324789"
form.inputs.value.termsAndConditions = true 
form.inputs.value.privacyPolicy = true


/** 
 * Handle Sign Up Action 
 */
async function handleSignUp() {
    // disable submission 
    form.disableSubmission() 
    form.isSubmitting.value = true 

    // fix data
    const data = form.json()
    data["birthdate"] = Helpers.normalizeDate(data["birthdate"])
    
    // send sign-up request
    const signUpResponse = await httpClient.post("/auth/sign-up", data)
    const signUpStatus = signUpResponse.data["status"]
    
    if(signUpStatus == "REGISTERED") {
        // reenable form 
        subPage.value = "sign-up-success"
        form.enableSubmission() 
    } else {
        alert("Server Error")
    }
}

/** 
 * Request E-mail Code 
 */
async function requestEmailCode() {
    const response = 
        await httpClient.get("/auth/generate-verif-code", {
            params : {
                "type" : "email-verif", 
                "handle" : form.inputs.value.email
            }
        })
    const data = response.data
    form.inputs.value.emailCode = data["code"]["value"]
}

/** 
 * Request SMS Code 
 */
async function requestSMSCode() {
    const response = 
        await httpClient.get("/auth/generate-verif-code", {
            params : {
                "type" : "mobile-verif", 
                "handle" : form.inputs.value.mobileNo
            }
        })
    const data = response.data
    form.inputs.value.smsCode = data["code"]["value"]
}


/**
 * On Mounted Hook 
 */
onMounted(async () => {
})

</script> 

<template> 
    <div class="sign-up-page"> 
        <DefaultLayout>
            <div 
                v-if="subPage == 'form'" 
                class="sign-up-form"
            >
                <div class="title"> 
                    <h1>Sign Up</h1>
                </div> 
                <div class="form">
                    <!-- {{ form.errors() }}
                    {{ form.values() }} <br /> <br />
                    {{ form.errors() }} <br /><br /> 
                    Has Errors : {{ form.hasErrors() }} <br /> <br /> 
                    Empty Fields: {{ form.containsEmptyFields() }} <br /><br /> -->
                    <div class="form-item">
                        <input 
                            class="username"
                            type="text"
                            placeholder="Username"
                            @change="form.handle('username')"
                            v-model="form.inputs.value.username"
                        />  
                        <div 
                            class="error-message" 
                            v-if="form.hasError('username', 'existsAlready')"
                        >   
                            User already exists.
                        </div> 
                        <div 
                            class="error-message" 
                            v-else-if="form.hasError('username', 'validFormat')"
                        >   
                            Username must be composed of only letters, numbers, 
                            dots, and underscores.
                        </div>
                    </div> 
                    <div class="form-item">
                        <input 
                            class="email"
                            type="text"
                            placeholder="E-mail Address"
                            @change="form.handle('email')"
                            v-model="form.inputs.value.email"
                        /> 
                        <div 
                            class="error-message" 
                            v-if="form.hasError('email', 'existsAlready')"
                        >   
                            E-mail already exists.
                        </div> 
                        <div 
                            class="error-message" 
                            v-else-if="form.hasError('email', 'validFormat')"
                        >   
                            Must be a valid e-mail address in the format: 
                            <i>user@example.com</i> 
                        </div> 
                    </div> 
                    <div class="form-item">
                        <input 
                            class="password"
                            type="password"
                            placeholder="Password"
                            @change="form.handle('password')"
                            v-model="form.inputs.value.password"
                        />
                        <div 
                            class="error-message" 
                            v-if="form.hasError('password')"
                            style="text-align: left"
                        >   
                            Password must be composed of at least:
                            <ul> 
                                <li>8 to 255 characters</li>
                                <li>1 big letter</li> 
                                <li>1 small letter</li> 
                                <li>1 number</li> 
                                <li>1 symbol e.g. (, ), \, etc. </li>
                            </ul> 
                        </div> 
                    </div> 
                    <div class="form-item">
                        <input 
                            class="confirm-password"
                            type="password"
                            placeholder="Confirm Password"
                            @change="form.handle('confirmPassword')"
                            v-model="form.inputs.value.confirmPassword"
                        /> 
                        <div 
                            class="error-message" 
                            v-if="form.hasError('confirmPassword')"
                        >   
                            Passwords do not match.
                        </div> 
                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Birthdate</b>
                        </div>
                        <div class="form-subitem picker">
                            <DatePicker 
                                class="birthdate"
                                :initial="form.inputs.value.birthdate"
                                @change="(value) => {
                                    form.handle('birthdate')
                                    form.inputs.value.birthdate = value
                                }"
                            />
                            <div 
                                class="error-message" 
                                v-if="form.hasError('birthdate')"
                            >   
                                Must be at least 18 years old to sign up.
                            </div> 
                        </div>
                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Gender</b>
                        </div>
                        <div class="form-subitem picker">
                            <select
                                class="gender"
                                v-model="form.inputs.value.gender"
                                @change="form.handle('gender')"
                            >    
                                <option value="M">Male</option> 
                                <option value="F">Female</option>
                            </select>  
                        </div>
                    </div>
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Region</b>
                        </div>
                        <div class="form-subitem picker">
                            <RegionPicker
                                :initial="form.inputs.value.region"
                                @change="(regionKey) => {
                                    form.handle('region')
                                    form.inputs.value.region = regionKey
                                }"
                            /> 
                        </div>
                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Province</b>
                        </div>
                        <div class="form-subitem picker">
                            <ProvincePicker 
                                :initial="form.inputs.value.province"
                                :region="form.inputs.value.region"
                                @change="(provinceKey) => {
                                    form.handle('province') 
                                    form.inputs.value.province = provinceKey
                                }"
                            />
                        </div>
                    </div> 
                    <div class="email-code form-item-flex">
                        <div class="form-subitem email-verification-code">
                            <input 
                                class="email-code"
                                type="text" 
                                placeholder="E-mail Code"
                                @change="form.handle('emailCode')"
                                v-model="form.inputs.value.emailCode"
                            />
                            <div 
                                class="error-message" 
                                v-if="form.hasError('emailCode')"
                            >   
                                Invalid code.
                            </div> 
                        </div>
                        <div class="form-subitem send-email-code">
                            <button 
                                class="wide-btn"
                                @click="requestEmailCode()"
                            >
                                Send E-mail Code
                            </button>
                        </div>
                    </div> 
                    <div class="form-item">
                        <input 
                            class="mobile-no"
                            type="text"
                            placeholder="Mobile Number"
                            @change="form.handle('mobileNo')"
                            v-model="form.inputs.value.mobileNo"
                        /> 
                        <div 
                            class="error-message" 
                            v-if="form.hasError('mobileNo', 'existsAlready')"
                        >   
                            Phone used by another person already.
                        </div> 
                        <div 
                            class="error-message" 
                            v-else-if="form.hasError('mobileNo', 'validFormat')"
                        >   
                            Must be a valid Philippine phone number: 
                            e.g. <b>09123456789</b>
                        </div> 
                    </div> 
                    <div class="sms-code form-item-flex">
                        <div class="form-subitem mobile-verification-code">
                            <input 
                                class="sms-code"
                                type="text" 
                                placeholder="SMS Code"
                                @change="form.handle('smsCode')"
                                v-model="form.inputs.value.smsCode"
                            />
                            <div 
                                class="error-message" 
                                v-if="form.hasError('smsCode')"
                            >   
                                Invalid code.
                            </div> 
                        </div>
                        <div class="form-subitem send-sms-code">
                            <button 
                                class="wide-btn"
                                @click="requestSMSCode()"
                            >
                                Send SMS Code
                            </button>
                        </div>
                    </div>
                    <div class="terms-and-conditions form-item-flex">
                        <div class="form-subitem message">
                            I agree to the&nbsp;<b>Terms and Conditions</b>
                        </div>  
                        <div class="form-subitem checkbox">
                            <input 
                                type="checkbox" 
                                v-model="form.inputs.value.termsAndConditions"
                            />
                        </div>
                    </div>
                    <div class="privacy-policy form-item-flex">
                        <div class="form-subitem message">
                            I agree to the&nbsp;<b>Privacy Policy</b>.
                        </div>  
                        <div class="form-subitem checkbox">
                            <input 
                                type="checkbox" 
                                v-model="form.inputs.value.privacyPolicy"
                            />
                        </div>
                    </div>
                </div> 
                <div class="controls">
                    <button 
                        class="wide-btn"
                        @click="handleSignUp()" 
                        :disabled="!form.canSubmit()"
                    >
                        {{ 
                            form.isSubmitting.value ? 
                                "Submitting..." : "Submit"
                        }}
                    </button>
                </div> 
            </div>
            <div 
                v-else-if="subPage == 'sign-up-success'" 
                class="sign-up-success"
            >
                <div class="text">
                    <b>You have successfully signed up</b>
                    <br /> 
                    You may now <router-link to="/log-in">log in</router-link>
                </div>
            </div> 
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .sign-up-page {

        /** Base Styles */
        .sign-up-form {
            margin-bottom: 100px;
            margin-left: auto; 
            margin-right: auto; 
            
            width: 512px; 

            .title {
                margin: 0px; 
                padding: 0px;
                font-weight: bold;
                font-size: 14px;
            }

            .form {
                display: flex; 
                flex-direction: column;
                gap: 10px;

                .birthdate.form-item-flex {
                    
                    .form-subitem.label {
                        width: 128px;
                        display: flex;
                        align-items: center;
                    }

                    .form-subitem.datepicker {
                        flex: 1;
                        input {
                            width: 100%;
                        }
                    }

                }

                .email-code.form-item-flex {

                    .form-subitem.email-verification-code {

                    }

                    .form-subitem.send-email-code {
                        flex: 1;
                    }

                }   

                .sms-code.form-item-flex {

                    .form-subitem.mobile-verification-code {

                    }

                    .form-subitem.send-sms-code {
                        flex: 1;
                    }

                }   

                .terms-and-conditions.form-item-flex {
                    .message {
                        display: flex; 
                        align-items: center;
                        flex : 1;
                    }

                    .checkbox {
                        margin-right: 5px;
                    }
                }

                .privacy-policy.form-item-flex {
                    .message {
                        display: flex; 
                        align-items: center;
                        flex : 1;
                    }

                    .checkbox {
                        margin-right: 5px;
                        border: none;
                    }
                }
            }


            .controls {
                margin-top: 20px;
                display: flex;
                width: 100%;
            }

            .picker {
                flex: 1;
            }
        }

        .sign-up-success {
            background-color: rgb(196, 227, 228);
            color: black;
            border: 1px solid rgb(50, 50, 50);
            padding: 20px; 
            display: flex; 
            justify-content: center;
            align-items: center;
            text-align: center;
            width: 512px;
            margin: 0 auto;
        }    

        a {
            color: black
        }
    }

</style>