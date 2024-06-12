## Quick User Guide Before Running This Project

Make sure you are in the root directory of the project, the one with `Pipfile` in it.

First, copy the contents of `dev-example.env` file over to a new `.env` file. This holds the environmental variables to configure the project.

## For Docker Development

You need to have Docker and Docker Compose. Git clone this project and enter its root directory, then run the following commands:

1. Build Docker images
```
docker-compose build
```
2. Apply migrations to set up the initial database tables.
```
docker-compose run django ./manage.py migrate
```
3. Start project / Start the services defined in the docker-compose.yml file
```
docker-compose up
```

Below are other useful commands

1. To create a superuser
```
docker-compose run django ./manage.py createsuperuser
```
2. To run all test cases
```
docker-compose run django ./manage.py test
```
3. To run test cases in a specific app (users, games and teams)
```
docker-compose run django ./manage.py test teams
```
4. To access the interactive console
```
docker-compose run django python ./manage.py shell
```
5. To starts an interactive Bash shell inside the container
```
docker-compose run django bash
```

## For Native Development

This project requires the following dependencies, so first install them on your system using your preferred method.
- Python 3.10
- Pipenv
- PostgreSQL 14 or compatible

By default, it will attempt to connect to the local PostgreSQL server using `tigerlab` as the user and database name, with an empty password. These can be changed using the `DB_*` environmental variables in the `.env` file.

In the root directory run the following command

1. Create a virtual environment
```
pipenv shell
```
2. Download and install all the Python dependencies
```
pipenv sync
```
3. Apply migrations to set up the initial database tables.
```
python3 manage.py migrate
```
4. Start the local server
```
python3 manage.py runserver
```

## Pre-commit setup

Developers should set up pre-commit before commiting any code.

1. Install pre-commit
```
pip install pre-commit
```
2. Setup pre-commit in git repo
```
pre-commit install
```
3. Run pre-commit in all file (optional)
```
pre-commit run --all-files
```

##### Reference
- [Pre-commit Install](https://pre-commit.com/#install)
