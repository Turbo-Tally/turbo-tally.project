<script setup> 

import { ref, defineProps } from "vue"

const props = defineProps([ "poll", "author", "timestamp", "votes" ])

</script> 

<template> 
    <div class="result-card-component"> 
        <div class="message">
            <div class="poll">
                {{ props.poll }}
            </div>
            <div class="author">
                {{ props.author }}
            </div>
        </div> 
        <div class="info"> 
            <div class="timestamp">
                {{ props.timestamp }}
            </div>
            <div class="votes">
                <i>{{ props.votes }}</i> votes
            </div>
        </div>
    </div>
</template> 

<style scoped lang="scss"> 
    .result-card-component {
        box-shadow: 0px 0px 2px black;
        display: flex; 

        .message {
            flex: 1;
            padding: 16px;
            display: flex; 
            flex-direction: column;
            gap: 10px;

            .poll {
                font-weight: bold;
            }
        }


        .info {
            background-color: rgb(234, 234, 234); 
            width: 180px;
            padding: 16px;
            border-left: 1px solid grey;
            display: flex;
            justify-content: center;
            text-align: right;
            flex-direction: column;

            .timestamp {
                font-weight: bold;
            }

            .votes {

            }
        }
    }
</style>