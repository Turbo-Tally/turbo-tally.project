<script setup> 

import { ref } from "vue"

const props = defineProps([ "itemsLength", "loading" ])
const emit = defineEmits([ "onClose", "onExpand" ])

const activePartition = ref(1)

function handleClickPartition(index) {
    emit("onClose", activePartition.value)
    if(index == activePartition.value) {
        activePartition.value = -1
    } else {
        activePartition.value = index
        emit("onExpand", activePartition.value)
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
            <div class="content" v-if="!props.loading && activePartition == index">
                <slot :name="'partition-' + index + '-content'" >

                </slot>
            </div>
            <div class="content loading" v-else-if="activePartition == index"> 
                Loading...
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
        padding: 50px 0px;
        display: flex; 
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .loading {
        display: flex; 
        justify-content: center;
        align-items: center;
    }
</style> 