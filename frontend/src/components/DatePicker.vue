<script setup> 
    import { defineProps, onMounted, ref, watch, defineEmits } from "vue"

    const emit = defineEmits([ "change" ])

    const birthdate = ref();

    watch(birthdate, () => {
        emit("change", birthdate.value)
    })

</script> 

<template> 
    <div class="datepicker">
        <input 
            type="date" 
            v-model="birthdate"
        />
    </div>
</template> 

<style lang="scss" scoped> 
    .datepicker {
        > input {
            width: 100%;
            background-color: rgb(234, 234, 234);
            border: 1px solid grey; 
            border-radius: 5px;
            padding: 5px 0px;
            font-size: 16px;
            text-align: center;
        }
    }
</style> 