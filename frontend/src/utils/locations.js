import { httpClient } from "@/utils/http-client.js" 

export class Locations 
{
    static async getRegions() {
        const regionsResponse = await httpClient.get("/common/regions") 
        const regionsData = regionsResponse.data
        return regionsData
    }

    static async getProvincesOfRegion(regionId) {
        const endpoint =  "/common/region/" + regionId + "/provinces"
        const provincesResponse = await httpClient.get(endpoint) 
        const provincesData = provincesResponse.data 
        return provincesData
    }
}