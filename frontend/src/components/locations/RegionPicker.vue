<script setup> 
    import { defineProps, onMounted, ref, watch, defineEmits } from "vue"
    import { Locations } from "@/utils/locations.js"

    const props = defineProps([ "initial" ])
    const emit = defineEmits([ "change" ])

    const selectedRegion = ref(props.initial)

    const regionsList = ref([])

    onMounted(async () => {
        regionsList.value = await Locations.getRegions();
    })

</script> 

<template> 
    <div class="region-picker">
        <select 
            class="region" 
            v-model="selectedRegion"
            @change="emit('change', selectedRegion)"
        >    
            <option 
                v-for="region in regionsList"
                :key="region['key']"
                :value="region['key']"
            >
                {{ region.key}} - {{ region.long }}
            </option> 
        </select>
    </div>
</template> 

<style lang="scss" scoped> 

</style> 