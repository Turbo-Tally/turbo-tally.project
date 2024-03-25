<script setup> 

import { ref } from "vue"
import DefaultLayout from "../layouts/DefaultLayout.vue"
import { httpClient } from "@/utils/http-client.js"
import { Form } from "@/utils/form.js"
import { Validators } from "@/utils/validators.js"

const statusMessage = ref({
    displayed : false, 
    message   : null 
})

const passwordMessage = ref({
    displayed : false, 
    temporaryPassword : null
})

const passwordSentMessage = ref(false)

const form = new Form() 

form.guardMode = "change"

form.addField("email", {
    validFormat : async (value) => {
        return Validators.email(value)
    }, 
    inexistent : async (value) => {
        return Validators.userExists("auth.email", value) 
    }
})

form.requireAll(true)

async function handleSendTemporaryPassword() {
    statusMessage.value.displayed = false
    passwordMessage.value.displayed = false

    const response = await httpClient.get("/auth/forgot-password", {
        params: {
            email : form.inputs.value.email
        }
    }) 

    const data = response.data 

    if (data["status"] == "TEMPORARY_PASSWORD_SENT") {
        if("temporary_password" in data) {
            passwordMessage.value.displayed = true
            passwordMessage.value.temporaryPassword = data["temporary_password"]
        } 
        passwordSentMessage.value = true
    } else {
        alert("Server Error")
    }
}

</script> 

<template> 
    <div class="forgot-password-page"> 
        <DefaultLayout>
            <div class="forgot-password-form">
                <div class="title"> 
                    <h1>Forgot Password?</h1>
                </div> 
                <div class="form">
                    <input 
                        class="email"
                        type="text"
                        placeholder="E-mail Address"
                        @change="form.handle('email')"
                        v-model="form.inputs.value.email"
                    /> 
                    <div 
                        class="error-message" 
                        v-if="form.hasError('email', 'validFormat')"
                    >
                        Invalid e-mail format. 
                    </div> 
                    <div 
                        class="error-message" 
                        v-if="form.hasError('email', 'inexistent')"
                    >
                        E-mail does not exist.
                    </div> 
                </div> 
                <div class="controls"> 
                    <button 
                        class="primary-btn"
                        @click="handleSendTemporaryPassword()"
                        :disabled="!form.canSubmit()"
                    >
                        Send Temporary Password
                    </button>
                </div> 
                <div
                    class="password-sent-message"
                    v-if="passwordSentMessage"
                > 
                    Temporary password sent to the specified email.
                </div>
                <div 
                    class="temporary-password"
                    v-if="passwordMessage.displayed"
                > 
                    <h3 style="margin: 0; padding: 0">
                        Dev-Only Message
                    </h3>
                    <br />  
                    Your temporary password is:
                    <br >
                    <b>{{ passwordMessage.temporaryPassword }}</b>
                </div>
              
            </div>
           
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .forgot-password-page {
        .forgot-password-form {
            width: 512px; 
            margin: 0 auto;

            .title {
                h1 {
                    font-size: 24px;
                }
            }

            .form {
                display: flex;
                flex-direction: column; 
                gap: 10px;
            }

            .controls {
                margin-top: 20px;
                display: flex;
                width: 100%;
                height: 32px;
            }

            .temporary-password {
                border: 1px dashed black; 
                background-color: rgb(234, 234, 234);
                padding: 20px;
                text-align: center;
                margin-top: 20px;
            }

            .password-sent-message {
                border: 1px solid green; 
                background-color: rgb(179, 204, 158);
                padding: 20px;
                text-align: center;
                margin-top: 20px;
                border-radius: 5px;
            }
        }
    }
</style>