from app.models import User
from app.extensions import db

def get_user(user_id):
    return User.query.get(user_id)
