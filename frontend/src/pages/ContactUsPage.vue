<script setup> 

import { Form } from "@/utils/form.js" 

const form = new Form()

form.addField("email",  (value) => {
    const re = new RegExp("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return re.test(value)
})

form.addField("subject", (value) => {
    return true
}) 

form.addField("message", (value) => {
    return true
})

form.requireAll(true)

function submit() {
    console.log(form.json())
}

</script> 

<template> 
    <div class="contact-us-page"> 
        <h1>Contact Us</h1>

        Allow Submission : {{ form.allowSubmission }} <br />
        Values : {{ form.values() }} <br />
        Errors : {{ form.errors() }} <br />
        Empty Fields : {{ form.containsEmptyFields() }}  <br /> 
        Errors : {{ form.hasErrors() }} <br />
        E-mail Invalid: {{ form.hasError('email') }} <br /> 
        Subject Invalid: {{ form.hasError('subject') }} <br /> 
        Message Invalid: {{ form.hasError('message') }} <br /> 

        <div class="contact-us-form">
            <table> 
                <tr>
                    <td>E-mail</td> 
                    <td>
                        <input 
                            type="text" 
                            @change="form.handle('email')"
                            v-model="form.inputs.value.email" 
                        />
                        <div class="error" v-if="form.hasError('email')"> 
                            Invalid e-mail.
                        </div> 
                    </td>
                </tr> 
                <tr>
                    <td>Subject</td> 
                    <td>
                        <input
                            type="text" 
                            @change="form.handle('subject')"
                            v-model="form.inputs.value.subject" 
                        />
                        <div class="error" v-if="form.hasError('subject')"> 
                            Invalid subject.
                        </div> 
                    </td>
                </tr> 
                <tr>
                    <td>Message</td> 
                    <td>
                        <textarea 
                            @change="form.handle('message')"
                            v-model="form.inputs.value.message" 
                        />
                        <div class="error" v-if="form.hasError('message')"> 
                            Invalid message.
                        </div> 
                    </td>
                </tr> 
            </table> 
            
            <button 
                class="submit" 
                :disabled="!form.canSubmit()" 
                @click="submit()"
            >
                Submit 
            </button> 
        </div> 
    </div>  
</template> 

<style lang="scss"> 
    .contact-us-page {
        width: 960px;
        margin: 0 auto;
    }   

</style>