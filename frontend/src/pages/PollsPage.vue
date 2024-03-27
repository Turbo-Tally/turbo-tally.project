<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"
import ResultCard from "@/components/polls/ResultCard.vue"
import { ref, watch, onMounted } from "vue"

import { Helpers } from "@/utils/helpers.js"
import { useMainStore } from "@/stores/main.store.js" 
import { Poll } from "@/utils/poll.js"
import { useRouter } from "vue-router"
 
const router = useRouter()
const mainStore = useMainStore();
const fetched = ref(false)

const inputs = ref({
    q : "", 
    sort : "recent", 
    filter : "all",
    cursor: -1
})

const hasReachedEnd = ref(false)

const polls = ref(null)

function resetCursor() {
    inputs.value.cursor = -1
}

async function fetchInputs() {
    fetched.value = false

    const response = await httpClient.get("/voting/polls/browse", {
        params: inputs.value
    })
    const data = response.data 
    
    inputs.value.cursor = data["meta"]["next_cursor"]

    if (!("next_cursor" in data["meta"])) {
        hasReachedEnd.value = true
    }
    
    fetched.value = true 

    return data["data"]
}

function timestamp(dt) { 
    const daysAgoText = Helpers.daysAgoText(dt)
    const timeText = Helpers.timeText(dt) 
    return daysAgoText + ", " + timeText 
}

onMounted(async () => {
    polls.value = await fetchInputs()

    Helpers.onScrollBottom(async () => {
        if(!hasReachedEnd.value) {
            if(polls.value != null) {
                for(let input of await fetchInputs()) {
                    polls.value.push(input)
                }
            }
        }
    })
})

async function newFetch() {
    console.log("@ Fetching...")
    hasReachedEnd.value = false
    resetCursor() 
    polls.value = await fetchInputs()
}

async function handleClickResultCard(poll) {
    const pollId = poll["_id"]
    
    if(await Poll.hasAnswered(pollId)) {
        router.push("/poll/" + pollId + "/results")
    } else {
        router.push("/poll/" + pollId + "/answer")
    }
}



</script> 

<template> 
    <div class="polls-page"> 
        <DefaultLayout>
            <div class="polls-content" v-if="polls"> 
                <div class="search"> 
                    <input 
                        type="text" 
                        placeholder="Search..."
                        v-model="inputs.q"
                        @change="newFetch()"
                    />
                </div> 
                <div class="controls"> 
                    <div class="create-new-poll"> 
                        <button 
                            class="primary-btn"
                            @click="$router.push('/poll/create')"
                        >

                            + Create New Poll
                        </button> 
                    </div> 
                    <div class="sort-poll" > 
                        <div style="flex: 1" />
                        <div class="sort">
                            <select
                                v-model="inputs.sort"
                                @change="newFetch()"
                            >
                                <option value="recent">Recent</option>
                                <option value="oldest">Oldest</option>
                            </select> 
                        </div>
                        <div class="filter" v-if="mainStore.isLoggedIn">
                            <ul>
                                <li 
                                    @click="async () => {
                                        inputs.filter = 'all'
                                        await newFetch()
                                    }"
                                    :class="{ 'active' : inputs.filter == 'all' }"
                                >
                                    All
                                </li>
                                <li 
                                    @click="async () => {
                                        inputs.filter = 'unanswered'
                                        await newFetch()
                                    }"
                                    :class="{ 'active' : inputs.filter == 'unanswered' }"
                                >
                                    Unanswered
                                </li>
                                <li
                                    @click="async () => {
                                        inputs.filter = 'answered'
                                        await newFetch()
                                    }"
                                    :class="{ 'active' : inputs.filter == 'answered' }"
                                >
                                    Answered
                                </li>
                            </ul> 
                        </div>
                    </div>  
                </div> 
                <div class="results" v-if="polls.length > 0">
                    <ResultCard 
                        v-for="poll in polls"
                        @click="handleClickResultCard(poll)"
                        :key="poll['id']"
                        :poll="poll['title']" 
                        :author="poll['user']['info']['username']" 
                        :timestamp="timestamp(poll['created_at']['$date'])"
                        :votes="poll['meta']['no_of_answers']"
                    />
                </div>
                <div class="no-results-found" v-else-if="polls.length == 0"> 
                    No Results Found
                </div>     
            </div> 
         
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .polls-page {
        padding-bottom: 50px; 

        .polls-content {
            width: 900px;
            margin: 0 auto;

            .search {
                input {
                    font-size: 20px;
                }
            }

            .controls {
                margin-top: 14px;
                display: flex;

                .sort-poll {
                    flex: 1;
                    display: flex; 
                    justify-content: right;

                    .filter {
                        margin-left: 10px; 
                        padding-left: 10px; 
                        border-left: 2px solid black;
                        display: flex; 
                        align-items: center;
                        justify-content: center;
                       
                        ul {
                            padding: 0px; 
                            margin: 0px;
                        }

                        ul li {
                            display: inline;
                            margin: 0 10px;
                            cursor: pointer;
                        }

                        ul li:hover {
                            opacity: 0.8;
                        }

                        li.active {
                            font-weight: bold;
                        }
                    }
                }
            }

            .results {
                margin-top: 20px;
                display: flex;
                flex-direction: column;
                gap: 16px;

                .result-card-component:hover {
                    opacity: 0.8;
                    cursor: pointer;
                }

                .result-card-component:active {
                    opacity: 0.5;
                    cursor: pointer;
                }
            }
        }

        .no-results-found {
            width: 900px; 
            height: 300px; 
            border: 2px solid black; 
            background-color: rgb(234, 234, 234); 
            color: grey;
            margin-top: 20px; 
            border-radius: 5px; 
            display: flex; 
            align-items: center;
            justify-content: center;
        }
    }
</style>