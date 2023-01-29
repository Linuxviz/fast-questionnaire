import datetime

from beanie import Document, Link


class User(Document):
    user_name: str
    name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    password: str
    is_active: bool
    is_user: bool
    is_respondent: bool
    is_customer: bool
    questions: "list[Link[QuestionSet]]"
    register_at: datetime.datetime = datetime.datetime.now()


from models.question_set import QuestionSet  # circular dependency resolve

User.update_forward_refs()
