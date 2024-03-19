<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

</script> 

<template> 
    <div class="poll-results-page"> 
        <DefaultLayout>
            <div class="poll-results-content"> 
                <div class="search"> 
                    <input type="text" />
                </div> 
            </div>     
        </DefaultLayout>
    </div> 
</template> 

<style lang="scss" scoped> 
    .poll-results-page {
        .poll-results-content {
            .search {
                input {
                    font-size: 20px;
                }
            }
        }

    }
</style>