<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import DatePicker from "../components/DatePicker.vue"
import { User } from "@/utils/user.js"
import { onMounted, ref } from "vue"
import { Form } from "@/utils/form.js"
import { Validators } from "@/utils/validators.js"
import { Helpers } from "@/utils/helpers.js"

import RegionPicker from "@/components/locations/RegionPicker.vue"
import ProvincePicker from "@/components/locations/ProvincePicker.vue"

const userData = ref(null) 

/** 
 * Personal Info
 */
const personalInfo = new Form() 
const personalInfoUpdated = ref({
    displayed: false
})

personalInfo.addField("region", async (value) => {
    return true 
})

personalInfo.addField("province", async (value) => {
    return true 
})

personalInfo.addField("gender", async (value) => {
    return true 
})

personalInfo.addField("birthdate", async (value) => {
    return true 
})

async function handleUpdatePersonalInfo() {
    const inputData = personalInfo.json() 

    inputData["birthdate"] = 
        Helpers.normalizeDate(Helpers.dateString(inputData["birthdate"]))


    const response = await httpClient.post(
        "/auth/update-info", inputData
    )
    
    const data = response.data

    if(data["status"] == "INFO_UPDATED") {
        personalInfoUpdated.value.displayed = true; 
        setTimeout(() => {
            personalInfoUpdated.value.displayed = false
        }, 3000)
    }
}

/** 
 * Change Email 
 */
const emailChange = new Form() 
const emailChangeUpdated = ref({
    displayed: false
})

emailChange.addField("email", async (value) => {
    return Validators.email(value)
})

emailChange.addField("emailCode", async (value) => {
    const validCode = Validators.verifCode(value) 
    const correctCode = await Validators.correctCode(
        "email-change", 
        emailChange.inputs.value.email, 
        value
    )
    console.log(validCode, correctCode)
    return validCode && correctCode
})

emailChange.requireAll(true)

async function requestEmailCode() {
    const response = 
        await httpClient.get("/auth/generate-verif-code", {
            params : {
                "type" : "email-change", 
                "handle" : emailChange.inputs.value.email
            }
        })
    const data = response.data
    emailChange.inputs.value.emailCode = data["code"]["value"]
}

async function handleUpdateEmailChange() {
    const response = await httpClient.post("/auth/change-email", {
        email: emailChange.inputs.value.email, 
        code: emailChange.inputs.value.emailCode 
    })
    const data = response.data 
    
    if(data["status"] == "EMAIL_CHANGED") {
        emailChangeUpdated.value.displayed = true
        emailChange.inputs.value.emailCode = null
        setInterval(() => {
            emailChangeUpdated.value.displayed = false
        }, 3000)
    }
}

/** 
 * Change Password
 */
const changePassword = new Form() 
const changePasswordUpdated = ref({
    displayed: false
})

changePassword.addField("currentPassword", async (value) => {
    return Validators.isCorrectPassword(value)
})

changePassword.addField("newPassword", async (value) => {
    return Validators.password(value)
})

changePassword.addField("confirmNewPassword", async (value) => {
    return value == changePassword.inputs.value.newPassword
})

changePassword.requireAll(true)

async function handleChangePassword() {
    const response = await httpClient.post("/auth/change-password", {
        current_password: changePassword.inputs.value.currentPassword, 
        new_password: changePassword.inputs.value.newPassword
    })
    const data = response.data 
    
    if(data["status"] == "PASSWORD_CHANGED") {
        changePasswordUpdated.value.displayed = true

        changePassword.inputs.value.currentPassword = null
        changePassword.inputs.value.newPassword = null
        changePassword.inputs.value.confirmNewPassword = null

        setInterval(() => {
            changePasswordUpdated.value.displayed = false
        }, 3000)
    }
}

/**
 * Mounted Hook
 */
onMounted(async () => {
    userData.value = await User.data();

    personalInfo.inputs.value.region = userData.value["info"]["region"]
    personalInfo.inputs.value.province = userData.value["info"]["province"]
    personalInfo.inputs.value.gender = userData.value["info"]["gender"]
    personalInfo.inputs.value.birthdate = userData.value["info"]["birthdate"]

    emailChange.inputs.value.email = userData.value["auth"]["email"]
})

</script> 

<template> 
    <div class="account-settings-page"> 
        <DefaultLayout>
            <div class="account-settings-content">
                <div class="personal-info section">
                    <div class="section-title"> 
                        <h1>Personal Info</h1>
                    </div> 
                    <div class="content" v-if="userData"> 
                        <div class="form-content" > 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Username</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <input 
                                        type="text"  
                                        style="text-align: left"
                                        disabled 
                                        :value="userData['auth']['username']"
                                    />
                                </div>
                            </div>
                        </div> 
                        <div class="form-content" > 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Region</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <RegionPicker 
                                        :initial="userData['info']['region']"
                                        @change="(regionKey) => {
                                            personalInfo.handle('region')
                                            personalInfo.inputs.value.region = regionKey
                                        }"
                                    />
                                </div>
                            </div>
                        </div> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Province</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <ProvincePicker 
                                        :region="userData['info']['region']"
                                        :initial="userData['info']['province']"
                                        @change="(provinceKey) => {
                                            personalInfo.handle('region')
                                            personalInfo.inputs.value.province = provinceKey
                                        }"
                                    />
                                </div>
                            </div>
                        </div> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Gender</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <select 
                                        class="gender wide-item"
                                        @change="form.handle('gender')"
                                        v-model="personalInfo.inputs.value.gender"
                                    >
                                        <option value="M">Male</option>
                                        <option value="F">Female</option>
                                    </select>
                                </div>
                            </div>
                        </div> 
                        <div class="form-content">
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Birthdate</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <DatePicker 
                                        :initial="userData['info']['birthdate']" 
                                    />
                                </div>
                            </div>
                        </div> 
                        <div class="controls" style="margin-top: 10px"> 
                            <button 
                                class="primary-btn"
                                @click="handleUpdatePersonalInfo()"
                            >
                                UPDATE 
                            </button>
                        </div> 
                    </div> 
                    <div class="loading" v-else>
                        Loading info...
                    </div> 
                    <div class="updated ok" v-if="personalInfoUpdated.displayed"> 
                        Update OK.
                    </div> 
                </div> 

                <div class="change-email-address section">
                    <div class="section-title"> 
                        <h1>Change E-mail Address</h1>
                    </div> 
                    <div class="content"> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="text"
                                    @change="emailChange.handle('email')"
                                    placeholder="E-mail Address"
                                    v-model="emailChange.inputs.value.email"
                                /> 
                            </div>
                            <div 
                                class="error-message" 
                                v-if="emailChange.hasError('email')"
                            > 
                                Invalid email address.    
                            </div> 
                        </div> 
                        <div class="email-code form-content">
                            <div class="form-item-flex">
                                <div 
                                    class="form-subitem email-verification-code"
                                >
                                    <input 
                                        type="number" 
                                        placeholder="E-mail Verification Code"
                                        @change="emailChange.handle('emailCode')"
                                        v-model="emailChange.inputs.value.emailCode"
                                    />
                                    <div 
                                        class="error-message" 
                                        v-if="emailChange.hasError('emailCode')"
                                    > 
                                        Invalid code.
                                    </div> 
                                </div>
                                <div class="form-subitem send-email-code">
                                    <button 
                                        class="primary-btn"
                                        @click="requestEmailCode()"
                                    >
                                        Send E-mail Code
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="controls" style="margin-top: 10px"> 
                            <button 
                                class="primary-btn"
                                :disabled="!emailChange.canSubmit()"
                                @click="handleUpdateEmailChange()"
                            >
                                UPDATE 
                            </button>
                        </div> 
                        <div class="updated ok" v-if="emailChangeUpdated.displayed"> 
                            Update OK.
                        </div> 
                    </div> 
                </div> 

                <div class="change-email-address section">
                    <div class="section-title"> 
                        <h1>Change Password</h1>
                    </div> 
                    <div class="content"> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="password"
                                    placeholder="Current Password"
                                    @change="changePassword.handle('currentPassword')"
                                    v-model="changePassword.inputs.value.currentPassword"
                                /> 
                            </div>
                            <div 
                                class="error-message"
                                v-if="changePassword.hasError('currentPassword')"
                            >
                                Wrong Password
                            </div> 
                        </div> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="password"
                                    placeholder="New Password"
                                    @change="changePassword.handle('newPassword')"
                                    v-model="changePassword.inputs.value.newPassword"
                                /> 
                            </div>
                            <div 
                                class="error-message"
                                v-if="changePassword.hasError('newPassword')"
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
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="password"
                                    placeholder="Confirm New Password"
                                    @change="changePassword.handle('confirmNewPassword')" 
                                    v-model="changePassword.inputs.value.confirmNewPassword"
                                /> 
                            </div>
                            <div 
                                class="error-message"
                                v-if="changePassword.hasError('confirmNewPassword')"
                                style="text-align: left"
                            >
                                Passwords do not match.
                            </div> 
                        </div> 
        
                        <div class="controls" style="margin-top: 10px"> 
                            <button 
                                class="primary-btn"
                                @click="handleChangePassword()"
                                :disabled="!changePassword.canSubmit()"
                            >
                                UPDATE 
                            </button>
                        </div> 

                        <div class="updated ok" v-if="changePasswordUpdated.displayed"> 
                            Update OK.
                        </div> 
                    </div> 
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .account-settings-page {
        .account-settings-content {
            width: 900px;
            margin: 0 auto; 
            display: flex;
            gap: 20px;
            flex-direction: column;
            margin-bottom: 100px;

            .form-content {
                padding: 1px;
            }

            .section-title {
                margin-bottom: 20px;
                
                h1 {
                    font-size: 24px;
                    text-align: center;
                    margin: 0px;
                    padding: 0px;
                }
            }

            .section {
                padding: 20px;
                box-shadow: 0px 0px 2px black;
            

                .form-item-flex { 
                    display: flex;
                    .title {
                        width: 100px;
                        justify-content: left;
                    }
                }
            }


            .email-code {

                .form-subitem.email-verification-code {
                    flex: 1;
                }

                .form-subitem.send-email-code {
                    width: 150px;
                }

            }  
        }

        .loading {
            text-align: center;
            padding: 30px;
            border: 1px solid grey;
            border-radius: 5px;
            color: grey;
            background-color: rgb(234, 234, 234);
        }

        .ok {
            margin-top: 10px;
            background-color: rgb(137, 255, 163);
            border: 1px solid black;
            border-radius: 5px;
            padding: 20px;
            display: flex; 
            justify-content: center;
            align-items: center
        }
    }
</style>