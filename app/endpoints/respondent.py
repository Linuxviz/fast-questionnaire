from routers.respondent import respondent_router as router

@router.get("/question_sets/{question_set_id}")
async def read_item(question_set_id: PydanticObjectId) -> QuestionSet:
    question_set = await QuestionSet.get(question_set_id)
    return question_set