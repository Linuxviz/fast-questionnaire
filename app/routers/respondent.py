from fastapi import APIRouter

respondent_router = APIRouter(
    prefix="/respondent",
    responses={404: {"description": "Not found"}},
)
