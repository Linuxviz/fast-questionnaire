from fastapi import APIRouter

hr_router = APIRouter(
    prefix="/hr",
    responses={404: {"description": "Not found"}},
)
