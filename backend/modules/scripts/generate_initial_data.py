#
# :: generate_initial_data.py 
# Generate initial data for the database. 
# 
import utils.preloader

from modules.repositories.users import users 
from modules.repositories.polls import polls 
from modules.repositories.answers import answers 
from modules.common.data_generation \
    import generate_random_user 

# clear database
users.coll.drop() 
polls.coll.drop() 
answers.coll.drop()

# specify generation variables 
NO_OF_USERS = 1000 
NO_OF_POLLS = 3000
NO_OF_ANSWERS_PER_POLL = 150 

##################
# GENERATE USERS #
################## 
current_emails = set() 
current_mobile_nos = set() 
current_usernames = set() 

generated_users = 0 
generated_users_list = []

while generated_users < NO_OF_USERS:
    data = generate_random_user() 
    
    email = data["auth"]["email"]
    mobile_no = data["info"]["mobile_no"] 
    username = data["info"]["username"] 

    if email in current_emails:
        continue 

    if mobile_no in current_mobile_nos:
        continue 

    if username in current_usernames: 
        continue 

    current_emails.add(email)
    current_mobile_nos.add(mobile_no) 
    current_usernames.add(username)

    generated_users_list.append(data)
    
    generated_users += 1

users.coll.insert_many(generated_users_list)
 
##################
# GENERATE POSTS #
################## 
for i in range(NO_OF_POLLS): 
    