from modules.common.formats import formats, extend_format, require_all

schemas = {}

#
# Registration Input Schema
# 
schemas["registration_input"] = {
    "username"   : formats["username"],
    "email"      : formats["email"],  
    "password"   : formats["password"], 
    "birthdate"  : formats["datetime_str"], 
    "gender"     : formats["gender"], 
    "region"     : formats["region"], 
    "province"   : formats["province"],
    "mobile_no"  : formats["ph_mobile_no"], 
    "sms_code"   : formats["verif_code"], 
    "email_code" : formats["verif_code"], 

    "confirm_password" : { "type" : "string" }, 
    "privacy_policy" : { "type" : "boolean" }, 
    "terms_and_conditions" : { "type" : "boolean" }
}   

require_all(schemas["registration_input"])

#
# Update Info Schema 
# 
schemas["info_update_input"] = {
    "region"        : formats["region"], 
    "province"      : formats["province"], 
    "birthdate"     : formats["datetime_str"], 
    "gender"        : formats["gender"]
}

require_all(schemas["info_update_input"], False)