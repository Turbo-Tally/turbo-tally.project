import { io } from "socket.io-client" 

export const wsClient = io("ws://localhost:30001");

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

export function joinRoom(roomId) {
    wsClient.emit("join", roomId)
}

export function leaveRoom(roomId) {
    wsClient.emit("leave", roomId)
}

window.wsClient = wsClient;