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

    window.scansClient = scansClient;
})() 