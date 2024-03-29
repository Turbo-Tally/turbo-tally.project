import { Helpers } from "./helpers.js" 
import { Locations } from "./locations.js"

export class Poll 
{
    static async getInfo(pollId) {
        const endpoint = "/voting/polls/" + pollId + "/info"
        const response = await httpClient.get(endpoint) 
        const data = response.data 
        return data
    }

    static async getChoices(pollId, q = "", cursor = -1) {
        const endpoint = "/voting/polls/" + pollId + "/find-choices" 
        const response = await httpClient.get(endpoint, {
            params : {
                q : q,
                cursor : cursor
            }
        })
        const data = response.data 
        return data
    }

    static async answer(pollId, answer) {
        const endpoint = "/voting/polls/" + pollId + "/answer" 
        const response = await httpClient.post(endpoint, {
            answer: answer
        })
        const data = response.data 
        return data
    }

    static async hasAnswered(pollId) {
        const endpoint = "/voting/has-answered/" + pollId 
        const response = await httpClient.get(endpoint)
        const data = response.data 
        return data["status"] == "ALREADY_ANSWERED"
    }

    static async getResults(pollId, endpoint, args) {
        return await httpClient.get(`/analysis/${pollId}/${endpoint}`, {
            params: args
        })
    }
}
