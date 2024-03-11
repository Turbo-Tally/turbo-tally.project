/** 
 * Dependencies (Socket.IO)
 */

(() => {
    class SCANSClient 
    {
        constructor() {
            this.taskId = null
            this.streamIds = [] 
            this.streamMetas = {} 
        }

        async load(taskId) {
            console.log("@ Loading task id [" + taskId + "]")

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

            // load stream metas
            await this.loadStreamMetas()
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
            this.taskId = taskInfo.task_id 

            // load stream metas
            await this.loadStreamMetas()
        }

        async loadStreamMetas() {
            console.log("@ Loading Stream Metas...")
            for(let streamId of this.streamIds) {
                console.log("@ Loading metadata of Stream ID :", streamId)
                this.streamMetas[streamId] = 
                    await (await fetch(`/streams/${streamId}/info`)).json()
                console.log(
                    "\tStream ID [" + streamId + "] :",
                    this.streamMetas[streamId]
                )
            }
        }
    }

    window.SCANSClient = SCANSClient;
})()