from fastapi import FastAPI,Depends
from routers import auth
import models
from starlette.staticfiles import StaticFiles

from database import engine
from routers import todos,users,address
from company import company,dependencies
from starlette import status
from starlette.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(address.router)

@app.get("/")
async def root():
    return RedirectResponse("/todos",status_code=status.HTTP_302_FOUND)

app.include_router(
    company.router,
    prefix="/company",tags=["company"],
    responses={418:{"description":"Internal Use only"}},
    dependencies=[Depends(dependencies.get_token_header)]
    )
app.include_router(users.router)

