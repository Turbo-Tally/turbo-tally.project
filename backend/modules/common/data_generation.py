from faker import Faker 
from .locations import provinces, regions
import random
from .password_generation import random_password
from .formats import datetime_format
from datetime import datetime, date

from modules.main.auth import auth

faker = Faker()

region_keys = list(map(lambda x: x["key"], regions))
province_by_regions = {} 

for province in provinces:
    if province["region"] not in province_by_regions: 
        province_by_regions[province["region"]] = [] 
    province_by_regions[province["region"]].append(province["key"])

def generate_random_mobile_no(): 
    mobile_no = "09" 
    suffix = "" 
    for i in range(9): 
        suffix += str(random.randint(0, 9))
    return mobile_no + suffix


def generate_random_user():
    selected_region = random.choice(region_keys)
    selected_password = random_password(16)

    data = {
        "info" : {
            "gender" : random.choice(["M", "F"]), 
            "birthdate" : 
                datetime.strptime(
                    faker.date_of_birth(minimum_age=18, maximum_age=100)\
                         .strftime(datetime_format),
                    datetime_format
                ),
            "region" : selected_region, 
            "province" : random.choice(province_by_regions[selected_region]),
            "username" : faker.simple_profile()["username"],
            "mobile_no" : generate_random_mobile_no()
        },
        "auth" : {
            "email" : faker.ascii_email(), 
            "password" : selected_password, 
            "password_hash" : auth.hash(selected_password),
            "is_admin" : False, 
            "is_bot" : False
        },
        "created_at" : datetime.now()
    }
    
    return data
    
def generate_random_poll(**kwargs):
    n_choices = kwargs.get("n_choices", (4, 10))
    choices_count = random.randint(n_choices[0], n_choices[1])
    answer_date = faker.date_between(
        date(2022, 1, 1),
        date(2024, 1, 1)
    )

    data = { 
        "title" : faker.sentences(nb=1)[0][0:-1] + "?", 
        "choices" :     
            map(
                lambda x: x.upper(), 
                faker.words(nb=choices_count, unique=True)
            ), 
        "created_at" : datetime(
            answer_date.year,
            answer_date.month, 
            answer_date.day
        )
    }
    return data

