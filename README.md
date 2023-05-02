# Superdevs

This is the Superdevs reqrutment task. It is a simple Django app that uses the swapi.dev API to display data about
Star Wars characters. Task related files are located in superdevs/starwars module of app.

[Task File](./TASK.md)

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Envs

to speed up the development process, envs are stored in the repository. This practice in normal circumstances is
would be a security risk, but since this is a not-production project, It is decided to do it this way.

## Requirements

- docker
- docker-compose
- python 3.8+
- pre-commit

## Commands

All critical commands are in the Makefile. Commands:

- `make build` - builds the docker-compose
- `make make_migrations` - runs django makemigrations
- `make migrate` - runs django migrate
- `make mm` - runs django makemigrations and migrate
- `make superuser` - runs django createsuperuser
- `make collectstatic` - runs django collectstatic
- `make exportdata` - runs django dumpdata to data.json located in root directory
- `make importdata` - runs django loaddata from data.json located in root directory
- `make update_dep` - install pip-tools and execute pip-compile which will update the dependacies in requirements
  files
- `make enter_running` - enter the running container (useful for debugging)
- `make shell_plus` - runs django shell_plus in running container
- `make reset_db` - resets the database (deletes all data)
- `make down_db` - stops the database container
- `make init_all` - runes make reset_db, make down_db, make mm
- `make build_all` - runes make build, make collectstatic, make init_all
- `make docker_clean` - removes all docker images and containers
- `make run` - runs the app
- `make test` - runs the tests

## Instalation

To set up your local environment, you need to have docker and docker-compose installed. Then, run the following
commands:

    $ git clone https://github.com/kamil1marczak/superdevs.git
    $ cd superdevs
    $ pre-commit install
    $ make build
    $ make mm
    $ make superuser
    $ make collectstatic

## Running the app

After the instalation, you can run the app with the following command:

    $ make run

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ make createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Running tests with pytest

    $ make test
