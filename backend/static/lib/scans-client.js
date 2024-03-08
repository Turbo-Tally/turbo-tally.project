/** 
 * Dependencies (Socket.IO)
 */

(() => {
    console.log("Hello, world! - from scans-client.")

    class SCANSClient 
    {
        constructor(
            streamIds = [],
            {
                baseURL = "", 
                port = "80", 
                wsScheme = "ws",
                httpScheme = "http",
                connectSelf = false
            } = {}
        ) {
            
            this.baseURL = baseURL
            this.port = port
            this.wsScheme = wsScheme
            this.httpScheme = httpScheme
            this.streamIds = streamIds
            this.connectSelf = connectSelf 
            this.joined = {}
            this.noOfRooms = this.streamIds.length + 1

            this.io = this.createWsConnection()
            this.setup()
        }

        /**
         * Create websocket connection
         */
        createWsConnection() {
            let url = this.makeWsConnectionUrl();
            console.log(`> Connecting to WebSockers server in [${url}]...`)
            return io(url)
        }
        
        /** Connection URLS */
        makeWsConnectionUrl() {
            // create connection url
            let connectionURL = 
                this.wsScheme + "://" +
                this.baseURL + ":" + 
                this.port; 
            return connectionURL;    
        }

        makeHttpBaseUrl() {
            if(this.connectSelf == false) {
                // create connection url 
                let connectionURL = 
                    this.httpScheme + "://" + 
                    this.baseURL + ":" + 
                    this.port;
                return connectionURL;
            } else {
                return ""
            }
        }

        makeHttpAnalyzeUrl(streamIds) {
            let baseURL = this.makeHttpBaseUrl();
            let streamIdsPart = streamIds.join(",");
            let url = baseURL + "/analyze?streams=" + streamIdsPart  
            return url;
        }

        /**
         * Analyze stream ids.
         */
        async analyze() {
            /**
             * Store stream id.
             */
            let streamIds = this.streamIds
            
            /** 
             * Submit task for analysis. 
             */
            const url = this.makeHttpAnalyzeUrl(streamIds)
            console.log(`> Submitting analysis task with [${url}]`)

            const response = await fetch(url) 
            const result = await response.json() 

            console.log("> Received response from /analyze : ", result)

            return result
        }

        setup() {
            let self = this
           
            this.io.on("connect", (socket) => {
                (async () => {
                    self.onConnected(socket)
                })()
            })

            this.io.on("reconnect_attempt", () => {
                self.joined = {}
            })

            this.io.on("joined_room", (data) => {
                console.log(`> Joined room [${data}]`)
                self.joined[data] = true;
            })
        }

        getJoinList(results) {
            let joinList = [] 
            joinList.push("task." + results.task_id)
            for(let streamId of results.stream_ids)
                joinList.push("stream." + streamId)  
            return joinList
        }

   
        async onConnected(socket) {
            
            // send instruction to analyze streams
            const results = await this.analyze()
            console.log("> Connected to WebSockets server...")

            // join relevant rooms
            const joinList = this.getJoinList(results);
            console.log("> Joining server-side rooms:", joinList)
            
            const joined = this.joined; 
            const self = this
            let joinCount = 0
            
            const joinInterval = setInterval(() => {
                for(let joinItem of joinList) {
                    if(!(joinItem in joined)) {
                        console.log(
                            `> Joining room ` +
                            `(${joinCount + 1}/${self.noOfRooms})` +
                            `[${joinItem}]`)
                        self.io.emit("join_room", joinItem) 
                        joinCount += 1
                    }
                }
            }, 3000)
        }
    }

    window.SCANSClient = SCANSClient

})()