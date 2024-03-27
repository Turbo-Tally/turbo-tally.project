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

    static async getResults(pollId) {
        const endpoint = "/analysis/polls/" + pollId 
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

    static async getNormalizedResults(pollId) {
        let results = await Poll.getResults(pollId)

        // get total per day answers 
        const per_day_answers = results["per_day_answers"]
        results["total_per_day_answers"] = []
        
        let total = 0;
        for(let i = 0; i < per_day_answers.length; i++) {
            total += per_day_answers[i]["answer_count"]
            const id = per_day_answers[i]["_id"]
            results["total_per_day_answers"].push(
                { "_id" : id, "answer_count" : total }
            )
        }

        // normalize province names 
        const provinceMap = {} 

        for(let province of Locations.provinces) {
            provinceMap[province.key] = province.name 
        }

        // revalue provinces 
        results["all_answers"]["by_province"] = Helpers.revalue(
            results["all_answers"]["by_province"],
            provinceMap,  
            "_id"
        )

        results["by_category"]["stacked_by_province"].forEach((value, index) => {
            results["by_category"]["stacked_by_province"][index]["_id"]["province"] = 
                provinceMap[value["_id"]["province"]]
        })

        console.log(results)


        return results
    }
}