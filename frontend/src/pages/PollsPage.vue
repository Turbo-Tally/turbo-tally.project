<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

import ResultCard from "@/components/polls/ResultCard.vue"

</script> 

<template> 
    <div class="polls-page"> 
        <DefaultLayout>
            <div class="polls-content"> 
                <div class="search"> 
                    <input 
                        type="text" 
                        placeholder="Search..."
                    />
                </div> 
                <div class="controls"> 
                    <div class="create-new-poll"> 
                        <button class="primary-btn">
                            + Create New Poll
                        </button> 
                    </div> 
                    <div class="sort-poll" > 
                        <div style="flex: 1" />
                        <div class="sort">
                            <select>
                                <option>Recent</option>
                            </select> 
                        </div>
                        <div class="filter">
                            <ul>
                                <li>All</li>
                                <li class="active">Unanswered</li>
                                <li>Answered</li>
                            </ul> 
                        </div>
                    </div>  
                </div> 
                <div class="results"> 
                    <ResultCard 
                        poll="What's your favorite color?" 
                        author="User1234" 
                        timestamp="Today, 7:04PM"
                        votes="1234"
                    />

                    <ResultCard 
                        poll="What's your favorite pet?" 
                        author="User4321"
                        timestamp="Today, 7:04PM"
                        votes="1234"
                    /> 
                </div>    
            </div> 
         
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .polls-page {
        .polls-content {
            width: 900px;
            margin: 0 auto;

            .search {
                input {
                    font-size: 20px;
                }
            }

            .controls {
                margin-top: 14px;
                display: flex;

                .sort-poll {
                    flex: 1;
                    display: flex; 
                    justify-content: right;

                    .filter {
                        margin-left: 10px; 
                        padding-left: 10px; 
                        border-left: 2px solid black;
                        display: flex; 
                        align-items: center;
                        justify-content: center;
                       
                        ul {
                            padding: 0px; 
                            margin: 0px;
                        }

                        ul li {
                            display: inline;
                            margin: 0 10px;
                        }

                        li.active {
                            font-weight: bold;
                        }
                    }
                }
            }

            .results {
                margin-top: 20px;
                display: flex;
                flex-direction: column;
                gap: 16px;

                .result-card-component:hover {
                    opacity: 0.8;
                    cursor: pointer;
                }

                .result-card-component:active {
                    opacity: 0.5;
                    cursor: pointer;
                }
            }
        }
    }
</style>