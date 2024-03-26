<script setup> 

import { computed, ref } from "vue"
import { Helpers } from "@/utils/helpers.js"

const props = defineProps([ "content" ])

const currentContent = computed(() => {
    return props.content
})

</script> 

<template> 
    <div class="event-reel-component"> 
        <div v-for="item in currentContent" :key="item.id">
            <div class="event-item">
                <div class="info">
                    <b>{{ item["user"]["info"]["username"] }}</b> 
                    voted 
                    <i><b>{{ item["answer"] }}</b></i> 
                    in 
                    <b>"{{ item["poll"]["title"] }}"</b>
                </div> 
                <div class="timestamp"> 
                    {{ Helpers.daysAgoText(item["answered_at"]["$date"]) }} 
                    @
                    {{ Helpers.timeText(item["answered_at"]["$date"]) }}

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