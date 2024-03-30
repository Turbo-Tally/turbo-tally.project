<script setup> 

import { ref } from "vue"

const props = defineProps([ "labels", "data", "width", "height" ])

const options = ref({
    plotOptions: {
        bar: {
            borderRadius: 0,
            horizontal: true,
            barHeight: '80%',
            isFunnel: true,
        }
    },
    dataLabels: {
        enabled: true,
        formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ':  ' + val
        },
        dropShadow: {
            enabled: true,
        },
    },
    xaxis: {
        categories: props.labels,
    }
})

const series = ref([{
    name: "TOTAL", 
    data: props.data
}])

function updateData(data) {
    series.value[0].data = data
}

function updateLabels(labels) {
    options.value.xaxis.categories = labels
}

defineExpose({ updateData, updateLabels });

</script> 

<template> 
    <div class="funnel-chart"> 
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
    .funnel-chart {
        margin: 20px;
    }
</style> 