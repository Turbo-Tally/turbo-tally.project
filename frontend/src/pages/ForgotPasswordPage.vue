<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="forgot-password-page"> 
        <DefaultLayout>
            <div class="forgot-password-form">
                <div class="title"> 
                    <h1>Forgot Password?</h1>
                </div> 
                <div class="form">
                    <input 
                        type="text"
                        placeholder="E-mail Address"
                    /> 
                </div> 
                <div class="controls"> 
                    <button class="primary-btn">
                        Log In
                    </button>
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .forgot-password-page {
        .forgot-password-form {
            width: 512px; 
            margin: 0 auto;

            .title {
                h1 {
                    font-size: 24px;
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
                height: 32px;
            }
        }
    }
</style>