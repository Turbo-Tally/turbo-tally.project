<script setup> 

import { ref } from "vue"

const eventReelItems = ref([
    { 
        "answer_id" : 1,
        "vote_info" : {
            "username" : "User1234", 
            "choice": "Asul",
        },  
        "poll" : {
            "id" : 1,
            "title" : "What's your favorite color?"
        }, 
        "answered_at" : "Today @ 7:05PM"
    },
    { 
        "answer_id" : 2,
        "vote_info" : {
            "username" : "User1123", 
            "choice": "Berde",
        },  
        "poll" : {
            "id" : 2,
            "title" : "What's your favorite color?"
        }, 
        "answered_at" : "Today @ 7:04PM"
    },
    { 
        "answer_id" : 3,
        "vote_info" : {
            "username" : "User4321", 
            "choice": "Pula",
        },  
        "poll" : {
            "id" : 2,
            "title" : "What's your favorite color?"
        }, 
        "answered_at" : "Today @ 7:03PM"
    }
])

</script> 

<template> 
    <div class="event-reel-component"> 
        <div v-for="item in eventReelItems" :key="item.id">
            <div class="event-item">
                <div class="info">
                    <b>{{ item.vote_info.username }}</b> 
                    voted 
                    <i><b>{{ item.vote_info.choice }}</b></i> 
                    in 
                    <b>"{{ item.poll.title }}"</b>
                </div> 
                <div class="timestamp"> 
                    {{ item.answered_at }}
                </div> 
            </div>
        </div>
    </div>
</template> 

<style scoped lang="scss"> 
    .event-reel-component {
        display: flex; 
        gap: 10px;
        flex-direction: column;

        .event-item {
            background-color: rgb(234, 234, 234);
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: 0px 0px 2px black;
            display: flex; 

            .info {
                flex: 1;
            }

            .timestamp {
                font-weight: bold;
            }
        }
    }
</style>