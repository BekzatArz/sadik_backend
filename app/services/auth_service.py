from app.models import User, Admin
from app.extensions import db

def create_user(data):
    user = User(first_name=data['first_name'], last_name=data['last_name'], phone_number=data['phone_number'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit() 
    return user

def create_admin(data):
    admin = Admin(company_name=data['company_name'], phone_number=data['phone_number'], email=data['email'])
    admin.set_password(data['password'])
    db.session.add(admin)
    db.session.commit()
    return admin