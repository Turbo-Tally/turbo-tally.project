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


const poll = ref({})
const results = ref({})

const modalShown = ref(false)

const route = useRoute()
const fetched = ref(false)

const selectedChart = ref("")

async function getInfo() {
    poll.value = await Poll.getInfo(route.params.pollId)
}

async function getResults() {
    results.value = await Poll.getNormalizedResults(route.params.pollId)
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
    console.log(selectedChart)
}


let chartRegistry = shallowRef(null)

watch(() => route.params.pollId, async () => {
    await getData()
})

onMounted(async () => {
    await getData()

    let chartData = {}
    
    chartData["total-per-day-answers.line-chart"] = {
        data: Helpers.rekey(results.value["total_per_day_answers"], {
            "_id" : "x", 
            "answer_count" : "y"
        }, {
            "x" : (v) => new Date(v)
        })
    }
    
    chartData["per-day-answers.line-chart"] = {
        data: Helpers.rekey(results.value["per_day_answers"], {
            "_id" : "x", 
            "answer_count" : "y"
        }, {
            "x" : (v) => new Date(v)
        })
    } 

    chartData["all-answers.by-choice"] = {
        labels: Object.keys(
            Helpers.extractChoices(
                results.value["all_answers"]["by_choice"]
            )
        ),
        data: Object.values(
            Helpers.extractChoices(
                results.value["all_answers"]["by_choice"]
            )
        )
    }
 
    chartData["all-answers.by-age"] = {
        labels: Object.keys(
            Helpers.extractChoices(
                results.value["all_answers"]["by_age"]
            )
        ),
        data: Object.values(
            Helpers.extractChoices(
                results.value["all_answers"]["by_age"]
            )
        )
    }

    chartData["all-answers.by-province"] = {
        labels: Object.keys(
            Helpers.extractChoices(
                results.value["all_answers"]["by_province"]
            )
        ),
        data: Object.values(
            Helpers.extractChoices(
                results.value["all_answers"]["by_province"]
            )
        )
    }

    chartData["all-answers.by-region"] = {
        labels: Object.keys(
            Helpers.extractChoices(
                results.value["all_answers"]["by_region"]
            )
        ),
        data: Object.values(
            Helpers.extractChoices(
                results.value["all_answers"]["by_region"]
            )
        )
    }

    chartData["all-answers.by-gender"] = {
        labels: Object.keys(
            Helpers.extractChoices(
                results.value["all_answers"]["by_gender"]
            )
        ),
        data: Object.values(
            Helpers.extractChoices(
                results.value["all_answers"]["by_gender"]
            )
        )
    }

    chartData["stacked.by-province"] =       
        results.value["by_category"]["stacked_by_province"]

    chartData["stacked.by-age"] =       
        results.value["by_category"]["stacked_by_age"]

    chartData["stacked.by-region"] =       
        results.value["by_category"]["stacked_by_region"]

    chartData["stacked.by-gender"] =       
        results.value["by_category"]["stacked_by_gender"]

    chartRegistry.value = {
        /** Small Charts */
        "total-per-day-answers.line-chart:SMALL" : {
            component: LineChart, 
            props: {
                width: 760,
                height: 150,
                ...chartData["total-per-day-answers.line-chart"]
            }
        }, 
        "per-day-answers.line-chart:SMALL" : {
            component: LineChart, 
            props: {
                width: 760,
                height: 150,
                ...chartData["per-day-answers.line-chart"]
            }
        },
        "all-answers.pie-chart:SMALL" : {
            component: PieChart, 
            props: {
                width: 150,
                height: 300,
                ...chartData["all-answers.by-choice"]
            }
        }, 
        "all-answers.bar-chart:SMALL" : {
            component: HorizontalBarChart, 
            props: {
                width: 200,
                height: 150,
                ...chartData["all-answers.by-choice"]
            }
        }, 
        "all-answers.funnel-chart:SMALL" : {
            component: FunnelChart, 
            props: {
                width: 200,
                height: 150,
                ...chartData["all-answers.by-age"]
            }
        }, 
        "all-answers.age.pie-chart:SMALL" : {
            component: PieChart, 
            props: {
                width: 200,
                height: 150,
                ...chartData["all-answers.by-age"]
            }
        }, 
        "all-answers.region.pie-chart:SMALL" : {
            component: PieChart, 
            props: {
                width: 200,
                height: 150,
                ...chartData["all-answers.by-region"]
            }
        }, 
        "all-answers.gender.pie-chart:SMALL" : {
            component: PieChart, 
            props: {
                width: 200,
                height: 150,
                ...chartData["all-answers.by-gender"]
            }
        },
        "all-answers.provinces.pie-chart:SMALL" : {
            component: PieChart, 
            props: {
                width: 200,
                height: 150,
                ...chartData["all-answers.by-province"]
            }
        },
        "all-answers.provinces.stacked-bar-chart:SMALL" : {
            component: HorizontalStackedBarChart, 
            props: {
                width: 320,
                height: 200,
                data: chartData["stacked.by-province"]
            }
        },
        "all-answers.age.stacked-bar-chart:SMALL" : {
            component: HorizontalStackedBarChart, 
            props: {
                width: 200,
                height: 150,
                data: chartData["stacked.by-age"]
            }
        },
        "all-answers.region.stacked-bar-chart:SMALL" : {
            component: HorizontalStackedBarChart, 
            props: {
                width: 200,
                height: 150,
                data: chartData["stacked.by-region"]
            }
        },
        "all-answers.gender.stacked-bar-chart:SMALL" : {
            component: HorizontalStackedBarChart, 
            props: {
                width: 200,
                height: 150,
                data: chartData["stacked.by-gender"]
            }
        },


        /** Small Charts */
        "total-per-day-answers.line-chart:BIG" : {
            component: LineChart, 
            props: {
                width: 730,
                height: 150,
                ...chartData["total-per-day-answers.line-chart"]
            }
        }, 
        "per-day-answers.line-chart:BIG" : {
            component: LineChart, 
            props: {
                width: 730,
                height: 150,
                ...chartData["per-day-answers.line-chart"]
            }
        },
        "all-answers.pie-chart:BIG" : {
            component: PieChart, 
            props: {
                width: 500,
                ...chartData["all-answers.by-choice"]
            }
        }, 
        "all-answers.bar-chart:BIG" : {
            component: HorizontalBarChart, 
            props: {
                width: 500,
                ...chartData["all-answers.by-choice"]
            }
        }, 
        "all-answers.funnel-chart:BIG" : {
            component: FunnelChart, 
            props: {
                width: 500,
                height: 1000,
                ...chartData["all-answers.by-age"]
            }
        }, 
        "all-answers.age.pie-chart:BIG" : {
            component: PieChart, 
            props: {
                width: 500,
                ...chartData["all-answers.by-age"]
            }
        }, 
        "all-answers.region.pie-chart:BIG" : {
            component: PieChart, 
            props: {
                width: 500,
                ...chartData["all-answers.by-region"]
            }
        }, 
        "all-answers.gender.pie-chart:BIG" : {
            component: PieChart, 
            props: {
                width: 500,
                ...chartData["all-answers.by-gender"]
            }
        },
        "all-answers.provinces.pie-chart:BIG" : {
            component: PieChart, 
            props: {
                width: 500,
                ...chartData["all-answers.by-province"]
            }
        },
        "all-answers.provinces.stacked-bar-chart:BIG" : {
            component: HorizontalStackedBarChart, 
            props: {
                height: 1000,
                data: chartData["stacked.by-province"],
                context: "province"
            }
        },
        "all-answers.age.stacked-bar-chart:BIG" : {
            component: HorizontalStackedBarChart, 
            props: {
                height: 1000,
                data: chartData["stacked.by-age"],
                context: "age"
            }
        },
        "all-answers.region.stacked-bar-chart:BIG" : {
            component: HorizontalStackedBarChart, 
            props: {
                height: 1000,
                width: 600,
                data: chartData["stacked.by-region"],
                context: "region"
            }
        },
        "all-answers.gender.stacked-bar-chart:BIG" : {
            component: HorizontalStackedBarChart, 
            props: {
                height: 1000,
                data: chartData["stacked.by-gender"],
                context: "gender"
            }
        }
    }
   
})

</script> 

<template> 
    <div class="poll-results-page"> 
        <DefaultLayout>
            <div class="poll-results-content" v-if="fetched && chartRegistry"> 
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
                <div class="results" v-if="fetched"> 
                    <div class="per-day-answers" style="margin-top: 30px">
                        <b>Per Day Answers</b>
                    </div> 
                    <div 
                        class="line-chart__total-per-day chart" style="margin-top: 10px"
                        @dblclick="enlargeChart('total-per-day-answers.line-chart')"
                    >
                        <component
                            :is="chartRegistry['total-per-day-answers.line-chart:SMALL'].component"
                            v-bind="chartRegistry['total-per-day-answers.line-chart:SMALL'].props" 
                        />
                    </div>
                    <div 
                        class="line-chart__per-day chart" style="margin-top: 10px"
                        @dblclick="enlargeChart('per-day-answers.line-chart')"
                    >
                        <component
                            :is="chartRegistry['per-day-answers.line-chart:SMALL'].component"
                            v-bind="chartRegistry['per-day-answers.line-chart:SMALL'].props" 
                        />
                    </div>
                    
                    <div class="all-answers-header">
                        <b>All Answers</b>
                    </div> 
                    <div class="all-answers-results">
                        <div 
                            class="pie-chart chart"
                            @dblclick="enlargeChart('all-answers.pie-chart')"
                        >
                            <component
                                :is="chartRegistry['all-answers.pie-chart:SMALL'].component"
                                v-bind="chartRegistry['all-answers.pie-chart:SMALL'].props" 
                            />
                        </div> 
                        <div 
                            class="bar-chart chart"
                            @dblclick="enlargeChart('all-answers.bar-chart')"
                        > 
                            <component
                                :is="chartRegistry['all-answers.bar-chart:SMALL'].component"
                                v-bind="chartRegistry['all-answers.bar-chart:SMALL'].props" 
                            />
                        </div> 
                        <div 
                            class="funnel-chart chart"
                            @dblclick="enlargeChart('all-answers.funnel-chart')"
                        > 
                            <component
                                :is="chartRegistry['all-answers.funnel-chart:SMALL'].component"
                                v-bind="chartRegistry['all-answers.funnel-chart:SMALL'].props" 
                            />
                        </div> 
                    </div> 
                    <div class="categorized-results">
                        <div class="pie-chart">
                            <div class="header"> 
                                By Age
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.age.pie-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.age.pie-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.age.pie-chart:SMALL'].props" 
                                />
                            </div>
                        </div> 
                        <div class="pie-chart"> 
                            <div class="header"> 
                                By Region
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.region.pie-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.region.pie-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.region.pie-chart:SMALL'].props" 
                                />
                            </div>
                        </div> 
                        <div class="pie-chart"> 
                            <div 
                                class="header"
                            > 
                                By Gender
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.gender.pie-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.gender.pie-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.gender.pie-chart:SMALL'].props" 
                                />
                            </div>
                        </div> 
                    </div>
                    <div class="categorized-results">
                        <div class="stacked-bar-chart">
                            <div class="header"> 
                                Stacked Bar Chart (age)
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.age.stacked-bar-chart')"
                            > 
                                <component
                                        :is="chartRegistry['all-answers.age.stacked-bar-chart:SMALL'].component"
                                        v-bind="chartRegistry['all-answers.age.stacked-bar-chart:SMALL'].props"
                                    context="age" 
                                />
                            </div>
                        </div> 
                        <div class="stacked-bar-chart"> 
                            <div class="header"> 
                                Stacked Bar Chart (region)
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.region.stacked-bar-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.region.stacked-bar-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.region.stacked-bar-chart:SMALL'].props"
                                    context="region" 
                                />
                            </div>
                        </div> 
                        <div class="stacked-bar-chart"> 
                            <div 
                                class="header"
                            > 
                                Stacked Bar Chart (gender)
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.gender.stacked-bar-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.gender.stacked-bar-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.gender.stacked-bar-chart:SMALL'].props"
                                    context="gender" 
                                />
                            </div>
                        </div> 
                    </div>
                    <div class="categorized-results">
                        <div class="pie-chart">
                            <div class="header"> 
                                Pie Chart (province)
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.provinces.pie-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.provinces.pie-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.provinces.pie-chart:SMALL'].props" 
                                />
                            </div>
                        </div> 
                        <div class="bar-chart"> 
                            <div class="header"> 
                                Stacked Bar Chart (province)
                            </div> 
                            <div 
                                class="chart"
                                @dblclick="enlargeChart('all-answers.provinces.stacked-bar-chart')"
                            > 
                                <component
                                    :is="chartRegistry['all-answers.provinces.stacked-bar-chart:SMALL'].component"
                                    v-bind="chartRegistry['all-answers.provinces.stacked-bar-chart:SMALL'].props" 
                                    context="province"
                                />
                            </div>
                        </div> 
                    </div>
                  
                </div>
            </div>   
            <div class="loading" v-else> 
                Loading Results...
            </div>  
            <Modal 
                v-if="chartRegistry && modalShown && selectedChart" 
                @close="modalShown = false"
                :title="selectedChart"
                :width="chartRegistry[selectedChart + ':BIG'].props.width"
            >   
                <component 
                    :is="chartRegistry[selectedChart  + ':BIG'].component"
                    v-bind="chartRegistry[selectedChart + ':BIG'].props"
                /> 
            </Modal> 
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
                .line-chart__total-per-day {
                    width: 100%;
                    height: 150px;
                    margin-top: 30px;
                    border: 2px solid black;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                } 

                .line-chart__per-day {
                    width: 100%;
                    height: 150px;
                    margin-top: 30px;
                    border: 2px solid black;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                } 

                .all-answers-header {
                    margin-top: 50px;
                }

                .all-answers-results {
                    display: flex;
                    gap: 10px; 

                    > div {
                        margin-top: 15px;
                        flex: 1; 
                        border: 2px solid black;
                        height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center; 
                        align-items: center; 
                    }
                }


                .categorized-results {
                    display: flex;
                    gap: 10px; 
                    margin-top: 20px;

                    > div {
                        margin-top: 15px;
                        flex: 1; 
                        display: flex;
                        flex-direction: column;
                        justify-content: center; 
                        align-items: center; 

                        > .header {
                            text-align: left;
                            width: 100%;
                            margin-bottom: 10px;
                            font-weight: bold;
                        }

                        > .chart {
                            border: 2px solid black;
                            height: 200px;
                            width: 100%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            text-align: center;
                        }
                    }
                }

                .by-province {
                    display: flex;
                    gap: 10px; 
                    margin-top: 20px;

                    > .content {
                        margin-top: 30px;
                        display: flex;
                        flex-direction: row;
                        justify-content: center; 
                        align-items: center; 
                        gap: 5px;
                        width: 245px;
                        gap: 5px;
                        margin-left: 5px;
                       
                    }

                    
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