FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install motor
RUN pip install email-validator

COPY ./app /app/app