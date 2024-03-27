<script setup> 
import { ref } from "vue"

const props = defineProps([ "labels", "data", "width", "height" ])

const options = ref({
    plotOptions: {
        bar: {
            borderRadius: 4,
            horizontal: true
        }
    },
    xaxis: {
        categories: props.labels
    }
})

const series = ref([{ data: props.data }])

</script> 

<template> 
    <div class="horizontal-bar-chart"> 
        <apexchart
            type="bar"
            :width="props.width"
            :height="props.height"
            :options="options"
            :series="series"
        />  
    </div> 
</template> 

<style lang="scss" scoped> 
    .horizontal-bar-chart {
        margin-top: 10px;
        margin-left: -15px;
    }
</style> 