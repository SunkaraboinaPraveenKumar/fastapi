from database import User
from sqlalchemy.orm import Session

def create_user(db:Session,username:str,email:str):
    db_user = User(username=username,email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db:Session,username:str):
    return db.query(User).filter(User.username==username).first()


# Update operation
def update_user_email(db:Session, user_id:int,new_email:str):
    db_user =db.query(User).filter(User.id==user_id).first()

    if db_user:
        db_user.email=new_email
        db.commit()
        db.refresh(db_user)
    return db_user

# delete operation

def delete_user(db:Session,user_id:int):
    db_user = db.query(User).filter(User.id==user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
    
    return db_user