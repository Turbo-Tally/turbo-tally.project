<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="create-poll-page"> 
        <DefaultLayout>
            <div class="create-poll-content"> 
                <div class="title"> 
                    <h1>Create Poll</h1>
                </div> 
                <div class="title-input"> 
                    <input type="text" placeholder="Enter Question Title..." />
                </div> 
                <div class="choices">
                    <div class="choices-header"> 
                        <div class="title"> 
                            CHOICES 
                        </div>  
                        <div class="controls"> 
                            <button class="primary-btn"> 
                                CLEAR ALL 
                            </button> 
                            <button class="primary-btn"> 
                                + ADD CHOICE 
                            </button> 
                        </div>
                    </div> 
                    <div class="choice-results"> 
                        <div class="choice"> 
                            <div class="name"> 
                                Berde
                            </div> 
                            <div class="trash"> 
                                🗑️ 
                            </div> 
                        </div> 
                        <div class="choice"> 
                            <div class="name"> 
                                Dilaw
                            </div> 
                            <div class="trash"> 
                                🗑️ 
                            </div> 
                        </div> 
                        <div class="choice"> 
                            <div class="name"> 
                                Asul
                            </div> 
                            <div class="trash"> 
                                🗑️ 
                            </div> 
                        </div> 
                    </div>
                    <div class="choice-submit"> 
                        <button class="primary-btn"> 
                            SUBMIT
                        </button> 
                    </div> 
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .create-poll-page {
        .create-poll-content {
            width: 900px;
            box-shadow: 0px 0px 2px black;
            margin: 0 auto;
            padding: 5px 20px;
            padding-bottom: 50px;

            .choices {
                margin-top: 20px;

                .choices-header {
                    display: flex;

                    .title {
                        flex: 1;
                        font-weight: bold;
                        display: flex; 
                        justify-content: left;
                        align-items: center;
                    }

                    .controls {
                        flex: 1; 
                        display: flex;
                        gap: 10px;
                        justify-content: right;


                        button {
                            width: 100px;
                        }
                    }

                }

                .choice-results {
                    margin-top: 15px;
                    display: flex;
                    gap: 10px;
                    flex-direction: column;

                    .choice {
                        background-color: rgb(234, 234, 234);
                        display: flex;
                        padding: 10px;
                        box-shadow: 0px 0px 2px black;

                        .name {
                            font-weight: bold;
                            flex: 1;
                        }

                        .trash {
                            cursor: pointer;
                            outline: none; 
                        }

                        .trash:hover {
                            opacity: 0.8;
                        }

                        .trash:active {
                            opacity: 0.5;
                        }
                    }
                }

                .choice-submit {
                    margin-top: 20px;
                }
            }
        }
    }
</style>