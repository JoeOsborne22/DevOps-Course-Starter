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
COPY tests tests
COPY tests_e2e tests_e2e
COPY runTodoApp.sh runTodoApp.sh
RUN chmod +x ./runTodoApp.sh



FROM base as development  
# Configure for local development
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as test
# Configure for running tests
ENTRYPOINT [ "poetry", "run", "pytest"]

FROM base as production 
# Configure for production
#ENTRYPOINT ["poetry" ,"run" , "gunicorn"  , "--bind", "0.0.0.0:5000", "todo_app.app:create_app()"]
ENTRYPOINT ./runTodoApp.sh


ENV GECKODRIVER_VER v0.29.1
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/ \
    && rm geckodriver-*.tar.gz
