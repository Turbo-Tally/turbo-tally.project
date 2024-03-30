<script setup> 
import { ref, inject } from "vue"

const props = defineProps([ "data", "width", "height", "labels" ])

const options = ref({
    legend : {
        show: true
    },
    chart: {
        type: 'heatmap'
    },
    colors: ["#008FFB"],
    labels: props.labels
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
    <div class="heatmap-chart"> 
        <apexchart
            type="heatmap"
            :width="props.width"
            :height="props.height"
            :options="options"
            :series="series"
        />  
    </div> 
</template> 

<style lang="scss" scoped> 
    .heatmap-chart {
        margin-top: 0px;
    }
</style> 