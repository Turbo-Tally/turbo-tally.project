<script setup> 

import FunnelChart from "@/components/charts/FunnelChart.vue" 
import HorizontalBarChart from "@/components/charts/HorizontalBarChart.vue" 
import HorizontalStackedBarChart from "@/components/charts/HorizontalStackedBarChart.vue" 
import LineChart from "@/components/charts/LineChart.vue" 
import PieChart from "@/components/charts/PieChart.vue"

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

const selectedChart = ref("")

const resultEndpoints = ref({
    "answers-per-day" : false, 
    "answers-by-age" : false,
    "answers-by-gender" : false,
    "answers-by-region" : false,
    "answers-by-province" : false, 
    "stacked-by-age" : false, 
    "stacked-by-gender" : false, 
    "stacked-by-region" : false, 
    "stacked-by-province" : false 
})

async function getInfo() {
    poll.value = await Poll.getInfo(route.params.pollId)
}

async function getResults() {
    // get results for polls
}

async function getData() {
    fetched.value = false
    await getInfo() 
    await getResults()
    fetched.value = true
}

async function enlargeChart(name) {
    modalShown.value = true 
    selectedChart.value = name
}


let chartRegistry = shallowRef(null)
let chartData = {}

watch(() => route.params.pollId, async () => {
    await getData()
})

onMounted(async () => {
    await getData()
})

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
                    <Accordion class="charts" :itemsLength="14">
                        <!-- Total Answers Over Time -->
                        <template v-slot:partition-1-title> 
                            Total Answers Over Time (Line Graph)
                        </template> 
                        <template v-slot:partition-1-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers Over Time -->
                        <template v-slot:partition-2-title> 
                            Answers Over Time (Line Graph)
                        </template> 
                        <template v-slot:partition-2-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Choice (Pie Chart) -->
                        <template v-slot:partition-3-title> 
                            Answers by Choice (Pie Chart)
                        </template> 
                        <template v-slot:partition-3-content> 
                            Hello, 1
                        </template> 
                    
                        <!-- Answers by Choice (Bar Chart) -->
                        <template v-slot:partition-4-title> 
                            Answers by Choice (Bar Chart)
                        </template> 
                        <template v-slot:partition-4-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Choice (Funnel Chart) -->
                        <template v-slot:partition-5-title> 
                            Answers by Age (Funnel Chart)
                        </template> 
                        <template v-slot:partition-5-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Gender (Pie Chart) -->
                        <template v-slot:partition-6-title> 
                            Answers by Gender (Pie Chart)
                        </template> 
                        <template v-slot:partition-6-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Age (Pie Chart) -->
                        <template v-slot:partition-7-title> 
                            Answers by Age (Pie Chart)
                        </template> 
                        <template v-slot:partition-7-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Region (Pie Chart) -->
                        <template v-slot:partition-8-title> 
                            Answers by Region (Pie Chart)
                        </template> 
                        <template v-slot:partition-8-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Province (Pie Chart) -->
                        <template v-slot:partition-9-title> 
                            Answers by Province (Pie Chart)
                        </template> 
                        <template v-slot:partition-9-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Gender (Stacked Bar Chart) -->
                        <template v-slot:partition-10-title> 
                            Answers by Gender (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-10-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Gender (Stacked Bar Chart) -->
                        <template v-slot:partition-11-title> 
                            Answers by Age (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-11-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Region (Stacked Bar Chart) -->
                        <template v-slot:partition-12-title> 
                            Answers by Region (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-12-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Province (Stacked Bar Chart) -->
                        <template v-slot:partition-13-title> 
                            Answers by Region (Stacked Bar Chart)
                        </template> 
                        <template v-slot:partition-13-content> 
                            Hello, 1
                        </template> 

                        <!-- Answers by Age & Gender (Heatmap Chart) -->
                        <template v-slot:partition-14-title> 
                            Answers by Age &amp; Gender (Heatmap Chart)
                        </template> 
                        <template v-slot:partition-14-content> 
                            Hello, 1
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
    }
</style>