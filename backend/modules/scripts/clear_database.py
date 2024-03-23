
from modules.repositories.users import users 
from modules.repositories.polls import polls 
from modules.repositories.answers import answers 
from modules.repositories.choices import choices
from modules.repositories.auto_increments import auto_increments

def clear_database():
    auto_increments.coll.drop()
    users.coll.drop() 
    polls.coll.drop() 
    answers.coll.drop()
    choices.coll.drop()