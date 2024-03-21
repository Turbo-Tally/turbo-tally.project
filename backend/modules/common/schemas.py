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
    "email_code" : formats["verif_code"]
}   

require_all(schemas["registration_input"])