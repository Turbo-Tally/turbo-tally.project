<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import { httpClient } from "@/utils/http-client.js"
import { useRouter, useRoute } from "vue-router" 
import { onMounted, ref, watch } from "vue"
import { Poll } from "@/utils/poll.js"
import { User } from "@/utils/user.js"

const router = useRouter()
const route = useRoute()

const poll = ref({})
const choices = ref([])
const cursor = ref(-1) 
const query = ref("")

const user = ref({})
const hasAlreadyAnswered = ref(false)

/** 
 * Skip Polls
 */
async function skip() {
    const response = await httpClient.get("/voting/random-poll") 
    const data = response.data 
    const pollId = data["_id"] 
    router.push("/poll/" + pollId + "/answer")
}

async function fetchPoll() {
    poll.value =    
        await Poll.getInfo(route.params.pollId)
    const choicesResults =  
        await Poll.getChoices(
            route.params.pollId, 
            query.value.toUpperCase(), 
            -1
        )
    cursor.value = choicesResults["meta"]["next_cursor"]
    choices.value = choicesResults["data"]
}

async function selectAnswer(answer) {
    query.value = answer
}

async function submit() {
    const response = await Poll.answer(
        route.params.pollId, 
        query.value.toUpperCase()
    )
    if (response["status"] == "ANSWER_SUBMITTED") {
        router.push("/analyze/" + route.params.pollId)
    }
}

function canSubmit() {
    return query.value != ""
}

async function editQuery() {
    await fetchPoll()
}

watch(() => route.params.pollId, async () => {
    await fetchPoll()
})




onMounted(async () => {
    await fetchPoll()
    user.value = await User.data()

    if(await Poll.hasAnswered(route.params.pollId)) {
       hasAlreadyAnswered.value = true
    }
})


</script> 

<template> 
    <div class="answer-poll-page"> 
        <DefaultLayout>
            <div class="answer-poll-content" v-if="!hasAlreadyAnswered"> 
                <div class="title"> 
                    <h1>{{ poll["title"] }}</h1>
                </div>  
                <div class="answer-input" style="padding: 10px"> 
                    <input 
                        type="text" 
                        placeholder="Type an answer..." 
                        v-model="query"
                        style="text-transform: uppercase"
                        @keyup="editQuery"
                    />
                </div>
                <div class="choices"> 
                    <template v-if="choices.length > 0">
                        <div 
                            class="choice" 
                            v-for="choice in choices" 
                            :key="choice['_id']"
                            @click="selectAnswer(choice['answer'])"
                            :class="{ 'selected' : query == choice['answer'] }"
                        > 
                            <div 
                                class="label"
                            > 
                                {{ choice["answer"] }}
                            </div>
                        </div> 
                    </template> 
                    <div v-else class="new-answer"> 
                        <div class="text"> 
                            Click <b>Submit</b> for this new category of answer. 
                        </div>
                    </div> 
                </div>
                <div class="controls"> 
                    <div 
                        class="skip" 
                        style="text-align: left;"
                    > 
                        <div class="label"> 
                            <button 
                                class="primary-btn"
                                style="background-color: rgb(50, 50, 50);"
                                @click="skip()"
                            > 
                                SKIP
                            </button> 
                        </div>
                    </div> 
                    <div 
                        class="submit" 
                        style="text-align: right"
                    > 
                        <div class="label">
                            <button 
                                class="primary-btn" 
                                @click="submit()"
                                :disabled="!canSubmit()"
                            > 
                                SUBMIT
                            </button> 
                        </div>
                    </div>
                </div>
            </div> 

            <div class="already-answered" v-else> 
                <div class="inner">
                    Already answered... <br />
                    <a  
                        class="view-results" 
                        @click="$router.push('/analyze/' + $route.params.pollId)"
                    >
                        Click here to view results...
                    </a>
                </div>
            </div>  
        </DefaultLayout>
    </div> 
</template> 

<style lang="scss" scoped> 
    .answer-poll-page {
        padding-bottom: 100px;

        .answer-poll-content {
            width: 512px;
            box-shadow: 0px 0px 2px black;
            padding: 5px 20px;
            margin: 0 auto;
            padding-bottom: 30px;

            .title {
                margin-top: 20px;
                h1 {
                    margin: 0px; 
                    padding: 0px;
                }
            }

            .answer-input {
                margin-top: 15px;
            }

            ::--webkit-scrollbar {
                display: none;
            }

            .choices {
                padding: 10px;
                margin-top: 0px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px; 
                min-height: 250px; 
                max-height: 250px;
                overflow-y: scroll;

                .choice {
                    box-sizing: border-box;
                    width: 48%;
                    box-shadow: 0 0 0 1px black;
                    margin-bottom: 10px;
                    cursor: pointer;
                    user-select: none;

                    .label {
                        margin: 20px;
                    }
                 
                }
                
                .choice:hover {
                    background-color: rgb(200, 200, 200);
                    opacity: 0.8;
                }

                .choice:active {
                    opacity: 0.5;
                }

                .selected {
                    border: 2px solid green;
                    background-color: rgb(108, 255, 133)
                }
            }

            .controls {
                display: flex; 
                gap: 5px;
                margin-top: 20px;

                > div {
                    flex: 1;

                    button {
                        width: 80%;
                        height: 40px;
                    }
                }
            }
        }

        .already-answered {
            width: 528px; 
            height: 300px;
            background-color: rgb(234, 234, 234);
            margin: 0 auto;
            justify-content: center; 
            align-items: center;
            display: flex;
            border: 2px solid grey;
            text-align: center;

            a {
                text-decoration: underline;
                color: black;
            }
        }
        
        .view-results:hover {
            opacity: 0.8;
            cursor: pointer;
        }

        .new-answer {
            background-color: rgb(234, 234, 234);
            width: 100%;
            border-radius: 5px; 
            border: 2px solid grey;
            display: flex; 
            justify-content: center;
            align-items: center;
        }
    }
</style>