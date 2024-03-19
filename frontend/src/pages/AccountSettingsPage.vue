<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="account-settings-page"> 
        <DefaultLayout>
            <div class="account-settings-content">
                <div class="personal-info section">
                    <div class="section-title"> 
                        <h1>Personal Info</h1>
                    </div> 
                    <div class="content"> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Region</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <select class="wide-item">
                                        <option>V - Bikol Region</option>
                                    </select>
                                </div>
                            </div>
                        </div> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Province</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <select class="wide-item">
                                        <option>Camarines Sur</option>
                                    </select>
                                </div>
                            </div>
                        </div> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <div class="form-subitem centered title">
                                    <b>Sex</b>
                                </div> 
                                <div class="form-subitem" style="flex: 1">
                                    <select class="wide-item">
                                        <option>Male</option>
                                    </select>
                                </div>
                            </div>
                        </div> 
                        <div class="controls" style="margin-top: 10px"> 
                            <button class="primary-btn">
                                UPDATE 
                            </button>
                        </div> 
                    </div> 
                </div> 

                <div class="change-email-address section">
                    <div class="section-title"> 
                        <h1>Change E-mail Address</h1>
                    </div> 
                    <div class="content"> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="text"
                                    placeholder="E-mail Address"
                                /> 
                            </div>
                        </div> 
                        <div class="email-code form-content">
                            <div class="form-item-flex">
                                <div 
                                    class="form-subitem email-verification-code"
                                >
                                    <input 
                                        type="number" 
                                        placeholder="E-mail Verification Code"
                                    />
                                </div>
                                <div class="form-subitem send-email-code">
                                    <button class="primary-btn">
                                        Send E-mail Code
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="controls" style="margin-top: 10px"> 
                            <button class="primary-btn">
                                UPDATE 
                            </button>
                        </div> 
                    </div> 
                </div> 

                <div class="change-email-address section">
                    <div class="section-title"> 
                        <h1>Change Password</h1>
                    </div> 
                    <div class="content"> 
                        <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="password"
                                    placeholder="Current Password"
                                /> 
                            </div>
                        </div> 
                           <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="password"
                                    placeholder="New Password"
                                /> 
                            </div>
                        </div> 
                           <div class="form-content"> 
                            <div class="form-item-flex"> 
                                <input 
                                    type="password"
                                    placeholder="Confirm New Password"
                                /> 
                            </div>
                        </div> 
        
                        <div class="controls" style="margin-top: 10px"> 
                            <button class="primary-btn">
                                UPDATE 
                            </button>
                        </div> 
                    </div> 
                </div> 
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style scoped lang="scss"> 
    .account-settings-page {
        .account-settings-content {
            width: 900px;
            margin: 0 auto; 
            display: flex;
            gap: 20px;
            flex-direction: column;
            margin-bottom: 100px;

            .form-content {
                padding: 1px;
            }

            .section-title {
                margin-bottom: 20px;
                
                h1 {
                    font-size: 24px;
                    text-align: center;
                    margin: 0px;
                    padding: 0px;
                }
            }

            .section {
                padding: 20px;
                box-shadow: 0px 0px 2px black;
            

                .form-item-flex { 
                    .title {
                        width: 100px;
                        justify-content: left;
                    }
                }
            }


            .email-code {

                .form-subitem.email-verification-code {
                    flex: 1;
                }

                .form-subitem.send-email-code {
                    width: 150px;
                }

            }  
        }
    }
</style>