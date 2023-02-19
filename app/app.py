import uuid
from typing import Union, Optional, List, Dict

from beanie import init_beanie, Document, Link, PydanticObjectId
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from models.answer_set import AnswerSet
from models.question_set import QuestionSet
from models.user import User
from routers.api import api_router
import logging

from schemas.users import UserRead, UserCreate, UserUpdate
from users_config import auth_backend, current_active_user, fastapi_users

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

app = FastAPI()
app.include_router(api_router)
add_pagination(app)
"""
DB
"""


async def db_init():
    # Create Motor client
    client = AsyncIOMotorClient("mongodb://database:27017/mongodb", uuidRepresentation="standard")
    # Init beanie
    await init_beanie(database=client.db_name, document_models=[User, QuestionSet, AnswerSet])


async def test_db_init():
    # Create Motor client
    client = AsyncIOMotorClient("mongodb://database:27017/mongodb", uuidRepresentation="standard")
    db = client['test_database']
    # Init beanie
    await init_beanie(database=db, document_models=[User, QuestionSet, AnswerSet])


"""
ENDDB
"""


@app.on_event("startup")
async def startup_event():
    if app.debug:
        await test_db_init()
        logger.info("App start with test db")
    else:
        await db_init()
        logger.info("App start with normal db")


@app.on_event("shutdown")
async def shutdown_event():
    models = [User, QuestionSet, AnswerSet]
    for model in models:
        await model.get_motor_collection().drop()
        await model.get_motor_collection().drop_indexes()


@app.post("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/question_sets/{question_set_id}")
async def read_item(question_set_id: PydanticObjectId) -> QuestionSet:
    question_set = await QuestionSet.get(question_set_id)
    return question_set


@app.post("/question_sets/")
async def read_item(question_set: QuestionSet) -> QuestionSet:
    new_question_set = await QuestionSet(**question_set.dict()).save()
    return new_question_set


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


""" EndViews """
