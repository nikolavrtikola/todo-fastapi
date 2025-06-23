from sqlalchemy import Boolean,Integer,String,Column,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(255),unique=True,index=True)
    username = Column(String(45),unique=True,index=True)
    first_name = Column(String(45))
    last_name = Column(String(45))
    hashed_password = Column(String(200))
    is_active = Column(Boolean,default=True)
    phone_number = Column(String)
    address_id = Column(Integer,ForeignKey("address.id"))
    

    todos = relationship("Todos",back_populates="owner")
    address = relationship("Address",back_populates="user_address")

class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(200))
    description = Column(String(200))
    priority = Column(Integer)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("Users",back_populates="todos")

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer,primary_key=True,index=True)
    address_1 = Column(String)
    address_2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    apt_num = Column(Integer)
   
    

    user_address = relationship("Users",back_populates="address")
    
