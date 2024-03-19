import Axios from "axios"

export const httpClient = 
    Axios.create({
        baseURL: "http://172.28.2.3:80", 
        withCredentials: true
    })

async function testPing() {
    const response = await httpClient.get("/ping") 
    console.log(
        "> HTTP Client : Received message from server -> " + response.data + "."
    )
} 

await testPing()

window.httpClient = httpClient