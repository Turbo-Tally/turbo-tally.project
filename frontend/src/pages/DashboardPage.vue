<script setup> 

import { ref, onMounted } from "vue"
import DefaultLayout from "../layouts/DefaultLayout.vue"
import ResultCard from "@/components/dashboard/ResultCard.vue"
import { httpClient } from "@/utils/http-client.js"
import { User } from "@/utils/user.js"
import { Helpers } from "@/utils/helpers.js"
import { useRouter } from "vue-router"

const router = useRouter()

/** 
 * Get User Polls 
 */
const pollsInput = ref({
    search: "", 
    cursor: -1 
})

const polls = ref([])

async function getUserPolls() {
    const user = (await User.data())["_id"]
    const response = await httpClient.get("/voting/polls/by-user", {
        params : {
            user : user, 
            cursor : pollsInput.value.cursor, 
            q : pollsInput.value.search  
        }
    })
    const data = response.data 
    pollsInput.value.cursor = data["meta"]["next_cursor"]
    return data["data"]
}

async function refetchPolls() {
    pollsInput.value.cursor = -1
    polls.value = await getUserPolls()
}

/** 
 * Get Answers  
 */
const answerInputs = ref({
    search : "", 
    cursor : -1
})

const answers = ref([])

async function getAnswers() {
    const user = (await User.data())["_id"]
    const response = await httpClient.get("/voting/answers/by-user", {
        params : {
            user : user, 
            cursor : answerInputs.value.cursor, 
            q : answerInputs.value.search  
        }
    })
    const data = response.data 
    answerInputs.value.cursor = data["meta"]["next_cursor"]
    return data["data"]
}

async function refetchAnswers() {
    answerInputs.value.cursor = -1
    answers.value = await getAnswers()
}

onMounted(async () => {
    polls.value = await getUserPolls()
    answers.value = await getAnswers()
    
    await Helpers.onContainerScrollBottom(
        document.getElementById("poll_results"), 
        async () => {
            polls.value = polls.value.concat(await getUserPolls())
        }
    )

    await Helpers.onContainerScrollBottom(
        document.getElementById("answer_results"), 
        async () => {
            const newAnswers = await getAnswers()
            answers.value = answers.value.concat(newAnswers)
        }
    )
})

/** 
 * Get Random Poll (Random Button)
 */

async function getRandomPoll() {
    const response = await httpClient.get("/voting/random-poll") 
    const data = response.data 
    const pollId = data["_id"] 
    router.push("/polls/" + pollId + "/answer")
}

</script> 

<template> 
    <div class="dashboard-page"> 
        <DefaultLayout>
            <div class="dashboard-content">
                <div class="main-panel"> 
                    <div class="your-activity section">
                        <div class="title"> 
                            Your Activity 
                        </div> 
                        <div class="content"> 
                            <div class="search-box" style="padding: 5px"> 
                                <input 
                                    type="text" 
                                    placeholder="Search..."
                                    v-model="answerInputs.search"
                                    @change="refetchAnswers()"
                                />
                            </div> 
                            <div 
                                class="answer-results" id="answer_results"  
                                style="margin-top: 16px"
                            > 
                               
                                <ResultCard 
                                    v-for="answer in answers"
                                    :key="answer['_id']"
                                    :answer="answer['answer']"  
                                    :poll="answer['poll']['title']"
                                    :timestamp="{
                                        'date' : 
                                            Helpers.daysAgoText(
                                                answer['answered_at']['$date']
                                            ), 
                                        'time' : 
                                            Helpers.timeText(
                                                answer['answered_at']['$date']
                                            )
                                    }"
                                /> 
                            </div>
                        </div>
                    </div> 
                </div> 
                <div class="side-panel"> 
                    <div class="join-a-random-poll section"> 
                        <div class="title"> 
                            Join a Random Poll
                        </div> 
                        <div class="content"> 
                            <button 
                                class="wide-btn randomize"
                                @click="getRandomPoll()"
                            >
                                Randomize
                            </button> 
                        </div>
                    </div> 
                    <div class="your-polls section"> 
                        <div class="title"> 
                            Your Polls 
                        </div> 
                        <div class="content"> 
                            <div class="search-box" style="padding: 0 5px;"> 
                                <input 
                                    type="text" 
                                    placeholder="Search..."
                                    v-model="pollsInput.search"
                                    @change="refetchPolls()"
                                />
                            </div> 
                            <div class="poll-results" id="poll_results"> 
                                <div 
                                    class="result-item"
                                    v-for="poll in polls"
                                    :key="poll['_id']"
                                    @click="$router.push('/poll/' + poll['_id'] + '/results')"
                                >   
                                    {{ poll["title"] }}
                                </div> 
                                <div 
                                    class="no-polls"
                                    v-if="polls.length == 0"
                                >   
                                    No Polls Found
                                </div> 
                            </div>
                        </div>
                    </div> 
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss">     
    .dashboard-content {
        display: flex;
        gap: 10px; 
        width: 900px;
        margin: 0 auto;
        margin-bottom: 50px;

        .main-panel {
            flex: 1;
        }

        .side-panel {
            width: 320px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .section {
            padding: 20px;
            box-shadow: 0px 0px 2px black;

            .title {
                font-size: 27px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        }
        
        .randomize:hover {
            opacity: 0.8; 
        }

        .randomize:active {
            opacity: 0.5;
        }
 
        ::-webkit-scrollbar {
            display: none;
        }

        .poll-results {
            margin-top: 16px;
            gap: 10px; 
            display: flex; 
            flex-direction: column;
            min-height: 50px;
            overflow-y: scroll;
            padding: 10px 5px;
            max-height: 188px;

            .result-item {
                background-color: rgb(234, 234, 234); 
                padding: 10px 20px;
                box-shadow: 0px 0px 2px black;
                cursor: pointer;
            }

            .result-item:hover {
                opacity: 0.8;
            }

            .result-item:active {
                opacity: 0.5;
            }
        }

        .answer-results {
            margin-top: 16px;
            gap: 10px; 
            display: flex; 
            flex-direction: column;
            min-height: 300px;
            overflow-y: scroll;
            padding: 10px 5px;
            max-height: 300px;
            

            .result-item {
                background-color: rgb(234, 234, 234); 
                padding: 10px 20px;
                box-shadow: 0px 0px 2px black;
                cursor: pointer;
            }

            .result-item:hover {
                opacity: 0.8;
            }

            .result-item:active {
                opacity: 0.5;
            }
        }


        .no-polls {
            text-align: center;
            padding: 20px;
            border: 1px solid grey;
            color: grey;
            border-radius: 5px;
        }
       
    }
</style>