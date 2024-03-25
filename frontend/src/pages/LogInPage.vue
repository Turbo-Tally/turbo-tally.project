<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import { ref } from "vue"
import { Form } from "@/utils/form.js" 
import { Validators } from "@/utils/validators.js" 
import { httpClient } from "@/utils/http-client.js"
import { useMainStore } from "@/stores/main.store.js" 
import { useRouter } from "vue-router"

const mainStore = useMainStore() 
const router = useRouter()

/**
 * Create Error Message
 */
const errorMessage = ref({
    displayed: false, 
    status: null
})

/**
 * Create Form
 */
const form = new Form() 

form.addField("email", async () => {
    return true 
})

form.addField("password", async () => {
    return true
})

/**
 * Handle Log In
 */
async function handleLogIn() {
    const response = await httpClient.post("/auth/log-in", {
        email: form.inputs.value.email, 
        password: form.inputs.value.password
    })

    const data = response.data 

    if(data["status"] != "LOGGED_IN") {
        errorMessage.value.displayed = true
        errorMessage.value.status = data["status"]
    } else {
        mainStore.logIn()
        router.push("dashboard")
    }
}

</script> 

<template> 
    <div class="log-in-page"> 
        <DefaultLayout>
            <div class="log-in-form">
                <div class="title"> 
                    <h1>Log In</h1>
                </div> 
                <div class="form">
                    <input 
                        class="email"
                        type="text"
                        placeholder="E-mail Address"
                        v-model="form.inputs.value.email"
                        @change="form.handle('email')"
                    /> 
                    <input 
                        class="password" 
                        type="password"
                        placeholder="Password"
                        v-model="form.inputs.value.password"
                        @change="form.handle('password')"
                    /> 
                    <div 
                        class="error-message" 
                        v-if="errorMessage.status == 'EMAIL_DOES_NOT_EXIST'"
                    >
                        E-mail does not exist.
                    </div> 
                    <div 
                        class="error-message" 
                        v-if="errorMessage.status == 'INVALID_PASSWORD'"
                    >
                        Wrong password for email.
                    </div> 
                </div> 
                <div class="controls"> 
                    <div class="forgot-password-link"> 
                        <a href="/#/forgot-password">Forgot Password?</a>
                    </div> 
                    <div class="log-in-button">
                        <button
                            class="primary-btn"
                            @click="handleLogIn()"
                        >
                            Log In
                        </button>
                    </div>
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .log-in-page {
        .log-in-form {
            width: 512px; 
            margin: 0 auto;

            .title {
                h1 {
                    font-size: 28px;
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

                .forgot-password-link {
                    flex: 1;
                 
                    a {
                        color: black;
                        text-decoration: underline; 
                    }
                }

                .log-in-button {
                    width: 100px;

                  
                }

            }
        }
    }
</style>