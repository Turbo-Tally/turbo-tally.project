Here is the format of a regular report from the analyzer. 

```json
{
    "stream_id" : "<stream-id>", 
    "results" : {
        "earnings_breakdown" : {
            "by_currency" : {
                "PHP" : 0.0, 
                "USD" : 0.0, 
                ... (all currencies are listed)
            }, 
            "by_author" : [
               { "id" : "<author_id>", "amount" : 100.0 }, 
               { "id" : "<author_id>", "amount" :  50.0 }, 
               ... (top 10 are listed), 
               { "id" : "top-10-50", "amount" : 200.0 }, 
               { "id" : "top-51-100", "amount" : 300.0 }, 
               { "id" : "top-101-above", "amount" : 400.0 }
            ],  
            "by_tier" : {
                "tier-a" : 0.0, 
                "tier-b" : 0.0, 
                ... (all tiers are listed)
            }
        },
        "message-flow" : [
            10,   // first minute
            5,    // second minute
            8,    // third minute 
            ... 
            10    // last minute 
        ], 
        "earnings-flow" : [
            10.00,     // first minute
            0.00,      // second minute 
            12.00,     // third minute
            ...,   
            10         // last minute    
        ]
    }
}
```