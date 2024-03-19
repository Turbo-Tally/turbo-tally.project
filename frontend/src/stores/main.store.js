import { defineStore } from "pinia"

export const useMainStore = defineStore("mainStore", {

    persist: localStorage,

    state: () => ({
        _init: false 
    }), 

    getters: {

    }, 

    actions: {
        init() {
            this._init = true
        }
    }

})