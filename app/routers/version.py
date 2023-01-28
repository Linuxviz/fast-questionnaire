from fastapi import APIRouter

from routers.customer import customer_router
from routers.hr import hr_router
from routers.respondent import respondent_router

version_v1_router = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)

version_v1_router.include_router(respondent_router.router)
version_v1_router.include_router(hr_router.router)
version_v1_router.include_router(customer_router.router)