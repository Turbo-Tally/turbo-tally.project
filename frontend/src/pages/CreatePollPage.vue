<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import { Form } from "@/utils/form.js"
import { Validators } from "@/utils/validators.js"
import Choice from "@/components/Choice.vue"
import { httpClient } from "@/utils/http-client.js"
import { useRouter } from "vue-router"

const form = new Form() 

const choicesWithErrors = []

form.addField("title", (value) => {
    return Validators.pollTitle(value)
})

form.addField("choices", (value) => {
    for(let item in value) {
        const iterItem = value[item]
        if(!Validators.pollChoice(iterItem))
            return false
    }
    return true
})

form.inputs.value.choices = [ "" ]

form.requireAll(true)

const router = useRouter()

function editChoice(index, value) {
    form.inputs.value.choices[index] = value
    form.handle('choices')
}

function handleClearAll() {
    form.inputs.value.choices = [ "" ]
    form.handle('choices')
}

function handleAddChoice() {
    form.inputs.value.choices.push("")
    form.handle('choices')
}

async function handleSubmit() {
    const inputs = form.json() 
    const response = await httpClient.post("/voting/polls/create", inputs) 
    const data = response.data 
    const pollId = data["poll_id"]
    if(data["status"] == "POLL_CREATED") {
        router.push("/poll/" + pollId + '/results') 
    }
}

window.addEventListener("keydown", (e) => {
    if(e.key == "Enter") {
        handleAddChoice();
    }
})

</script> 

<template> 
    <div class="create-poll-page"> 
        <DefaultLayout>
            <div class="create-poll-content"> 
                <div class="title"> 
                    <h1>Create Poll</h1>
                </div> 
                <div class="title-input"> 
                    <input 
                        type="text" 
                        placeholder="Enter Question Title..." 
                        @change="form.handle('title')"
                        v-model="form.inputs.value.title"
                    />
                    <div class="error-message" v-if="form.hasError('title')"> 
                        Title must be between 5 and 256 characters.
                    </div> 
                </div> 
                <div class="choices">
                    <div class="choices-header">
                        <div class="title"> 
                            CHOICES 
                        </div>  
                        <div class="controls"> 
                            <button 
                                class="primary-btn"
                                @click="handleClearAll()"
                            > 
                                CLEAR ALL 
                            </button> 
                            <button 
                                class="primary-btn"
                                @click="handleAddChoice()"
                            >

                                + ADD CHOICE 
                            </button> 
                        </div>
                    </div> 
                    <div class="choice-results">    
                        <div
                            v-for="(choice, index) in form.inputs.value.choices"
                            :key="choice"
                            class="choice"
                        > 
                            <div class="name">
                                <Choice 
                                    :value="choice" 
                                    @change="(value) => editChoice(index, value)" 
                                />
                            </div> 
                            <div 
                                class="trash"
                                @click="form.inputs.value.choices.splice(index, 1)"
                            > 
                                🗑️ 
                            </div> 
                        </div> 
                    </div>
                    <div class="choice-submit"> 
                        <button 
                            class="primary-btn"
                            :disabled="!form.canSubmit()"
                            @click="handleSubmit()"
                        > 
                            SUBMIT
                        </button> 
                    </div> 
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .create-poll-page {
        .create-poll-content {
            width: 900px;
            box-shadow: 0px 0px 2px black;
            margin: 0 auto;
            padding: 5px 20px;
            padding-bottom: 50px;

            .choices {
                margin-top: 20px;

                .choices-header {
                    display: flex;

                    .title {
                        flex: 1;
                        font-weight: bold;
                        display: flex; 
                        justify-content: left;
                        align-items: center;
                    }

                    .controls {
                        flex: 1; 
                        display: flex;
                        gap: 10px;
                        justify-content: right;


                        button {
                            width: 100px;
                        }
                    }

                }

                .choice-results {
                    margin-top: 15px;
                    display: flex;
                    gap: 10px;
                    flex-direction: column;

                    .choice {
                        display: flex;
                        padding: 10px;
                        box-shadow: 0px 0px 2px black;

                        .name {
                            font-weight: bold;
                            flex: 1;
                        }

                        .trash {
                            cursor: pointer;
                            outline: none; 
                        }

                        .trash:hover {
                            opacity: 0.8;
                        }

                        .trash:active {
                            opacity: 0.5;
                        }
                    }
                }

                .choice-submit {
                    margin-top: 20px;
                }
            }
        }
    }
</style>