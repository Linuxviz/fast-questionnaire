from beanie import PydanticObjectId
from fastapi import APIRouter

from models.question_set import QuestionSet

hr_router = APIRouter(
    prefix="/hr",
    responses={404: {"description": "Not found"}},
    tags=["HR", ]
)


@hr_router.get("/question_sets")
async def list_of_respondent_question_set_sets():
    QuestionSet.find_all()


@hr_router.get("/question_sets/{id}")
async def list_of_respondent_question_set_sets(question_set_id: PydanticObjectId):
    pass


@hr_router.post("/question_sets")
async def start_question_set(question_set_id: PydanticObjectId):
    pass


@hr_router.post("/question")
async def set_answer(question_set_id: PydanticObjectId):
    pass
