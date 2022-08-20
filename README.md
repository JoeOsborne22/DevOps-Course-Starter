# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Setup a Trello Account and acquire a new 'Secret'
This app uses Trello's API to fetch and save to-do tasks. In order to call their API, you need to first create an account - https://trello.com/signup
Then generate an API key and token by following the instructions here - https://trello.com/app-key


## Testing The app
This to do app makes use of pytest for running test cases. Running the tests can be done in a few different ways shown below

while being in the project directory (the test foleder should be visible or you should be within this dir) you can run the below command.
This will run pytest on all available modules/scrits
    poetry run pytest 

Run tests for a particular module/script, cd into the dir where the file exists and run the following
    poetry run pytest <module/script name>
    e.g: poetry run pytest test_ToDoApps.py

Run tests in a directory - similar to the first option but now we can provide the filepath
say we are in <project>/<todo_app> and our tests are in <project>/<tests>, we can run with the following command
    poetry run pytest ../tests/

Lastly you can Run tests by keyword expressions
    poetry run pytest -k "<keyword>"
    e.g: poetry run pytest -k "category_split"

FYI - The E2E test has a dependency on having Firefox installed (and Geckodriver)

You can find more information here:https://docs.pytest.org/en/6.2.x/usage.html  

## Using Docker
This application comes with a Dockerfile for easy deploying to a container this allows anyone to pick up the app and get it running in moments.
## You will need to be in the root dir of the todo_app
- Build the Docker image
docker build --tag todo_app . 

- Build for a particular Env (prod, development, test available)
docker build --target test --tag my-test-image .
docker build --target development --tag todo-app:dev . 
docker build --target production --tag todo-app:prod .

- Run the docker image, this uses an env file, publishes ports for connectivity and gives thw image tag <todo_app>
docker run --publish 5000:5000 --env-file .env todo_app
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev

- Run docker image tests (unit+integration)
docker run --env-file .env.test my-test-image tests

- Run docker e2e tests
docker run -e MONGO_DB_NAME=<MONGO_DB_NAME> -e MONGO_CONNECT=<MONGO_CONNECT> -e MONGO_COLLECTION_NAME=<MONGO_COLLECTION_NAME> -e MONGO_DEFAULT_STATUS=<MONGO_DEFAULT_STATUS> my-test-image tests_e2e

- or to utilise the .env file:
docker run --env-file .env my-test-image tests_e2e


## Note as of 2022.03.11(exercise 9) integration with Trello has been terminated and instead replaced with MongoDB
This app now uses a MongoDB connection and will need the necessary environment variable set up for integration with this form of database.
Signup to MongoDB: https://www.mongodb.com/try


## As of 2022.07.01(ecercise 10) Authentication and Authorisation has been implemented. 
This will require users to authenticate via GitHub and then certain 'read', 'edit' permissions will be given per user ID. Default is 'read' access. 

## As of 2022.08.05(ecercise 11) The application is now hosted on Azure
This connectivity has also been added to the CI/CD pipeline to ensure the latest docker image is uploaded and then pulled and deployed to Azure.
