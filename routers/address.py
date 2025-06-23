import sys
sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException,APIRouter
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from pydantic import BaseModel


router = APIRouter(
   prefix="/address",
   tags=["address"],
   responses={404:{"description":"Address not Found"}}
)

def get_db():
    try:
     db = SessionLocal()
     yield db
    finally:
       db.close()

class Address(BaseModel):
   address_1: str
   address_2: str
   city: str
   state:str
   country:str
   postal_code:str
   apt_num : Optional[int]

@router.post("/")
async def create_address(address: Address,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
   if user is None:
      raise get_user_exeption()
   address_model = models.Address()
   address_model.address_1 = address.address_1
   address_model.address_2 = address.address_2
   address_model.city = address.city
   address_model.state = address.city
   address_model.country = address.country
   address_model.postal_code = address.postal_code
   address_model.apt_num = address.apt_num

   db.add(address_model)
   db.flush()
   user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
   user_model.address_id = address_model.id
   db.add(user_model)
   db.commit()

