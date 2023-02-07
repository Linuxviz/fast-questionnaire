import uuid
from typing import Union, Optional, List, Dict

from beanie import init_beanie, Document, Link, PydanticObjectId
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from models.answer_set import AnswerSet
from models.question_set import QuestionSet
from models.user import User
from routers.api import api_router
import logging

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
    client = AsyncIOMotorClient("mongodb://database:27017/mongodb")
    # Init beanie
    await init_beanie(database=client.db_name, document_models=[User, QuestionSet, AnswerSet])


async def test_db_init():
    # Create Motor client
    client = AsyncIOMotorClient("mongodb://database:27017/mongodb")
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


""" EndViews """
