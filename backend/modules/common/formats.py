from cerberus import schema_registry
from datetime import datetime
from modules.common.locations import regions, provinces

###########################
# Default Datetime Format #
###########################
datetime_format = "%Y-%m-%d %H:%M:%S"

#####################
# Custom Validators #
#####################

formats = {}

# username validator
formats["username"] =  {
    "type" : "string", 
    "minlength" : 3, 
    "maxlength" : 20, 
    "regex" : 
        "^[A-Za-z0-9\.\_]+$"
}

# email validator 
formats["email"] = {
    "type" : "string", 
    "minlength" : 4, 
    "maxlength" : 320, 
    "regex" :   
        "^\S+@\S+$" 
}

# password validator  
formats["password"] = {
    "type" : "string", 
    "minlength" : 8, 
    "maxlength" : 255,
    "allof" : [
        { 
            "type" : "string", 
            "regex" : ".*[0-9].*"
        },
        { 
            "type" : "string", 
            "regex" : ".*[A-Z].*"
        },
        { 
            "type" : "string", 
            "regex" : ".*[a-z].*"
        },
        { 
            "type" : "string", 
            "regex" : 
                ".*" +
                "[\~\!\@\#\$\%\^\&\*\(\)\_\+\`\\-\=\[\]\{\}\;\'\:\"\,\\.\/<\>\?]" +
                ".*"
        }
    ]
}

# datetime 
def check_datetime(field, value, error): 
    try: 
        datetime.strptime(value, datetime_format)
    except: 
        error(field, "Must be a valid datetime.") 


formats["datetime_str"] = {
    "type" : "string", 
    "check_with" : check_datetime
}

# gender 
formats["gender"] = {
    "type" : "string",
    "allowed" : ["M", "F"]
}

# regions 
formats["region"] = {
    "type" : "string", 
    "allowed" : list(map(lambda x: x["key"], regions))
}

# province 
formats["province"] = {
    "type" : "string", 
    "allowed" : list(map(lambda x: x["key"], provinces))
}

# PH mobile number 
formats["ph_mobile_no"] = {
    "type" : "string", 
    "minlength" : 11, 
    "maxlength" : 11, 
    "regex" : "09[0-9]{9}"
}

# verification code 
formats["verif_code"] = {
    "type" : "string", 
    "minlength" : 6, 
    "maxlength" : 6, 
    "regex" : "[0-9]{6}"
}

# poll title 
formats["poll_title"] = {
    "type" : "string", 
    "minlength" : 5, 
    "maxlength" : 256
}

# poll answer 
formats["poll_choice"] = {
    "type" : "string", 
    "minlength" : 1, 
    "maxlength" : 64 
} 


####################
# HELPER FUNCTIONS #
#################### 

def extend_format(dict_a, dict_b): 
    return dict(dict_a, **dict_b)

def require_all(dict_a, is_required = True): 
    dict_b = {} 
    for key in dict_a:
        dict_b[key] = dict_a[key] 
        dict_b[key]["required"] = is_required
    return dict_b

def is_province_allowed(region, province): 
    # get list of allowed province in region 
    def filter_fn(province_record): 
        return province_record["region"] == region

    allowed_provinces = \
        list(filter(filter_fn, provinces))
    allowed_province_keys = \
        list(map(lambda province: province["key"], allowed_provinces))

    return province in allowed_province_keys
