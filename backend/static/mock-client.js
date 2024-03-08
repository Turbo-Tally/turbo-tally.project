/** 
 * Mock Client
 */


(() => {
    const scansClient = 
        new SCANSClient(
            [
                "VRBfUcbmYZA",
                "8K7dHdcGhwo",
                "AhM-PEO65Zw"
            ], 
            {
                connectSelf : true
            }
        ); 

    scansClient.onRetrievedVideoInfos = (infos) => {
        /**
         * Process retrieved video information.
         */
    }

    window.scansClient = scansClient;
})() 