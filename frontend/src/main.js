import { createApp } from 'vue'

import './style.css'
import App from './App.vue'

// import setup functions 
import { setupRouter } from "./plugins/router"
import { setupPinia } from "./plugins/pinia" 

// create app 
const app = createApp(App)

// load vue-router 
app.use(setupRouter())

// load pinia 
app.use(setupPinia())

// load axios (http-client)
import "./utils/http-client"

// lock socket-io (ws-client)
import "./utils/ws-client"

// initialize app's store 
import { useMainStore } from './stores/main.store'
useMainStore().init()

// mount app 
app.mount("#app") 

// show store
window.showStore = () => {
    const storeData = localStorage.getItem("mainStore");
    const store = JSON.parse(storeData);
    console.log(store) 
}