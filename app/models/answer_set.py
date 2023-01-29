import datetime
import uuid

from beanie import Document, Link
from pydantic import BaseModel

from models.question_set import QuestionSet
from models.user import User



class UserAnswer(BaseModel):
    question: uuid.UUID
    answer: str


class AnswerSet(Document):
    create_at: datetime.datetime = datetime.datetime.now()
    question_set: Link[QuestionSet]
    user_answers: list[UserAnswer]
    users: Link[User]
