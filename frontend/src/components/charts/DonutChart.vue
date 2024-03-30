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

function updateData(data) {
    series.value = data
}

function updateLabels(labels) {
    options.value.labels = labels
}

defineExpose({ updateData, updateLabels });

</script> 

<template> 
    <div class="donut-chart"> 
        <apexchart
            type="donut"
            :width="props.width"
            :height="props.height"
            :options="options"
            :series="series"
        />  
    </div> 
</template> 

<style lang="scss" scoped> 
    .donut-chart {
        margin-top: 0px;
    }
</style> 