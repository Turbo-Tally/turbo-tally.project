
## variables 

```json
[
    {
        "_id"           : ObjectId,
        "key"           : string (index, alphanumeric), 
        "value"         : any
    },
    ...
]
```

## users 
```json
[
    {
        "user_id"           : integer (index), 
        "info" : {
            "email"             : string (email),
            "password"          : string (strong password),   # dev only field
            "password_hash"     : string (hashed password), 
            "birthdate"         : Date, 
            "gender"            : string (M | F), 
            "region_key"        : string, 
            "province_key"      : string,
        }, 
        "history" : {
            "login_count"           : integer, 
            "failed_login_count"    : integer
        }, 
        "answers" : [
            { 
                "question" : Reference to Question, 
                "answer"   : Reference to Answer
            }
        ]
    },
    ...
]
```

## questions 
``json
[
    {
        "question_id" : integer (index), 
        "asker_id" : Reference to User
        "info" : {
            "title" : string,
            "choices" : [... array of string choices ...],  
        },
        "asked_at" : timestamp   
    }
]
```

