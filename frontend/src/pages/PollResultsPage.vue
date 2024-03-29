<script setup> 

import FunnelChart from "@/components/charts/FunnelChart.vue" 
import HorizontalBarChart from "@/components/charts/HorizontalBarChart.vue" 
import HorizontalStackedBarChart from "@/components/charts/HorizontalStackedBarChart.vue" 
import LineChart from "@/components/charts/LineChart.vue" 
import DonutChart from "@/components/charts/DonutChart.vue"
import LinesChart from "@/components/charts/LinesChart.vue"
import HeatMapChart from "@/components/charts/HeatMapChart.vue"

import { Locations } from "@/utils/locations.js"
import DefaultLayout from "../layouts/DefaultLayout.vue"
import { Poll } from "@/utils/poll.js"
import { ref, watch, onMounted, shallowRef } from "vue"
import { useRoute } from  "vue-router"
import { Helpers } from "@/utils/helpers.js"
import Modal from "@/components/Modal.vue"
import Accordion from "@/components/Accordion.vue"


const poll = ref({})
const results = ref({})

const modalShown = ref(false)

const route = useRoute()
const fetched = ref(false)

const selectedChart = ref(0)
const selectedRegion = ref("NCR")
const resultEndpoint = ref(null)

const data = ref({})
const labels = ref({})
const args = ref({
    filter_field : "user.info.region",
    filter_value : "NCR"
})

async function getInfo() {
    poll.value = await Poll.getInfo(route.params.pollId)
}

function clearEndpoints() { 
    resultEndpoint.value = null
}

function setEndpoint(key) {
    resultEndpoint.value = key 
}


async function getData() {
    fetched.value = false 
    await getInfo() 
    await getResults()
    fetched.value = true
}


async function getResults() {
    const endpoint = reports[selectedChart.value]["endpoint"]
    const filter = reports[selectedChart.value]["filter"]
    let filterer = {} 

    if(filter) {
        filterer = args.value
    }

    const fetchedData = 
        (await Poll.getResults(pollId.value, endpoint, filterer)).data  
    reports[selectedChart.value].normalize(fetchedData)
}

let chartRegistry = shallowRef(null)
let chartData = {}

watch(() => route.params.pollId, async () => {
    await getData()
})

onMounted(async () => {
    await getData()
})

const pollId = ref(route.params.pollId) 

const reports = [
    { 
        title : "line.total-answers-over-time", 
        endpoint : "answers-per-day", 
        normalize : (rawData) => {
            let total = 0

            for(let i = 0; i < rawData.length; i++) {
                total += rawData[i]["count"]
                rawData[i]["count"] = total
            }

            data.value =  Helpers.rekey(rawData, {
                "key" : "x", 
                "count" : "y"
            }, {
                "x" : (v) => new Date(v)
            })
        }
    }, 
    {
        title : "line.answers-over-time",
        endpoint : "answers-per-day", 
        normalize : (rawData) => {
            data.value =  Helpers.rekey(rawData, {
                "key" : "x", 
                "count" : "y"
            }, {
                "x" : (v) => new Date(v)
            })
        }
    }, 
    {
        title : "line.answers-per-day-choices",
        endpoint : "answers-per-day/choices", 
        normalize : (rawData) => {
            const formedData = {} 
            const total = {}

            for(let i = 0; i < rawData.length; i++) {
                let item = rawData[i] 
                const answer = item["subkey"]
                const date = item["key"]
                const count = item["count"]

                if(!(answer in formedData)) {
                    formedData[answer] = []
                    total[answer] = 0
                }

                total[answer] += count

                formedData[answer].push({
                    x : new Date(date), 
                    y : total[answer]
                })

            }

            const normData = [] 


            for(let key in formedData) {
                normData.push({
                    name: key, 
                    data: formedData[key]
                })
            }

            console.log(normData)

            data.value = normData
        }
    }, 
    {
        title : "pie.answers-by-choice", 
        endpoint : "answers-by-choice", 
        normalize : (rawData) => {
            labels.value = Helpers.extractLabels(rawData)
            data.value = Helpers.extractCounts(rawData)
        }
    }, 
    {
        title : "bar.answers-by-choice", 
        endpoint : "answers-by-choice", 
        normalize : (rawData) => {
            labels.value = Helpers.extractLabels(rawData)
            data.value = Helpers.extractCounts(rawData)
        }
    }, 
    {
        title : "funnel.answers-by-age", 
        endpoint : "answers-by/age", 
        normalize : (rawData) => {
            labels.value = Helpers.extractLabels(rawData)
            data.value = Helpers.extractCounts(rawData)
        }
    }, 
    {
        title : "pie.answers-by-gender",
        endpoint : "answers-by/gender", 
        normalize : (rawData) => {
            labels.value = Helpers.extractLabels(rawData)
            data.value = Helpers.extractCounts(rawData)
        }
    }, 
    {
        title : "pie.answers-by-age", 
        endpoint : "answers-by/age", 
        normalize : (rawData) => {
            labels.value = Helpers.extractLabels(rawData)
            data.value = Helpers.extractCounts(rawData)
        }   
    }, 
    {
        title : "pie.answers-by-region", 
        endpoint : "answers-by/region", 
        normalize : (rawData) => {
           labels.value = Helpers.extractLabels(rawData)
           data.value = Helpers.extractCounts(rawData)
        }
    }, 
    {
        title : "pie.answers-by-province", 
        endpoint : "answers-by/province", 
        normalize : (rawData) => {
            labels.value = Helpers.extractLabels(rawData)
            data.value = Helpers.extractCounts(rawData)
        }
    }, 
    {
        title : "stacked-bar.answers-by-gender", 
        endpoint : "stacked-by/gender", 
        normalize : (rawData) => {
            data.value = rawData
        }
    }, 
    {
        title : "stacked-bar.answers-by-age",
        endpoint : "stacked-by/age", 
        normalize : (rawData) => {
            data.value = rawData
        }
    }, 
    {
        title : "stacked-bar.answers-by-region", 
        endpoint : "stacked-by/region",
        normalize : (rawData) => {
            data.value = rawData
        }
    }, 
    {
        title : "stacked-bar.answers-by-province", 
        endpoint : "stacked-by/province",
        filter : true, 
        normalize : (rawData) => {
            data.value = rawData
        }
    }, 
    {
        title : "heatmap.answers-by-age-and-gender", 
        endpoint : "paired-map/age/gender", 
        normalize : (rawData) => {
            const normData = Helpers.normalizedPairedMap(rawData)
            data.value = normData.data 
            labels.value = normData.labels
        }
    }, 
    {
        title : "heatmap.answers-by-region-and-gender", 
        endpoint : "paired-map/region/gender", 
        normalize : (rawData) => {
            const normData = Helpers.normalizedPairedMap(rawData)
            data.value = normData.data 
            labels.value = normData.labels      
        }
    },
    {
        title : "heatmap.answers-by-region-and-age", 
        endpoint : "paired-map/region/age", 
        normalize : (rawData) => {
            const normData = Helpers.normalizedPairedMap(rawData)
            data.value = normData.data 
            labels.value = normData.labels
        }
    },
    {
        title : "heatmap.answers-by-province-and-age", 
        endpoint : "paired-map/province/gender", 
        filter : true, 
        normalize : (rawData) => {
            if(rawData.length == 0) {
                data.value = null
            } else {
                const normData = Helpers.normalizedPairedMap(rawData)
                data.value = normData.data 
                labels.value = normData.labels
            }
        }
    },
    {
        title : "heatmap.answers-by-province-and-age", 
        endpoint : "paired-map/province/age", 
        filter : true, 
        normalize : (rawData) => {
            if(rawData.length == 0) {
                data.value = null
            } else {
                const normData = Helpers.normalizedPairedMap(rawData)
                data.value = normData.data 
                labels.value = normData.labels
            }
        }
    },
]

async function onPartitionExpand(index) {
    selectedChart.value = index - 1
    await getData()
}

watch(() => route.params.pollId, () => {
    pollId.value = route.params.pollId
})

async function handleSelectRegion(key) {
    console.log("Hello!")
    args.value.filter_key = "user.info.region"
    args.value.filter_value = selectedRegion.value
    await getData()
}

</script> 

<template> 
    <div class="poll-results-page"> 
        <DefaultLayout>
            <div class="poll-results-content"> 
                <div class="title">
                    <h1>{{ poll.title }}</h1>
                </div>
                <div class="info"> 
                    <table> 
                        <tr> 
                            <td class="key">
                                Posted On  
                            </td>
                            <td class="value" v-if="poll['created_at']">
                                {{ Helpers.daysAgoText(poll["created_at"]["$date"]) }}, 
                                {{ Helpers.timeText(poll["created_at"]["$date"]) }}
                            </td>
                        </tr> 
                        <tr> 
                            <td class="key">
                                Posted By  
                            </td>
                            <td class="value" v-if="poll['user']">
                                {{ poll["user"]["info"]["username"] }}
                            </td>
                        </tr> 
                        <tr> 
                            <td class="key"> 
                                No. of Votes 
                            </td> 
                            <td class="value" v-if="poll['meta']"> 
                                {{ poll["meta"]["no_of_answers"]}}
                            </td> 
                        </tr>
                    </table> 
                </div> 
                <div class="results"> 
                    <Accordion 
                        class="charts" :itemsLength="19"
                        @onExpand="onPartitionExpand"
                        :loading="!fetched"
                    >
                        <!-- Total Answers Over Time -->
                        <template v-slot:partition-1-title> 
                            Total Answers Over Time (Line Graph)
                        </template> 
                        <template v-slot:partition-1-content> 
                            <LineChart 
                                width="600" 
                                :data="data"
                            />
                        </template> 

                        <!-- Answers Over Time -->
                        <template v-slot:partition-2-title> 
                            Answers Over Time (Line Graph)
                        </template> 
                        <template v-slot:partition-2-content> 
                            <LineChart 
                                width="600" 
                                :data="data"
                            />
                        </template> 

                        <!-- Answers Over Time -->
                        <template v-slot:partition-3-title> 
                            Answers Over Time - per Choice (Line Graph)
                        </template> 
                        <template v-slot:partition-3-content> 
                            <LinesChart 
                                width="600" 
                                :data="data"
                            />
                        </template> 

                        <!-- Answers by Choice (Pie Chart) -->
                        <template v-slot:partition-4-title> 
                            Answers by Choice (Pie Chart)
                        </template> 
                        <template v-slot:partition-4-content> 
                            <DonutChart 
                                width="600" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 
                    
                        <!-- Answers by Choice (Bar Chart) -->
                        <template v-slot:partition-5-title> 
                            Answers by Choice (Bar Chart)
                        </template> 
                        <template v-slot:partition-5-content> 
                            <HorizontalBarChart 
                                width="600" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Age (Funnel Chart) -->
                        <template v-slot:partition-6-title> 
                            Answers by Age (Funnel Chart)
                        </template> 
                        <template v-slot:partition-6-content> 
                            <FunnelChart 
                                width="600"
                                :data="data" 
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Gender (Pie Chart) -->
                        <template v-slot:partition-7-title> 
                            Answers by Gender (Pie Chart)
                        </template> 
                        <template v-slot:partition-7-content> 
                            <DonutChart 
                                width="600" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Age (Pie Chart) -->
                        <template v-slot:partition-8-title> 
                            Answers by Age (Pie Chart)
                        </template> 
                        <template v-slot:partition-8-content> 
                            <DonutChart 
                                width="500" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Region (Pie Chart) -->
                        <template v-slot:partition-9-title> 
                            Answers by Region (Pie Chart)
                        </template> 
                        <template v-slot:partition-9-content> 
                            <DonutChart 
                                width="600" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Province (Pie Chart) -->
                        <template v-slot:partition-10-title> 
                            Answers by Province (Pie Chart)
                        </template> 
                        <template v-slot:partition-10-content> 
                            <DonutChart 
                                width="600" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Gender (Stacked Bar Chart) -->
                        <template v-slot:partition-11-title> 
                            Answers by Gender (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-11-content> 
                            <div class="chart">
                                <HorizontalStackedBarChart 
                                    width="600" 
                                    :data="data"
                                    :labels="labels"
                                />
                            </div>
                        </template> 

                        <!-- Answers by Age (Stacked Bar Chart) -->
                        <template v-slot:partition-12-title> 
                            Answers by Age (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-12-content> 
                            <HorizontalStackedBarChart 
                                width="600" 
                                height="600"
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Region (Stacked Bar Chart) -->
                        <template v-slot:partition-13-title> 
                            Answers by Region (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-13-content> 
                            <HorizontalStackedBarChart 
                                width="600" 
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Province (Stacked Bar Chart) -->
                        <template v-slot:partition-14-title> 
                            Answers by Province (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-14-content> 
                            <div class="chart">
                                <select
                                    @change="handleSelectRegion()"
                                    v-model="selectedRegion"
                                >
                                    <option 
                                        v-for="region in Locations.regions" 
                                        :key="region['key']"
                                        :value="region['key']"
                                    >
                                        {{ region['key']  + " - " + region['long'] }}
                                    </option>
                                </select>
                                <br />
                                <HorizontalStackedBarChart 
                                    width="600" 
                                    height="500"
                                    :data="data"
                                    :labels="labels"
                                />
                            </div>
                        </template> 

                        <!-- Answers by Age & Gender (Heatmap Chart) -->
                        <template v-slot:partition-15-title> 
                            Answers by Age &amp; Gender (Heatmap Chart)
                        </template> 
                        <template v-slot:partition-15-content> 
                            <HeatMapChart 
                                width="600" 
                                height="500"
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Region & Gender (Heatmap Chart) -->
                        <template v-slot:partition-16-title> 
                            Answers by Region &amp; Gender (Heatmap Chart)
                        </template> 
                        <template v-slot:partition-16-content> 
                            <HeatMapChart 
                                width="600" 
                                height="500"
                                :data="data"
                                :labels="labels"
                            />
                        </template> 

                        <!-- Answers by Region & Age (Heatmap Chart) -->
                        <template v-slot:partition-17-title> 
                            Answers by Region &amp; Age (Heatmap Chart)
                        </template> 
                        <template v-slot:partition-17-content> 
                            <HeatMapChart 
                                width="600" 
                                height="500"
                                :data="data"
                                :labels="labels"
                            />
                        </template> 


                        <!-- Answers by Region & Gender (Heatmap Chart) -->
                        <template v-slot:partition-18-title> 
                            Answers by Province &amp; Gender (Heatmap Chart)
                        </template> 
                        <template v-slot:partition-18-content> 
                            <div class="chart">
                                <select
                                    @change="handleSelectRegion()"
                                    v-model="selectedRegion"
                                >
                                    <option 
                                        v-for="region in Locations.regions" 
                                        :key="region['key']"
                                        :value="region['key']"
                                    >
                                        {{ region['key']  + " - " + region['long'] }}
                                    </option>
                                </select>
                                <br />
                                <HeatMapChart 
                                    width="600" 
                                    :data="data"
                                    :labels="labels"
                                />
                            </div>
                        </template> 

                        <!-- Answers by Region & Age (Heatmap Chart) -->
                        <template v-slot:partition-19-title> 
                            Answers by Province &amp; Age (Heatmap Chart)
                        </template> 
                        <template v-slot:partition-19-content> 
                            <div class="chart">
                                <select
                                    @change="handleSelectRegion()"
                                    v-model="selectedRegion"
                                >
                                    <option 
                                        v-for="region in Locations.regions" 
                                        :key="region['key']"
                                        :value="region['key']"
                                    >
                                        {{ region['key']  + " - " + region['long'] }}
                                    </option>
                                </select>
                                <br />
                                <HeatMapChart 
                                    width="600" 
                                    :data="data"
                                    :labels="labels"
                                    v-if="data"  
                                />
                                <div class="no-data" v-else> 
                                    No Data 
                                </div>
                            </div>
                        </template> 
                    </Accordion>
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style lang="scss" scoped> 
    .poll-results-page {
        padding-bottom: 100px;

        .poll-results-content {
            width: 760px;
            margin: 0 auto;

            .title {
                text-align: center;
            }

            .info { 
                table {
                    border-collapse: collapse;
                    width: 764px;

                    td { 
                        border: 2px solid black;
                    }

                    .key { 
                        font-weight: bold;
                        font-size: 16px;
                        width: 160px;
                        padding: 10px;
                        background-color: rgb(50, 50, 50    ); 
                        color: white;
                    }

                    .value {
                        border: 2px solid black;
                        width: 630px;   
                        font-weight: bold; 
                        text-align: center;
                    }
                }
            }

            .results {
                .charts {
                    margin-top: 20px;
                }
            }

        }   

        .loading {
            width: 760px; 
            height: 200px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            border: 2px solid black; 
            border-radius: 5px; 
            margin: 0 auto;
            background-color: rgb(234, 234, 234);

            .inner {
                text-align: center;

                .loading-icon { 
                    margin-bottom: 20px;
                    img {
                        width: 50px;
                    }
                }

                .loading-icon {
                    -webkit-animation: rotation 1s infinite linear;
                }

                @-webkit-keyframes rotation {
                    from {-webkit-transform: rotate(0deg);}
                    to   {-webkit-transform: rotate(359deg);}
                }
            }
        }

        .select-province {
            width: 502px;
            height: 410px;
            font-size: 20px;
            display: flex; 
            align-items: center;
            justify-content: center;
            background-color: rgb(234, 234, 234);
            border: 2px solid black;
        }

        .chart {
            padding: 10px 0px;
        }

        button {
            width: 500px;
            padding: 10px 20px;
        }
    }
</style>