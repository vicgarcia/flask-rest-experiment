This is an experiment to utilize [Flask](https://flask.palletsprojects.com/), [Sqlalchemy](https://www.sqlalchemy.org/), and [Marshmallow](https://marshmallow.readthedocs.io/) in a way that replicates the experience of [Django REST Framework](https://www.django-rest-framework.org/). My goal was to be able to utilize SqlAlchemy and Marshmallow to define database models and configuration for serializing to and from JSON, then plug these components into a base view class that defines a typical set of REST endpoints. The end result is an quick way to get a set of REST endpoints by simply defining a database model and schema for serialization.

<br>

clone repository
```
git clone https://github.com/vicgarcia/flask-rest-experiment.git
cd flask-rest-experiment
```

install dependencies with poetry
```
poetry install
```

create sqlite database and run migrations
```
poetry run alembic upgrade head
```

run the flask app
```
poetry run python run.py
```

import `insomnia.yaml` and interact with the apis via [Insomnia](https://insomnia.rest/)
