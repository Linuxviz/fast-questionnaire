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


"""
ENDDB
"""


@app.on_event("startup")
async def startup_event():
    await db_init()
    print("complete")


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
