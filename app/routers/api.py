from fastapi import APIRouter

from routers.version import version_v1_router

api_router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)
api_router.include_router(version_v1_router.router)
