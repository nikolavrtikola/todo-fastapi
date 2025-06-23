import sys 
sys.path.append("..")

from fastapi import Depends, Form,HTTPException,status,APIRouter,Request,Response
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from database import engine,SessionLocal
from typing import Optional
from sqlalchemy.orm import Session
import models
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt,JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401:{"user":"Not Authorized"}}
)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

SECRET_KEY = "4s1u07NOnPZqLonwB8nfjZVxsbnFRx9X"
ALGORITHM = "HS256"

# class CreateUser(BaseModel):
#     username: str
#     email: Optional[str]
#     first_name: str
#     last_name: str
#     password: str
#     phone_number:str

class LoginForm:
    def __init__(self,request:Request):
        self.request:Request = request
        self.username:Optional[str] = None
        self.password:Optional[str] = None
    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")


bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oaut2_bearer = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(userneme:str,user_id:int,expires_delta: Optional[timedelta]=None):
    encode = {"sub":userneme,"id":user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_password_ghash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_pass,hashed_pass):
    return bcrypt_context.verify(plain_pass,hashed_pass)

def authenticate_user(username: str,password: str,db: Session):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user
 
async def get_current_user(request:Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username":username,"id":user_id}
    except JWTError:
        raise HTTPException(status_code=404,detail="Not Found")




# @router.post('/create/user')
# async def create_new_user(create_user: CreateUser,db: Session = Depends(get_db)):
#     crete_user_model = models.Users()
#     crete_user_model.username = create_user.username
#     crete_user_model.email = create_user.email
#     crete_user_model.first_name = create_user.first_name
#     crete_user_model.last_name = create_user.last_name

#     hashed_pass = get_password_ghash(create_user.password)
#     crete_user_model.hashed_password = hashed_pass
#     crete_user_model.is_active = True
#     crete_user_model.phone_number = create_user.phone_number
#     db.add(crete_user_model)
#     db.commit()
#     return {"status_code":201,"transaction":"Transaction succesfull!!!"}

 

# @router.post("/token")
# async def login_for_access_token(
#     response: Response,
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     if not perform_login(form_data.username, form_data.password, db, response):
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     return {"message": "Login successful"}
###########################################################################################
# @router.post("/token")
# async def login_for_access_token(
#     response: Response,
#     request: Request,
#     form_data: OAuth2PasswordRequestForm = Depends(LoginForm),
#     db: Session = Depends(get_db)
# ):
#     token = perform_login(form_data.username, form_data.password, db)
#     if not token:
#         msg= "Invalid Username or Password"
#         # raise HTTPException(status_code=400, detail="Invalid username or password")
#         return templates.TemplateResponse("login.html",{"request":request,"msg":msg})

#     response.set_cookie(key="access_token", value=token, httponly=True)
#     response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
#     return response 
#     # return {"access_token": token}

##########################################################################################

# def perform_login(username: str, password: str, db: Session, response: Response) -> bool:
#     user = authenticate_user(username, password, db)
#     if not user:
#         return False
    
#     token_expires = timedelta(minutes=60)
#     token = create_access_token(user.username, user.id, expires_delta=token_expires)
#     response.set_cookie(key="access_token", value=token, httponly=True)
#     return True

def perform_login(username: str, password: str, db: Session) -> Optional[str]:
    user = authenticate_user(username, password, db)
    if not user:
        return None
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return token


#########################################################################################
@router.get("/",response_class=HTMLResponse)
async def authentication_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

#########################################################################################
# @router.post("/",response_class=HTMLResponse)
# async def login(request:Request,db:Session=Depends(get_db)):
  
#         form = LoginForm(request)
#         await form.create_oauth_form()
    
#         response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
#         token = perform_login(form.username, form.password, db)
#         # validate_user_cookie = login_for_access_token(response=response,form_data=form,db=db)
#         # Use form.username and form.password directly here
#         if not token:
        
#             msg = "Invalid username or password"
#             return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
#         response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
#         response.set_cookie(key="access_token", value=token, httponly=True)
#         return response

#################################################################################################################
@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    form = LoginForm(request)
    await form.create_oauth_form()
    print("Username:", form.username)
    print("Password:", form.password)


    token = perform_login(form.username, form.password, db)

    if not token:
        msg = "Invalid username or password"
        return templates.TemplateResponse("login.html", {
            "request": request,
            "msg": msg
        })

    response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response



        
##################################################################################################################    

@router.get("/logout")
async def logout(request:Request):
    msg = "You Logged Out Succesfuly"
    response = templates.TemplateResponse("login.html",{"request":request,"msg":msg})
    response.delete_cookie(key="access_token")
    return response

@router.get("/register",response_class=HTMLResponse)
async def register(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})

@router.post("/register",response_class=HTMLResponse)
async def register_user(request:Request,email:str=Form(...),
                        username:str=Form(...),firstname:str=Form(...),
                        lastname:str=Form(...),password:str=Form(...),password2:str=Form(...),
                        db:Session=Depends(get_db)):
    validation1 = db.query(models.Users).filter(models.Users.username == username).first()
    validation2 = db.query(models.Users).filter(models.Users.email == email).first()
    
    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html",{"request":request,"msg":msg})
    
    user_model = models.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname
    hashed_password = get_password_ghash(password)
    user_model.hashed_password = hashed_password
    user_model.is_active = True
    db.add(user_model)
    db.commit()
    msg = "User Sucessfuly created"
    return templates.TemplateResponse("login.html",{"request":request,"msg":msg})


#Exeptions
# def get_user_exeption():
#     credential_exeptions = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate":"Bearer"})
#     return credential_exeptions

# def get_token_exeption():
#     token_exeption_response = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Incorect Username or password",
#         headers={"WWW-Authenticate":"Bearer"}
#     )
#     return token_exeption_response;