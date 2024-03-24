<script setup> 

import { Form } from "@/utils/form.js" 

const form = new Form()

form.addField("email",  (value) => {
    return true
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

        Empty Fields : {{ form.containsEmptyFields() }}  <br /> 
        Errors : {{ form.hasErrors() }} <br />


        <div class="contact-us-form">
            <table> 
                <tr>
                    <td>E-mail</td> 
                    <td>
                        <input 
                            type="text" 
                            @change="form.handle('email')"
                            v-model="form.inputs.email.value" 
                        />
                    </td>
                </tr> 
                <tr>
                    <td>Subject</td> 
                    <td>
                        <input
                            type="text" 
                            @change="form.handle('subject')"
                            v-model="form.inputs.subject.value" 
                        />
                    </td>
                </tr> 
                <tr>
                    <td>Message</td> 
                    <td>
                        <textarea 
                            @change="form.handle('message')"
                            v-model="form.inputs.message.value" 
                        />
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