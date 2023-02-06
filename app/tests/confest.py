import logging

import pytest

from starlette.testclient import TestClient


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


# # @pytest.fixture(autouse=True)
# @pytest.fixture
# async def clean_db(loop, db):
#     models = [User, QuestionSet, AnswerSet]
#     yield None
#
#     for model in models:
#         await model.get_motor_collection().drop()
#         await model.get_motor_collection().drop_indexes()


@pytest.fixture(scope="session")
def test_client():
    # API client
    from app import app
    app.debug = True

    with TestClient(app) as test_client:
        yield test_client
