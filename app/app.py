import uuid
from typing import Union, Optional, List, Dict

from beanie import init_beanie, Document, Link, PydanticObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

"""
DB
"""


class OpenCallback(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    next_question: uuid.UUID


class OpenQuestion(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    text: str
    next_question: uuid.UUID


class QuestionSet(Document):
    name: str
    description: str
    email_letter: Optional[str]
    questions: List[OpenQuestion]
    callbacks: Dict[str, OpenCallback]  # key - question_id # key ==uuid4
    users: "List[Link[User]]"
    customer: "List[User]"


class User(Document):  # This is the model
    user_name: str
    name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: bool
    is_user: bool
    is_respondent: bool
    is_customer: bool
    questions: List[Link[QuestionSet]]


QuestionSet.update_forward_refs()


async def db_init():
    # Create Motor client
    client = AsyncIOMotorClient("mongodb://database:27017/mongodb")
    # Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[User, QuestionSet])


"""
ENDDB
"""


@app.on_event("startup")
async def startup_event():
    await db_init()
    print("complete")


""" Views """
"""
Views:
respondent
1) list of questions_sets get /s  GET api/v1/respondent/question_sets/
2) start question_set post /id    POST api/v1/respondent/question_sets/{id} (start session, create user_answer_sets)
3) Does anwser                     POST api/v1/respondent/user_answer/
HR
0) list of sets                   GET api/v1/hr/question_sets/
0.1) question_set info            GET api/v1/hr/question_sets/{id}
1) create question_sets post      POST api/v1/hr/question_sets/
2) add question post              POST api/v1/hr/question/
# 3) change data patch              
# 4) start (change status) patch
customer
1) list of question_sets get      GET api/v1/customer/question_sets/

Routers:
root - api
versioning - v1
respondent, hr, customer

"""

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
