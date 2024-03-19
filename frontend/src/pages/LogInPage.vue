<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="log-in-page"> 
        <DefaultLayout>
            <div class="log-in-form">
                <div class="title"> 
                    <h1>Log In</h1>
                </div> 
                <div class="form">
                    <input 
                        type="text"
                        placeholder="E-mail Address"
                    /> 
                    <input 
                        type="text"
                        placeholder="Password"
                    /> 
                </div> 
                <div class="controls"> 
                    <div class="forgot-password-link"> 
                        <a href="/#/forgot-password">Forgot Password?</a>
                    </div> 
                    <div class="log-in-button">
                        <button>Log In</button>
                    </div>
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .log-in-page {
        .log-in-form {
            width: 512px; 
            margin: 0 auto;

            .title {
                h1 {
                    font-size: 28px;
                }
            }

            .form {
                display: flex;
                flex-direction: column; 
                gap: 10px;
            }

            .controls {
                margin-top: 20px;
                display: flex;
                width: 100%;

                .forgot-password-link {
                    flex: 1;
                 
                    a {
                        color: black;
                        text-decoration: underline; 
                    }
                }

                .log-in-button {
                    width: 100px;

                  
                }

            }
        }
    }
</style>