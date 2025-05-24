from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import User, get_db
from CRUD import create_user, get_user_by_username, update_user_email, delete_user

app = FastAPI()

@app.post("/users/")
def create_user_endpoint(username: str, email: str, db: Session = Depends(get_db)):
    return create_user(db=db, username=username, email=email)

@app.get("/users/{username}")
def read_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, new_email: str, db: Session = Depends(get_db)):
    user = update_user_email(db=db, user_id=user_id, new_email=new_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

# Add this block to run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("db_app:app", host="127.0.0.1", port=8000, reload=True)