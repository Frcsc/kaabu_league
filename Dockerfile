# NOTE: This Dockerfile is meant for development use, not for production

FROM python:3.10-slim

WORKDIR /tigerlab

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
