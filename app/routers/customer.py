from fastapi import APIRouter

customer_router = APIRouter(
    prefix="/customer",
    responses={404: {"description": "Not found"}},
    tags=["Customers", ]
)


@customer_router.get("/question_sets")
async def list_of_respondent_question_set_sets():
    pass
