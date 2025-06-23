import sys
sys.path.append("..")
from starlette import status
from starlette.responses import RedirectResponse

from typing import Optional
from fastapi import Depends, Form, HTTPException,APIRouter,Request
from pydantic import BaseModel,Field
import models
from .auth import get_current_user
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
   prefix="/todos",
   tags=["todos"],
   responses={404:{"description":"ToDo not Found"}}
)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    try:
     db = SessionLocal()
     yield db
    finally:
       db.close()

@router.get("/",response_class=HTMLResponse)
async def get_all_by_user(request:Request,db:Session=Depends(get_db)):
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
   

   todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()
   return templates.TemplateResponse("home.html",{"request":request,"todos":todos,"user":user})

@router.get("/add-todo",response_class=HTMLResponse)
async def add_todo(request:Request):
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
   return templates.TemplateResponse("add-todo.html",{"request":request,"user":user})

@router.post("/add-todo",response_class=HTMLResponse)
async def create_new_todo(request:Request,
                          title: str= Form(...),
                          description:str =Form(...),
                          priority: int=Form(...),
                          complete:bool=False,
                          db:Session=Depends(get_db)):
   
   ## Check If the uswer is Autheticayed
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
   
   todo_model = models.Todos()
   todo_model.title = title
   todo_model.description = description
   todo_model.priority = priority
   todo_model.complete = complete
   todo_model.owner_id = user.get("id")
   db.add(todo_model)
   db.commit()
   return RedirectResponse(url="/todos/",status_code=status.HTTP_302_FOUND)
 


@router.get("/edit-todo/{todo_id}",response_class=HTMLResponse)
async def edit_todo(request:Request,todo_id:int,db: Session=Depends(get_db)):
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
   
   todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

   return templates.TemplateResponse("edit-todo.html",{"request":request,"todo":todo,"user":user})

@router.post("/edit-todo/{todo_id}",response_class=HTMLResponse)
async def commit_edit_todo(request:Request,todo_id:int,
                           db:Session=Depends(get_db),
                           title:str=Form(...),
                           description:str=Form(...),
                           priority:str=Form(...),
                           complete:bool=Form(...)
                           ):
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
   todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
   todo_model.title = title
   todo_model.description = description
   todo_model.priority = priority
   todo_model.complete = complete
   db.add(todo_model)
   db.commit()
   return RedirectResponse(url="/todos/",status_code=status.HTTP_302_FOUND)

@router.get("/delete/{todo_id}")
async def delete_todo(request:Request,todo_id:int,db:Session=Depends(get_db)):
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
   
   todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
   .filter(models.Todos.owner_id == user.get("id")).first()
   
   if todo_model is None:
      return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)
   db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
   db.commit()
   return RedirectResponse(url="/todos/",status_code=status.HTTP_302_FOUND)

@router.get("/complete/{todo_id}",response_class=HTMLResponse)
async def complete_todo(request:Request,todo_id:int,db:Session=Depends(get_db)):
   user = await get_current_user(request)
   if user is None:
      return RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
   todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
   todo.complete = not todo.complete
   db.add(todo)
   db.commit()

   return RedirectResponse(url="/todos/",status_code=status.HTTP_302_FOUND)




######################################################################################################

# class Todo(BaseModel):
#    title: str
#    description: Optional[str]
#    priority: int = Field(lt=6,gt=0,description="The priority must be between 1-5")
#    complete: bool = Field(default=False)


# @router.get("/test")
# async def test(request:Request):
#    return templates.TemplateResponse("home.html",{"request":request})


# @router.get("/")
# async def read_all_todos(db: Session = Depends(get_db)):
#     return db.query(models.Todos).all() 


# @router.get("/user")
# async def read_all_by_user(user: dict = Depends(get_current_user),db:Session= Depends(get_db)):
#    if user is None:
#       raise get_user_exeption()
#    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()
   


# @router.get('/{my_id}')
# async def get_todo_by_id(my_id: int,user: dict= Depends(get_current_user),db: Session = Depends(get_db)):
    
#     if user is None:
#        get_user_exeption()

#     todo_model = db.query(models.Todos)\
#       .filter(models.Todos.id == my_id)\
#       .filter(models.Todos.owner_id == user.get("id"))\
#       .first()
    
#     if todo_model is not None:
#         return todo_model
#     raise raise_HTTPException()

# @router.post("/")
# async def create_Todo(todo: Todo,user: dict=Depends(get_current_user),db: Session = Depends(get_db)):
   
#    todo_model = models.Todos()
   
#    todo_model.title = todo.title
#    todo_model.description = todo.description
#    todo_model.priority = todo.priority
#    todo_model.complete = todo.complete
#    todo_model.owner_id = user.get("id")
   
#    db.add(todo_model)
#    db.commit()
#    return successfull_response(201)

# @router.put('/{todo_id}')
# async def update_todo(todo_id: int,todo: Todo,user: dict=Depends(get_current_user),db: Session=Depends(get_db)):
   
#    todo_model = db.query(models.Todos)\
#    .filter(models.Todos.id == todo_id)\
#    .filter(models.Todos.owner_id == user.get("id")).first()

#    if todo_model is None:
#       raise raise_HTTPException()
#    todo_model.title = todo.title
#    todo_model.description = todo.description
#    todo_model.priority = todo.priority
#    todo_model.complete = todo.complete

#    db.add(todo_model)
#    db.commit()
#    return successfull_response(200)

# @router.delete('/{todo_id}')
# async def delete_todo(todo_id: int,user: dict=Depends(get_current_user),db:Session = Depends(get_db)):
#    todo_model = db.query(models.Todos)\
#       .filter(models.Todos.id == todo_id)\
#       .filter(models.Todos.owner_id == user.get("id")).first()
#    if todo_model is None:
#       raise raise_HTTPException()
#    db.query(models.Todos)\
#       .filter(models.Todos.id == todo_id)\
#       .filter(models.Todos.owner_id == user.get("id")).delete()
#    db.commit()
#    return successfull_response(200)


# def raise_HTTPException():
#    return HTTPException(status_code=404,detail='Item can\'t be found')

# def successfull_response(status_code: int):
#    return {'status_code':status_code,"transaction":"Transaction was Successfull!!!"}
