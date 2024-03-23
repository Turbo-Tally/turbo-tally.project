#
# :: generate_initial_data.py 
# Generate initial data for the database. 
# 
import random 

from utils.preloader import preload_default

from modules.repositories.users import users 
from modules.repositories.polls import polls 
from modules.repositories.answers import answers 
from modules.repositories.choices import choices
from modules.repositories.auto_increments import auto_increments

from modules.common.data_generation import \
    generate_random_user, generate_random_poll, generate_random_answer

from modules.main.voting import Voting

from time import sleep

# specify generation variables 
NO_OF_USERS = 300 
NO_OF_POLLS = 1000
NO_OF_CHOICES_PER_POLL = (4, 10)
NO_ANSWERS_PER_POLL = (50, 150)

def generate(): 
    generate_users()
    generate_polls() 
    generate_answers()

##################
# GENERATE USERS #
################## 
def generate_users(): 
    print("> Generating users...")

    users.coll.drop() 

    preload_default()

    current_emails = set() 
    current_mobile_nos = set() 
    current_usernames = set() 

    generated_users = 0 
    generated_users_list = []

    while generated_users < NO_OF_USERS:
        print(f"\t| Generating user {generated_users} of {NO_OF_USERS}")
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

        data["_id"] = users.next_id()

        generated_users_list.append(data)
        
        generated_users += 1

    print("\t| Inserting users to database.")
    users.coll.insert_many(generated_users_list)
 
##################
# GENERATE POLLS #
################## 
def generate_polls():
    print("> Generating polls...")

    polls.coll.drop() 
    answers.coll.drop() 
    choices.coll.drop() 

    preload_default()

    user_pool = list(users.coll.find({})) 
   
    for i in range(NO_OF_POLLS):
        print(f"\t| Creating poll {i + 1} of {NO_OF_POLLS}")
        random_user = random.choice(user_pool)
        random_poll = generate_random_poll(n_choices=NO_OF_CHOICES_PER_POLL)
        Voting.create_poll(random_user, random_poll)

####################
# GENERATE ANSWERS #
####################
def generate_answers(): 
    print("> Generating answers...") 

    poll_pool = list(polls.coll.find({}))
    user_pool = list(users.coll.find({}))
    
    n_polls = len(poll_pool)
    n_users = len(user_pool)

    answers.coll.drop()

    answers_list = []

    for i in range(n_polls): 

        print(f"\t| Generating answers for poll {i + 1} of {n_polls}")
        random_poll = poll_pool[i]
        n_answers = \
            random.randint(NO_ANSWERS_PER_POLL[0], NO_ANSWERS_PER_POLL[1])
        random_users = random.sample(user_pool, n_answers)
        poll_choices = \
            list(choices.coll.find({ "poll.$id" : random_poll["_id"]}))


        for j in range(n_answers): 
            print(f"\t| Generating {j + 1} of {n_answers} answers for poll {i + 1}")
            answers_list.append({
                "poll" : {
                    "$ref" : "polls", 
                    "$id" : random_poll["_id"]
                },
                "user" : {
                    "$ref" : "users", 
                    "$id" : random_users[j]["_id"]
                }, 
                "answer" : random.choice(poll_choices)["answer"]
            })

            polls.coll.update_one(
                { "_id" : random_poll["_id"] }, 
                { "$set" : { "meta.no_of_answers" : n_answers }}
            )

    answers.coll.insert_many(answers_list)

#################
# RUN GENERATOR #
#################
generate()

