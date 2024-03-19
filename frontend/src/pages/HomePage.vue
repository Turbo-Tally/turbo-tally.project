<script setup> 

import DefaultLayout from "../layouts/DefaultLayout.vue"

import StatCard from "@/components/StatCard.vue"
import EventReel from "@/components/EventReel.vue"

</script> 

<template> 
    <div class="home-page"> 
        <DefaultLayout>
            <div class="general-stats"> 
                <div class="total-no-of-polls">
                    <StatCard 
                        title="Total No. of Polls" 
                        value="1.0K"
                    />
                </div> 
                <div class="total-no-of-answerees"> 
                    <StatCard 
                        title="Total No. of Answerees" 
                        value="1.0K"
                    />
                </div> 
                <div class="average-answerees-per-post"> 
                    <StatCard 
                        title="Average Answerees per Post" 
                        value="1.0K"
                    />
                </div> 
            </div> 
            <div class="center-label">
                Join other people who vote in real time...
            </div>
            <div class="event-reel">
                <EventReel />
            </div>
        </DefaultLayout>
    </div> 
</template> 

<style lang="scss"> 
    .home-page {

        .general-stats {
            display: flex; 
            gap: 20px;

            > div {
                flex: 1;
            }
        }

        .center-label {
            margin-top: 20px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .event-reel {
            margin-top: 20px;
        }

    }

</style>