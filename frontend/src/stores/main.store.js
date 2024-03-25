import { defineStore } from "pinia"

export const useMainStore = defineStore("mainStore", {

    persist: {
        store: localStorage
    },

    state: () => ({
        _init: false, 
        isLoggedIn : false
    }), 

    getters: {

    }, 

    actions: {
        init() {
            this._init = true
        }, 

        logIn() {
            this.isLoggedIn = true 
        },

        logOut() {
            this.isLoggedIn = false
        }
    }

})