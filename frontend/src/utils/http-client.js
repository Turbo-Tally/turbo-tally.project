import Axios from "axios"

Axios.defaults.withCredentials = true

export const httpClient = 
    Axios.create({
        baseURL: "http://localhost:30001"
    })

async function testPing() {
    const response = await httpClient.get("/ping") 
    console.log(
        "> HTTP Client : Received message from server -> " + response.data + "."
    )
} 

async function getSessionId() {
    console.log("> Fetching Session ID...")
    const response = await httpClient.get("/auth/session-id", {
        withCredentials: true
    }) 
    console.log("> Session ID fetched...")
}

// test POST data 
await httpClient.post("/auth/sign-up", {
    "foo" : "bar"
})


await testPing()
await getSessionId()

window.httpClient = httpClient