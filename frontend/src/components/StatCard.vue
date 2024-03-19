<script setup> 

import { defineProps } from "vue" 

const props = defineProps([ "title", "value" ])

</script> 

<template> 
    <div class="stat-card-component"> 
        <div class="title">
            {{ props.title }} 
        </div>
        <div class="value">
            {{ props.value }}
        </div>
    </div>
</template> 

<style scoped lang="scss"> 
    .stat-card-component {
        background-color: rgb(234, 234, 234);
        box-shadow: 0px 0px 2px black;
        
        .title {
            padding: 16px 0px;
            font-weight: bold;
            text-align: center;
        }

        .value {
            text-align: center;
            padding: 20px;
            font-size: 50px;
            font-weight: bold;
        }
    }
</style>