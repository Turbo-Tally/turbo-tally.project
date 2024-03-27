<script setup> 

import { ref } from "vue"

const props = defineProps([ "data", "width", "height", "context" ])

const normData = {
    labels: new Set(), 
    answers: new Set(),
    groupedAnswers : {}, 
    normAnswers : [],
    finalAnswers : []
} 

function normalizeData() {
    const data = props.data 

    for(let item of data) {
        const label = item._id[props.context] 
        const answer = item._id.answer  

        normData.labels.add(label)
        normData.answers.add(answer)
    }

    normData.labels = Array.from(normData.labels)
    normData.answers = Array.from(normData.answers)

    for(let item of data) {
        const province = item._id[props.context] 
        const answer = item._id.answer  
        const answer_count = item.answer_count

        if(!(answer in normData.groupedAnswers)) {
            normData.groupedAnswers[answer] = {}
        }

        normData.groupedAnswers[answer][province] = answer_count
    }

    for(let answer in normData.groupedAnswers) {
        for(let label of normData.labels) {
            if(!(label in normData.groupedAnswers[answer])) {
                normData.groupedAnswers[answer][label] = 0
            }
        }
    }

    for(let answer in normData.groupedAnswers) {
        normData.normAnswers[answer] = []

        for(let label of normData.labels) {
            normData.normAnswers[answer].push(
                normData.groupedAnswers[answer][label]
            )
        }
    }

    for(let answer in normData.normAnswers) {
        normData.finalAnswers.push({
            name: answer, 
            data: normData.normAnswers[answer]
        })
    }
    
    console.log(props.data)
    console.log(normData)
}

normalizeData()

const options = ref({
    plotOptions: {
        bar: {
            horizontal: true,
            dataLabels: {
                total: {
                    enabled: true,
                    offsetX: 0,
                    style: {
                        fontSize: '13px',
                        fontWeight: 900
                    }
                }   
            }
        }
    },
    series: {
        stacking: 'normal',
        dataLabels: {
            enabled: true
        }
    },
    chart : {
        stacked: true,
    }, 
    legend: {
        show: false
    },
    xaxis: {
        categories: normData.labels
    }
})


const series = ref(normData.finalAnswers)

</script> 

<template> 
    <div class="horizontal-stacked-bar-chart"> 
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
    .horizontal-stacked-bar-chart {
        margin-top: 20px;
    }
</style> 