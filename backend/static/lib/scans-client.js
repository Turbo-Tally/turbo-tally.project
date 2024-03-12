/** 
 * Dependencies (Socket.IO)
 */

(() => {
    class SCANSClient 
    {
        constructor(io) {
            this.taskId = null
            
            this.streamIds = [] 
            this.streamMetas = {} 
            this.streamReports = {} 

            this.io = io
            this.socket = null
        }

        async load(taskId) {
            console.log("@ Loading task id `" + taskId + "`")

            // save to task id 
            this.taskId = taskId 
            
            // get task info 
            console.log("@ Getting task information...")
            const response = 
                await fetch(`/tasks/${taskId}/info`) 
            const taskInfo = 
                await response.json() 

            // save stream ids 
            console.log("@ Saving Stream IDs: ", taskInfo.stream_ids)
            this.streamIds = taskInfo.stream_ids
            
            // run task hook 
            await this.onTaskPreloaded(taskInfo)

            // load stream metas
            await this.preloadStreams()

            // connect 
            await this.connect()
        }

        async new(streamIds) {
            // save to stream ids 
            this.streamIds = streamIds 
            
            // submit task for analysis 
            console.log("@ Submitting task for analysis...")
            console.log(`@ Stream IDs : ${streamIds.join(", ")}`)

            const streamIdsStr = this.streamIds.join(",")
            const response = 
                await fetch(`/tasks/new?stream_ids=${streamIdsStr}`)
            const taskInfo = 
                await response.json()

            // save task id 
            console.log("@ Determined `task_id` : " + taskInfo.task_id)
            this.taskId = taskInfo.task_id 

            // run task hook
            await this.onTaskPreloaded(taskInfo)

            // load stream metas
            await this.preloadStreams()

            // connect 
            await this.connect()
        }

        async preloadStreams() {
            console.log("@ Preloading Stream Metas...")
            
            const length = this.streamIds.length; 
             
            let index = 1; 
            for(let streamId of this.streamIds) {
                console.log("@ Preloading Stream ID :", streamId)

                const streamInfo = 
                    await (await fetch(`/streams/${streamId}/info`)).json()
                
                // get stream meta 
                this.streamMetas[streamId] = streamInfo._meta 
                
                // get stream reports 
                this.streamReports[streamId] = streamInfo.report
                console.log("\tStream ID [" + streamId + "] :", streamInfo)

                // run stream hook
                await this.onStreamPreloaded(streamInfo, index, length)

                index += 1
            }
        }

        async connect() {
            console.log("@ Connecting to WebSocket server...")
            const socket = this.io("/", {
                query: {
                    "task_id" : this.taskId
                }
            });

            this.socket = socket; 
         
            socket.on("connect", () => {
                console.log("\tConnected to WebSocket server.")
            })

            socket.on("disconnect", () => {
                console.log("@ Disconnected from WebSocket server.")
            })

            socket.on("reconnect_attempt", () => {
                console.log("\tReconnecting to WebSocket server...")
            })
        }

        /** 
         * Event Hooks 
         */

        /**
         * Run hook when task information has been loaded.
         */
        async onTaskPreloaded(taskInfo) {
            
        }

        /**
         * Run hook when stream has been preloaded
         */
        async onStreamPreloaded(streamInfo, index, length) {

        }

    }

    window.SCANSClient = SCANSClient;
})()