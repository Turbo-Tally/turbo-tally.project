<script setup> 
    import { defineProps, onMounted, ref, watch, defineEmits } from "vue"
    import { Helpers } from "@/utils/helpers.js"

    const props = defineProps([ "value" ])
    const emit = defineEmits([ "change" ])
    const value = ref(props.value)

</script> 

<template> 
    <div class="choice-item">
        <input
            v-model="value"
            @change="$emit('change', value)"  
            placeholder="Click to edit choice..." 
        />
    </div>
</template> 

<style lang="scss" scoped> 
    .choice-item {
        > input { 
            background: none;
            padding: 5px 10px;
            border: none;
            background-color: white;
            width: 96%;
            font-size: 16px;
            outline: none;
            text-transform: uppercase;
        }
    }
</style> 