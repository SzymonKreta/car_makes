# Car Make

This app enables microservice for Car Make data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before installing app you should have below libraries installed:

```
apt-get install postgresql postgresql-contrib postgresql-dev gcc python3-dev musl-dev  #postgresql and psycopg2 deps
```

### Installing

Create virtualenv and source it

```
virtualenv -p python3 venv
source venv/bin/activate
```

clone repository then install through pip python dependencies

```
pip install -r requirements.txt
pip install -r dev_requirements.txt  #for test purposes

```

Edit env.prod to store your DB data like user, password etc.
then run the following command:
```
set -o allexport
source conf-file
set +o allexport
```

Create using psql database, user and grant him privileges to databes you've set in env.prod file
Then you should be able to migrate your schema and run app from project root directory.

```
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Then go to ```localhost:800/api/v1``` to see endpoint details, you can check documentation also on ```/docs``` endpoint


## Running the tests

Add permision to creatdb your db_user e.g.

```
ALTER USER db_user CREATEDB;
```
Then if you have dev_requirements.txt deps installed then you can run test simpy by runnin ```pytest``` command from your project root directory


### And coding style tests

For pep8 check just run below command

```
flake8
```

## Deployment

The configuration is not yet finished!!!

For live deployment edit env.prod file then built it and run using docker-compose, you should also extend docker conf files by adding nginx section.
```
docker-compose -f docker-compose.yaml down -v
docker-compose -f docker-compose.yaml up -d --build
```
More info how to update your docker-compose.yaml and other files you can find [here](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django Rest Framework](https://www.django-rest-framework.org/) - toolkit for building Web APIs
* [pytest](https://docs.pytest.org/en/latest/) - test framework for writing parametrized tests

## Authors

* **Szymon Głuchowski**



