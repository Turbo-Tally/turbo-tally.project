<script setup> 

import { ref } from "vue"

const props = defineProps([ "labels", "data", "width", "height" ])

const options = ref({
    labels: props.labels,
    chart : {
        width: props.width, 
        height: props.height
    }
})

const series = ref(props.data)


</script> 

<template> 
    <div class="pie-chart"> 
        <apexchart
            type="pie"
            :options="options"
            :series="series"
        />  
    </div> 
</template> 

<style lang="scss" scoped> 
    .pie-chart {
        margin-top: 0px;
    }
</style> 