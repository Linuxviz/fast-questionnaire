from typing import Union, Optional, List

from beanie import init_beanie, Document, Link
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

"""
DB
"""


# class QuestionSet(Document):

class User(Document):  # This is the model
    user_name: str
    name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: bool
    # questions: List[Link[QuestionSet]]


async def db_init():
    # Create Motor client
    client = AsyncIOMotorClient("mongodb://database:27017/mongodb")
    # Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[User])


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


@app.post("/a")
async def read_item(item: User):
    new_user = await User(**item.dict()).insert()
    return new_user
