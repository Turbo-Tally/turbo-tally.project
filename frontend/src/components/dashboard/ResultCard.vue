<script setup> 

import { ref, defineProps } from "vue"

const props = defineProps([ "answer", "poll", "timestamp" ])


</script> 

<template> 
    <div class="result-card-component"> 
        <div class="message">
            <div class="text" style="width: 100%;">
                You voted <i><b>{{ props.answer }}</b></i> on <br />
                <b>{{ props.poll }}</b>
            </div>
        </div> 
        <div class="timestamp"> 
            <b>{{ props.timestamp.date }}</b> <br /> 
            {{ props.timestamp.time }}
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
            text-align: left;
        }


        .timestamp {
            background-color: rgb(234, 234, 234); 
            width: 100px;
            padding: 16px;
            text-align: right;
            border-left: 1px solid grey;
        }
    }
</style>