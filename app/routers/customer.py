from fastapi import APIRouter

customer_router = APIRouter(
    prefix="/customer",
    responses={404: {"description": "Not found"}},
)
