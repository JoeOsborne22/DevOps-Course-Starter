FROM python:3.9 as base
# Perform common operations, dependency installation etc...

EXPOSE 5000
WORKDIR /app

#Having to install dependencies including flask and gunicorn as hit errors without this
RUN pip install poetry
RUN pip install gunicorn
RUN pip install flask

COPY pyproject.toml poetry.lock ./

RUN poetry install
COPY todo_app todo_app


FROM base as production 
# Configure for production
ENTRYPOINT ["gunicorn"  , "--bind", "0.0.0.0:5000", "todo_app.app:create_app()"]

FROM base as development  
# Configure for local development
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]

