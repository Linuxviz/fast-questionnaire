import datetime
import math
from typing import Any, Optional

from beanie import PydanticObjectId, Document
from fastapi import APIRouter, Query, HTTPException
from fastapi_pagination import Page, LimitOffsetPage
from pydantic import BaseModel, PositiveInt

from models.question_set import QuestionSet, QuestionSetCreationStatusEnum
from fastapi_pagination.ext.beanie import paginate

hr_router = APIRouter(
    prefix="/hr",
    responses={404: {"description": "Not found"}},
    tags=["HR", ]
)


class HRQuestionSetsProjection(BaseModel):
    _id: PydanticObjectId
    name: str
    description: str
    email_letter: str | None
    customer: list
    creation_status: QuestionSetCreationStatusEnum
    create_at: datetime.datetime


class PaginatedOut(BaseModel):
    total_elements: PositiveInt
    total_pages: PositiveInt
    page: PositiveInt
    page_size: PositiveInt
    items: list


class HROutQuestionSet(PaginatedOut):
    items: list[HRQuestionSetsProjection]


@hr_router.get("/question_sets/", response_model=HROutQuestionSet)
async def list_of_respondent_question_sets(
        page_size: int | None = Query(50, ge=1, le=100, description="Page size"),
        page: int | None = Query(1, ge=1, description="Page number")
):
    total_elements = await QuestionSet.find({}).count()
    total_pages = math.ceil(total_elements / page_size)
    if page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Page index - {page} more then count of total pages - {total_pages}"
        )
    limit = page_size
    offset = page_size * (page - 1)

    result = await QuestionSet.find_many(
        limit=limit,
        skip=offset
    ).project(HRQuestionSetsProjection).to_list()

    return {
        'total_elements': total_elements,
        'total_pages': total_pages,
        'page': page,
        'page_size': page_size,
        'items': result
    }


@hr_router.get("/question_sets/{id}")
async def list_of_respondent_question_set_sets(question_set_id: PydanticObjectId):
    return await QuestionSet.get(question_set_id)


@hr_router.post("/question_sets")
async def start_question_set(question_set_id: PydanticObjectId):
    pass


@hr_router.post("/question")
async def set_answer(question_set_id: PydanticObjectId):
    pass
