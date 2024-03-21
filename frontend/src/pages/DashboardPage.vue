<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

import ResultCard from "@/components/dashboard/ResultCard.vue"

</script> 

<template> 
    <div class="dashboard-page"> 
        <DefaultLayout>
            <div class="dashboard-content">
                <div class="main-panel"> 
                    <div class="your-activity section">
                        <div class="title"> 
                            Your Activity 
                        </div> 
                        <div class="content"> 
                            <div class="search-box"> 
                                <input 
                                    type="text" 
                                    placeholder="Search..."
                                />
                            </div> 
                            <div class="results" style="margin-top: 16px"> 
                                <ResultCard 
                                    answer="Berde"  
                                    poll="What's your favorite color?" 
                                    :timestamp="{
                                        'date' : 'Today', 
                                        'time' : '7:05 PM'
                                    }"
                                /> 
                                <ResultCard 
                                    answer="Berde"  
                                    poll="What's your favorite pet?" 
                                    :timestamp="{
                                        'date' : 'Today', 
                                        'time' : '7:05 PM'
                                    }"
                                /> 
                            </div>
                        </div>
                    </div> 
                </div> 
                <div class="side-panel"> 
                    <div class="join-a-random-poll section"> 
                        <div class="title"> 
                            Join a Random Poll
                        </div> 
                        <div class="content"> 
                            <button class="wide-btn randomize">
                                Randomize
                            </button> 
                        </div>
                    </div> 
                    <div class="your-polls section"> 
                        <div class="title"> 
                            Your Polls 
                        </div> 
                        <div class="content"> 
                            <div class="search-box"> 
                                <input 
                                    type="text" 
                                    placeholder="Search..."
                                />
                            </div> 
                            <div class="results"> 
                                <div class="result-item">
                                    What's your favorite pet?
                                </div> 
                                <div class="result-item">
                                    What's your favorite color?
                                </div> 
                            </div>
                        </div>
                    </div> 
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss">     
    .dashboard-content {
        display: flex;
        gap: 10px; 
        width: 900px;
        margin: 0 auto;

        .main-panel {
            flex: 1;
        }

        .side-panel {
            width: 320px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .section {
            padding: 20px;
            box-shadow: 0px 0px 2px black;

            .title {
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        }
        
        .randomize:hover {
            opacity: 0.8; 
        }

        .randomize:active {
            opacity: 0.5;
        }

        .results {
            margin-top: 16px;
            gap: 10px; 
            display: flex; 
            flex-direction: column;

            .result-item {
                background-color: rgb(234, 234, 234); 
                padding: 10px 20px;
                box-shadow: 0px 0px 2px black;
                cursor: pointer;
            }

            .result-item:hover {
                opacity: 0.8;
            }

            .result-item:active {
                opacity: 0.5;
            }
        }
       
    }
</style>