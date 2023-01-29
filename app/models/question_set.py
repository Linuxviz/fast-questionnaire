import datetime
import uuid
from enum import Enum

from beanie import Document, Link
from pydantic import BaseModel


class OpenCallback(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    next_question: uuid.UUID


class OpenQuestion(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    text: str
    next_question: uuid.UUID


class QuestionSetCreationStatusEnum(str, Enum):
    draft = 'draft'
    created = 'created'
    launched = 'launched'
    stopped = 'stopped'
    archived = 'archived'


class QuestionSet(Document):
    name: str
    description: str
    email_letter: str | None
    questions: list[OpenQuestion]
    callbacks: dict[str, OpenCallback]  # key - question_id # key ==uuid4
    users: "list[Link[User]]"
    customer: "list[User]"
    creation_status: QuestionSetCreationStatusEnum = "draft"
    create_at: datetime.datetime = datetime.datetime.now()


from models.user import User  # circular dependency resolve

QuestionSet.update_forward_refs()
