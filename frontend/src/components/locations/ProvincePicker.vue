
<script setup> 
    import { defineProps, onMounted, ref, watch, defineEmits } from "vue"
    import { Locations } from "@/utils/locations.js"

    const props = defineProps([ "region", "initial" ])
    const emit = defineEmits([ "change" ])

    const selectedProvince = ref(props.initial)

    const provincesList = ref([])   

    async function fetchProvinces() {
        provincesList.value = 
            await Locations.getProvincesOfRegion(props.region);
    }

    watch(() => props.region, async () => {
        await fetchProvinces()
    })

    onMounted(async () => {
        await fetchProvinces()
    })

</script> 

<template> 
    <div class="province-picker">
        <select 
            class="province"
            v-model="selectedProvince"
            @change="emit('change', selectedProvince)"
        >    
            <option
                v-for="province in provincesList"
                :key="province['key']" 
                :value="province['key']"
            >   
                {{ province["name"] }}
            </option> 
        </select>
    </div>
</template> 

<style lang="scss" scoped> 
    .province-picker {
        width: 100%;
    }
</style> 