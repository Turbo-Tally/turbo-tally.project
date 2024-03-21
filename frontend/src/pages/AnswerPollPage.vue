<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="answer-poll-page"> 
        <DefaultLayout>
            <div class="answer-poll-content"> 
                <div class="title"> 
                    <h1>What is your favorite color?</h1>
                </div> 
                <div class="answer-input"> 
                    <input type="text" placeholder="Type an answer..." />
                </div>
                <div class="choices"> 
                    <div class="choice"> 
                        <div class="label"> 
                            ASUL
                        </div>
                    </div> 
                    <div class="choice"> 
                        <div class="label">
                            BERDE 
                        </div>
                    </div>
                    <div class="choice"> 
                        <div class="label">
                            DILAW 
                        </div> 
                    </div>
                    <div class="choice"> 
                        <div class="label">
                            PULA 
                        </div>
                    </div> 
                </div>
                <div class="controls"> 
                    <div 
                        class="skip" 
                        style="text-align: left;"
                    > 
                        <div class="label"> 
                            <button 
                                class="primary-btn"
                                style="background-color: rgb(50, 50, 50);"
                            > 
                                SKIP
                            </button> 
                        </div>
                    </div> 
                    <div 
                        class="submit" 
                        style="text-align: right"
                    > 
                        <div class="label">
                            <button 
                                class="primary-btn" 
                            > 
                                SUBMIT
                            </button> 
                        </div>
                    </div>
                </div>
            </div> 
        </DefaultLayout>
    </div> 
</template> 

<style lang="scss" scoped> 
    .answer-poll-page {
        .answer-poll-content {
            width: 512px;
            box-shadow: 0px 0px 2px black;
            padding: 5px 20px;
            margin: 0 auto;
            padding-bottom: 30px;

            .title {
                margin-top: 20px;
                h1 {
                    margin: 0px; 
                    padding: 0px;
                }
            }

            .answer-input {
                margin-top: 15px;
            }

            .choices {
                margin-top: 20px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px; 

                .choice {
                    width: 100%;
                    flex: 48%;
                    box-shadow: 0 0 0 1px black;
                    margin-bottom: 10px;
                    cursor: pointer;
                    user-select: none;

                    .label {
                        margin: 20px;
                    }
                 
                }
                
                .choice:hover {
                    background-color: rgb(200, 200, 200);
                    opacity: 0.8;
                }

                .choice:active {
                    opacity: 0.5;
                }
            }

            .controls {
                display: flex; 
                gap: 5px;
                margin-top: 20px;

                > div {
                    flex: 1;

                    button {
                        width: 80%;
                        height: 40px;
                    }
                }
            }
        }
    }
</style>