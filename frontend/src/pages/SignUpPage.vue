<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="sign-up-page"> 
        <DefaultLayout>
            <div class="sign-up-form">
                <div class="title"> 
                    <h1>Sign Up</h1>
                </div> 
                <div class="form">
                    <div class="form-item">
                        <input 
                            type="text"
                            placeholder="Username"
                        /> 
                    </div> 
                    <div class="form-item">
                        <input 
                            type="text"
                            placeholder="E-mail Address"
                        /> 
                    </div> 
                    <div class="form-item">
                        <input 
                            type="password"
                            placeholder="Password"
                        />
                    </div> 
                    <div class="form-item">
                        <input 
                            type="password"
                            placeholder="Confirm Password"
                        /> 
                    </div> 
                    <div class="birthdate form-item-flex">
                        <div class="form-subitem label">
                            <b>BIRTHDATE</b>
                        </div>
                        <div class="form-subitem datepicker">
                            <input 
                                type="date" 
                            />
                        </div>
                    </div> 
                    <div class="email-code form-item-flex">
                        <div class="form-subitem email-verification-code">
                            <input 
                                type="number" 
                                placeholder="E-mail Code"
                            />
                        </div>
                        <div class="form-subitem send-email-code">
                            <button class="wide-btn">
                                Send E-mail Code
                            </button>
                        </div>
                    </div> 
                    <div class="form-item">
                        <input 
                            type="text"
                            placeholder="Mobile Number"
                        /> 
                    </div> 
                    <div class="sms-code form-item-flex">
                        <div class="form-subitem mobile-verification-code">
                            <input 
                                type="number" 
                                placeholder="SMS Code"
                            />
                        </div>
                        <div class="form-subitem send-sms-code">
                            <button class="wide-btn">
                                Send SMS Code
                            </button>
                        </div>
                    </div>
                    <div class="terms-and-conditions form-item-flex">
                        <div class="form-subitem message">
                            I agree to the&nbsp;<b>Terms and Conditions</b>
                        </div>  
                        <div class="form-subitem checkbox">
                            <input 
                                type="checkbox" 
                            />
                        </div>
                    </div>
                    <div class="privacy-policy form-item-flex">
                        <div class="form-subitem message">
                            I agree to the&nbsp;<b>Privacy Policy</b>.
                        </div>  
                        <div class="form-subitem checkbox">
                            <input 
                                type="checkbox" 
                            />
                        </div>
                    </div>
                </div> 
                <div class="controls"> 
                    <button class="wide-btn">
                        Sign Up
                    </button>
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .sign-up-page {

        .sign-up-form {
            margin-bottom: 100px;
            margin-left: auto; 
            margin-right: auto; 
            
            width: 512px; 

            .title {
                margin: 0px; 
                padding: 0px;
                font-weight: bold;
                font-size: 14px;
            }

            .form {
                display: flex; 
                flex-direction: column;
                gap: 10px;

                .birthdate.form-item-flex {
                    
                    .form-subitem.label {
                        width: 128px;
                        display: flex;
                        align-items: center;
                    }

                    .form-subitem.datepicker {
                        flex: 1;
                        input {
                            width: 100%;
                        }
                    }

                }

                .email-code.form-item-flex {

                    .form-subitem.email-verification-code {

                    }

                    .form-subitem.send-email-code {
                        flex: 1;
                    }

                }   

                .sms-code.form-item-flex {

                    .form-subitem.mobile-verification-code {

                    }

                    .form-subitem.send-sms-code {
                        flex: 1;
                    }

                }   

                .terms-and-conditions.form-item-flex {
                    .message {
                        display: flex; 
                        align-items: center;
                        flex : 1;
                    }

                    .checkbox {
                        margin-right: 5px;
                    }
                }

                .privacy-policy.form-item-flex {
                    .message {
                        display: flex; 
                        align-items: center;
                        flex : 1;
                    }

                    .checkbox {
                        margin-right: 5px;
                        border: none;
                    }
                }
            }


            .controls {
                margin-top: 20px;
                display: flex;
                width: 100%;

            }
        }
    }

</style>