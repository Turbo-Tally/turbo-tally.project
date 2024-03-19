import { io } from "socket.io-client" 

export const wsClient = io("ws://172.28.2.3:80");

wsClient.on("connect", () => {
    console.log("> WS Client : Connected to back-end server.")
})

wsClient.on("disconnect", () => {
    console.log("> WS Client : Disconnected from back-end server.")
})

wsClient.on("reconnect", () => {
    console.log("> WS Client : Reconnected to back-end server.")
})

wsClient.on("reconnect_attempt", () => {
    console.log("> WS Client : Reconnecting to back-end server...")
})

window.wsClient = wsClient;