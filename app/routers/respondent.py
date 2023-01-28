from beanie import PydanticObjectId
from fastapi import APIRouter

respondent_router = APIRouter(
    prefix="/respondent",
    responses={404: {"description": "Not found"}},
    tags=["Respondents", ]
)


@respondent_router.get("/question_sets")
async def list_of_respondent_question_set_sets():
    pass


@respondent_router.post("/question_sets")
async def start_question_set(question_set_id: PydanticObjectId):
    pass


@respondent_router.post("/user_answer")
async def set_answer(question_set_id: PydanticObjectId):
    pass
