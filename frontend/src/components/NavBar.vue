<script setup> 

</script> 

<template> 
    <div class="nav-bar-component"> 
        <div v-if="false" class="nav-bar-items"> 
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
            <div @click="$router.push('/logout')">LOGOUT</div>
        </div>
    </div>
</template> 

<style scoped lang="scss"> 
    .nav-bar-component {
        width: 100%; 
        display: flex;
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