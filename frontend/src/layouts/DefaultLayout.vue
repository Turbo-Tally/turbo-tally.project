<script setup>

import NavBar from "@/components/NavBar.vue"

</script> 

<template> 
    <div class="default-layout"> 
        <div class="header ">
            <div class="title"> 
                TurboTally
            </div> 
            <div class="navbar"> 
                <NavBar />
            </div> 
        </div> 

        <div class="content"> 
            <slot></slot>
        </div>
    </div> 
</template> 

<style scoped lang="scss"> 
    .default-layout {
        width: 1024px; 
        margin: 0 auto;      
        
        .header {
            margin-top: 30px; 

            .title {
                font-size: 35px;
                text-align: center;
                font-family: inconsolata;
                font-weight: bold;
            }
        }


        .content {
            margin-top: 20px;
        }   
    }

</style> 