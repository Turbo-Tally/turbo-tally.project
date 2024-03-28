<script setup> 

import { ref } from "vue"

const props = defineProps([ "itemsLength" ])
const emit = defineEmits([ "close" ])

const activePartition = ref(1)

function handleClickPartition(index) {
    if(index == activePartition.value) {
        activePartition.value = -1
    } else {
        activePartition.value = index
    }
}

</script> 

<template> 
    <div class="accordion"> 
        <div v-for="index in itemsLength" :class="'partition-' + index" :key="index">
            <div class="header" @click="handleClickPartition(index)"> 
                {{ activePartition == index ? "+" : "-" }} 
           
                <slot :name="'partition-' + index + '-title'" >
                    Partition {{ index }}
                </slot>
            </div>
            <div class="content" v-if="activePartition == index">
                <slot :name="'partition-' + index + '-content'" >

                </slot>
            </div>
        </div>
    </div> 
</template> 

<style lang="scss" scoped> 
    .header {
        margin-top: 5px;
        background-color: black; 
        border: 2px solid black; 
        color: white;
        font-weight: bold;
        padding: 5px 10px;
        cursor: pointer;
    }

    .header:hover {
        opacity: 0.8;
    }

    .content {
        border: 2px solid black;
        padding: 10px;
    }
</style> 