import { httpClient } from "./http-client.js"

export class User 
{
    static async data() {
        const response = await httpClient.get("/auth/user")
        const data = response.data.data 
        return data
    }
}