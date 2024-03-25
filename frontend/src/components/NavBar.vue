<script setup> 
    import { useMainStore } from "@/stores/main.store.js"
    import { httpClient } from "@/utils/http-client.js"
    import { useRouter } from 'vue-router'

    const mainStore = useMainStore();
    const router = useRouter()

    async function handleLogOut() {
        const response = await httpClient.get("/auth/log-out")
        const data = response.data 
        
        if(data["status"] == "LOGGED_OUT") {
            mainStore.logOut()
            router.push("/")
        }
    }

</script> 

<template> 
    <div class="nav-bar-component">

   

        <div v-if="!mainStore.isLoggedIn" class="nav-bar-items"> 
            <div @click="$router.push('/')">HOME</div>
            <div @click="$router.push('/polls')">POLLS</div> 
            <div @click="$router.push('/sign-up')">SIGN UP</div>
            <div @click="$router.push('/log-in')">LOG IN</div>
        </div>

        <div v-else class="nav-bar-items"> 
            <div @click="$router.push('/')">HOME</div>
            <div @click="$router.push('/polls')">POLLS</div> 
            <div @click="$router.push('/dashboard')">DASHBOARD</div>
            <div @click="$router.push('/account')">ACCOUNT</div>
            <div @click="handleLogOut()">LOGOUT</div>
        </div>

    </div>
</template> 

<style scoped lang="scss"> 
    .nav-bar-component {
        margin-top: 20px;
        width: 100%; 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        .nav-bar-items {
            margin-top: 20px;
            display: flex;

            div {
                padding: 10px 35px;
            }

            div:hover {
                opacity: 0.8;
                background-color: black;
                color: white;
                cursor: pointer;
            }

            div:active {
                background-color: rgb(50, 50, 50);
            }
        }

    }
</style>