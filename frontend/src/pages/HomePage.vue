<script setup> 

import { nextTick, onMounted, onUnmounted, ref } from "vue"
import DefaultLayout from "../layouts/DefaultLayout.vue"

import StatCard from "@/components/StatCard.vue"
import EventReel from "@/components/EventReel.vue"

import { httpClient } from "@/utils/http-client.js" 
import { joinRoom, leaveRoom, wsClient } from "@/utils/ws-client.js"

const totalNoOfPolls = ref("-") 
const totalNoOfAnswerees = ref("-") 
const totalAverageAnswers = ref("-")

const recentAnswers = ref([])

async function fetchCount(type) {
    const response = await httpClient.get("/voting/counts/" + type);
    const data = response.data 
    return data
}

async function getRecentAnswers() {
    const response = await httpClient.get("/voting/recent-answers") 
    const data = response.data 
    return data
}


onMounted(async () => {
    totalNoOfPolls.value = await fetchCount("polls")
    totalNoOfAnswerees.value = await fetchCount("answerees")    
    totalAverageAnswers.value = await fetchCount("average-answers")   

    recentAnswers.value = await getRecentAnswers()

    joinRoom("recent-answers")
    wsClient.on("new-update", (data) => {
        recentAnswers.value = JSON.parse(data)
    })
})


onUnmounted(async () => {
    joinRoom("recent-answers")
})


</script> 

<template> 
    <div class="home-page"> 
        <DefaultLayout>
            <div class="general-stats"> 
                <div class="total-no-of-polls">
                    <StatCard 
                        title="Total No. of Polls" 
                        :value="totalNoOfPolls"
                    />
                </div> 
                <div class="total-no-of-answerees"> 
                    <StatCard 
                        title="Total No. of Answerees" 
                        :value="totalNoOfAnswerees"
                    />
                </div> 
                <div class="average-answerees-per-post"> 
                    <StatCard 
                        title="Average Answers per Post" 
                        :value="totalAverageAnswers"
                    />
                </div> 
            </div> 
            <div class="center-label">
                Join other people who vote in real time...
            </div>
            <div class="event-reel">
                <EventReel :content="recentAnswers" />
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style lang="scss"> 
    .home-page {
        padding-bottom: 100px;

        .general-stats {
            display: flex; 
            gap: 20px;

            > div {
                flex: 1;
            }
        }

        .center-label {
            margin-top: 20px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .event-reel {
            margin-top: 20px;
        }

    }

</style>