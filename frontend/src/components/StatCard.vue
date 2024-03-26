<script setup> 

import { defineProps, computed, ref } from "vue" 

const props = defineProps([ "title", "value" ])


const normValue = computed(() => {
    const val = props.value

    if (val >= 1000000) {
        return (val / 1000000).toFixed(1) + "M"
    }
    else if (val >= 1000) {
        return (val / 1000).toFixed(1) + "K"
    }
    else {
        return val 
    }
    
})

</script> 

<template> 
    <div class="stat-card-component"> 
        <div class="title">
            {{ props.title }} 
        </div>
        <div class="value" :title="props.value">
            {{ normValue }}
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
            margin-top: -20px;
            font-size: 50px;
            font-weight: bold;
        }
    }
</style>