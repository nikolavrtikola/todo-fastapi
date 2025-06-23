import sys 
sys.path.append("..")

from fastapi import APIRouter,Depends
import models
from .auth import get_current_user,verify_password,get_password_ghash 
from pydantic import BaseModel
from database import SessionLocal,engine
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404:{"description":"Not Found"}}
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str

@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.get("/user/{user_id}")
async def get_user_path(user_id: int,db:Session=Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid User_id"

@router.get("/user/")
async def get_user_by_query(user_id:int,db:Session=Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None:
        return user_model
    return "Invalid user_id"

@router.put("/user/password")
async def change_user_password(user_verification: UserVerification,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exeption()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(user_verification.password,user_model.hashed_password):
            user_model.hashed_password = get_password_ghash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "Sucessfull password change!!!"
    return "Invalid User or request!!!"

@router.delete("/user")
async def delete_user(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):

    if user is None:
        raise get_user_exeption()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        return "Invalid User or request"
    
    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    db.commit()
    return "Delete Succesfull!!!"
