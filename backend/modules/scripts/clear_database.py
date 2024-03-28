from mdoules.core.database import db

def clear_database():
    db.drop_database()