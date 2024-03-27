<script setup> 

const props = defineProps([ "title", "width" ])
const emit = defineEmits([ "close" ])

</script> 

<template> 
    <div class="modal">
        <div class="modal-dimmer">
        </div>
        <div class="modal-content">
            <div class="header">
                <div class="title"> 
                    <div class="text">
                        {{ props.title }}
                    </div> 
                </div> 
                <div class="close">
                    <div class="close-icon" @click="emit('close')"> 
                        X
                    </div> 
                </div> 
            </div> 
            <div class="content">
                <div class="main-content"  :style="{ 'width' : props.width + 'px' }">
                    <slot />
                </div> 
            </div> 
        </div>
    </div>
</template> 

<style lang="scss" scoped> 
    .modal {
        z-index: 100;
    }

    .modal-dimmer {
        background-color: black; 
        opacity: 0.9; 
        z-index: 100;
        position: fixed; 
        top: 0px; 
        left: 0px; 
        width: 100%; 
        height: 100%;   
    }

    .modal-content {
        background-color: white;
        z-index: 100;
        position: fixed; 
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        min-height: 200px;
        width: 760px;
       
        
        .header {
            display: flex; 
            max-height: 300px; 
            overflow-y: scroll;
            width: 760px;

            .title {
                flex: 1;
                padding: 10px;
                background-color: rgb(234, 234, 234);

                .text {
                    margin-top: -3.5px;
                    font-weight: bold;
                }
            }

            .close {
                width: 30px;
                text-align: center;
                display: flex; 
                align-items: center;
                justify-content: center;
                background-color: none;
                cursor: pointer;

                .close-icon {
                    padding: 5px 10px;
                    margin: 5px;
                    background-color: red;
                    color: white;
                    height: 16px;
                    width: 20px;
                    font-weight: bold; 
                }

            }
            
            .close:hover {
                opacity: 0.8;
            }
        }


        .content {
            margin: 10px;
            text-align: center;
            overflow-y: scroll; 
            max-height: 500px;

            .main-content {
                margin: 0 auto;
            }
        }
    }
</style> 