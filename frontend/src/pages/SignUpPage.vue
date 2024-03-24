<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import DatePicker from "../components/DatePicker.vue"

import { onMounted, ref, watch } from "vue"
import { httpClient } from "@/utils/http-client.js"

import { Form } from "@/utils/form.js"

/** 
 * Set-up Regions & Province Field
 */

const regionsList = ref()
const provincesList = ref()
const selectedRegionId = ref()

async function fetchRegionsList() {
    console.log("> Fetching regions list...")
    const regionsResponse = await httpClient.get("/common/regions") 
    const regionsData = regionsResponse.data
    regionsList.value = regionsData
    console.log("\t| Fetched regions list.")
}

async function fetchProvinceList(regionId) {
    console.log("> Fetching province list for " + regionId.value + "...")
    const endpoint =  "/common/region/" + regionId.value + "/provinces"
    const provincesResponse = await httpClient.get(endpoint) 
    const provincesData = provincesResponse.data 
    provincesList.value = provincesData 
    console.log("\t| Fetched provinces list.")
}

watch(selectedRegionId, async () => {
   inputs.value.region = selectedRegionId
   fetchProvinceList(selectedRegionId)
})

/**
 * Create Form
 */
const form = new Form({

})

console.log(form)

/**
 * On Mounted Hook 
 */
onMounted(async () => {
    await fetchRegionsList()
})

</script> 

<template> 
    <div class="sign-up-page"> 
        <DefaultLayout>
            <div class="sign-up-form">
                <div class="title"> 
                    <h1>Sign Up</h1>
                </div> 
                <div class="form">
                    <div class="form-item">
                        <input 
                            class="username"
                            type="text"
                            placeholder="Username"
                        /> 
                    </div> 
                    <div class="form-item">
                        <input 
                            class="email"
                            type="text"
                            placeholder="E-mail Address"
                        /> 
                    </div> 
                    <div class="form-item">
                        <input 
                            class="password"
                            type="password"
                            placeholder="Password"
                        />
                    </div> 
                    <div class="form-item">
                        <input 
                            class="confirm-password"
                            type="password"
                            placeholder="Confirm Password"
                        /> 
s                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Birthdate</b>
                        </div>
                        <div class="form-subitem datepicker">
                            <DatePicker 
                                class="birthdate"
                                :class="{ 'error' : errors.birthdate }"
                            />
                        </div>
                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Gender</b>
                        </div>
                        <div class="form-subitem datepicker">
                            <select
                                class="gender"
                                v-model="inputs.gender"
                                :class="{ 'error' : errors.gender }"
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
                        <div class="form-subitem datepicker">
                            <select 
                                class="region" 
                                v-model="selectedRegionId"
                            >    
                                <option 
                                    v-for="region in regionsList"
                                    :key="region['key']"
                                    :value="region['key']"
                                >
                                    {{ region.key}} - {{ region.long }}
                                </option> 
                            </select>
                        </div>
                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>Province</b>
                        </div>
                        <div class="form-subitem datepicker">
                            <select 
                                class="province"
                            >    
                                <option
                                    v-for="province in provincesList"
                                    :key="province['key']" 
                                    :value="province['key']"
                                >   
                                    {{ province["name"] }}
                                </option> 
                            </select>
                        </div>
                    </div> 
                    <div class="email-code form-item-flex">
                        <div class="form-subitem email-verification-code">
                            <input 
                                class="email-code"
                                type="number" 
                                placeholder="E-mail Code"
                                v-model="inputs.emailCode"
                            />
                        </div>
                        <div class="form-subitem send-email-code">
                            <button class="wide-btn">
                                Send E-mail Code
                            </button>
                        </div>
                    </div> 
                    <div class="form-item">
                        <input 
                            class="mobile-no"
                            type="text"
                            placeholder="Mobile Number"
                            v-model="inputs.mobileNo"
                        /> 
                    </div> 
                    <div class="sms-code form-item-flex">
                        <div class="form-subitem mobile-verification-code">
                            <input 
                                class="sms-code"
                                type="number" 
                                placeholder="SMS Code"
                                v-model="inputs.smsCode"
                            />
                        </div>
                        <div class="form-subitem send-sms-code">
                            <button class="wide-btn">
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
                                v-model="inputs.tac"
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
                                v-model="inputs.pp"
                            />
                        </div>
                    </div>
                </div> 
                <div class="controls">
                    <button 
                        class="wide-btn"
                        @click="handleSignUp()" 
                        :disabled="!allowSubmission"
                    >
                        Sign Up
                    </button>
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
        }

        

    }

</style>