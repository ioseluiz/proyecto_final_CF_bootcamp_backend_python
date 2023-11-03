# Bus Tickets E-commerce app

## Introduction



## Setup

The first thing to do is to clone the repository

```console
$ git clone https://github.com/ioseluiz/proyecto_final_CF_bootcamp_backend_python.git
```

Create a virtual environment to install dependencies in it an activate it:

```console
$ python3 -m venv env
$ source env/bin/activate
```

Next,install the dependencies:

```console
$ pip install -r requirements.txt
```

Note the (env) in front of the prompt. This indicates that the terminal session operates in virtual environment setup by virtualenv.

## Database Configuration

In the project root folder, create an .env file:

```console
$ touch .env
```
In PostgreSQL, create a database and assign a user to the database.

Open the .env file with a text editor and add the following:

```console
SECRET_KEY=<your_django_secret_key>
DEBUG=False
DB_NAME=<database_name>
DB_USER=<database_user>
DB_PASSWORD=<database_password>
DB_HOST=localhost
DB_PORT=5432
```

Apply database migrations with the following command:

```console
$ python manage.py migrate
```

Create a superuser, in order to test app's module that require admin privileges:

```console
$ python manage.py createsuperuser
```
