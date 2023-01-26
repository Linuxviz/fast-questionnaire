FROM python:3.11.1-alpine3.16

COPY requirements.txt /requirements/requirements.txt
COPY app /app
WORKDIR /app
EXPOSE 8080

RUN pip install --upgrade -r /requirements/requirements.txt

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]