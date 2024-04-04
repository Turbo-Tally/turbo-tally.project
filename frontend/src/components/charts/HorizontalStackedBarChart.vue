<script setup> 

import { onMounted, ref } from "vue"

const props = defineProps([ "data", "width", "height" ])

let normData = {
    labels: new Set(), 
    answers: new Set(),
    groupedAnswers : {}, 
    normAnswers : [],
    finalAnswers : []
} 

function normalizeData() {
    normData = {
        labels: new Set(), 
        answers: new Set(),
        groupedAnswers : {}, 
        normAnswers : [],
        finalAnswers : []
    } 

    console.log("Normalizing data...")
    const data = props.data 

    for(let item of data) {
        const label = item.key 
        const answer = item.subkey

        normData.labels.add(label)
        normData.answers.add(answer)
    }

    normData.labels = Array.from(normData.labels)
    normData.answers = Array.from(normData.answers)

    for(let item of data) {
        const key = item.key
        const answer = item.subkey
        const answer_count = item.count

        if(!(answer in normData.groupedAnswers)) {
            normData.groupedAnswers[answer] = {}
        }

        normData.groupedAnswers[answer][key] = answer_count
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

    for(let answer of normData.answers) {
        normData.finalAnswers.push({
            name: answer, 
            data: normData.normAnswers[answer]
        })
    }

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
        position: 'top',
        horizontalAlign: 'left',
        offsetX: 40
    },
    xaxis: {
        categories: normData.labels
    }
})

const series = ref(normData.finalAnswers)

function updateData(data) {
    normalizeData(data)
    series.value = normData.finalAnswers
}

function updateLabels(labels) {
    options.value.xaxis.categories = labels
}

defineExpose({ updateData, updateLabels });

onMounted(async () => {
    await normalizeData()
    series.value = normData.finalAnswers
})
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