<script setup> 
import { ref } from "vue"

const props = defineProps([ "data", "width", "height" ])

const options = ref({
    xaxis : {
        type: "datetime"
    }
})

const series = ref([{
    name: "TOTAL", 
    data: props.data
}])

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
        margin-top: 20px;
    }
</style> 