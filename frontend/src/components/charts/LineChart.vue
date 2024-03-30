<script setup> 
import { ref } from "vue"

const props = defineProps([ "data", "width", "height" ])

const options = ref({
    xaxis : {
        type : "datetime"
    },
    legend : {
        position : "top"
    }
})

const series = ref([
    {
        name: "TOTAL", 
        data: props.data
    }
])

function updateData(data) {
    series.value[0].data = data
}

defineExpose({ updateData });

</script> 

<template> 
    <div class="line-chart"> 
        <apexchart
            type="line"
            :width="props.width"
            :height="props.height"
            :options="options"
            :series="series"
        />  
    </div> 
</template> 

<style lang="scss" scoped> 
    .line-chart {     
    }
</style> 