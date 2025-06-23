from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"company_name":"Example company LLC"}

@router.get("/employees")
async def get_num_employees():
    return 166