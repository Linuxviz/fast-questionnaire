import logging

from tests.confest import test_client

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()


def test_get_hr_question_set(test_client):
    json = {
        "name": "string",
        "description": "string",
        "email_letter": "string",
        "questions": [
            {
                "id": "7a707ea0-0791-4d07-8e36-7e8d85b08748",
                "text": "string",
                "next_question": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        ],
        "callbacks": {
            "additionalProp1": {
                "id": "f17f39cf-534e-46da-8fcf-b7a1964f219b",
                "next_question": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            },
            "additionalProp2": {
                "id": "f17f39cf-534e-46da-8fcf-b7a1964f219b",
                "next_question": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            },
            "additionalProp3": {
                "id": "f17f39cf-534e-46da-8fcf-b7a1964f219b",
                "next_question": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        },
        "users": [
        ],
        "customer": [],
        "creation_status": "draft",
        "create_at": "2023-02-05T15:42:26.488379"
    }
    test_client.post('http://127.0.0.1:8080/question_sets/', json=json)
    response = test_client.get("/api/v1/hr/question_sets/")
    assert response.status_code == 200
