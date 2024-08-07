This is an experiment to utilize [Flask](https://flask.palletsprojects.com/), [Sqlalchemy](https://www.sqlalchemy.org/), and [Marshmallow](https://marshmallow.readthedocs.io/) in a way that replicates the experience of [Django REST Framework](https://www.django-rest-framework.org/). My goal was to be able to utilize SqlAlchemy and Marshmallow to define database models and configuration for serializing to and from JSON, then plug these components into a base view class that defines a typical set of REST endpoints. The end result is an quick way to get a set of REST endpoints by simply defining a database model and schema for serialization.


## example

Start with the Sqlalchemy ORM model to store data. The REST API will allow the manipulation of the ORM model.

```
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SimpleExample(Base):
    __tablename__ = 'simple_examples'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(40), nullable=False)
```

Define a serializer using Marshmallow. Ther serializer will handle conversion between JSON data and the ORM model.

```
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class SimpleExampleSerializer(SQLAlchemyAutoSchema):

    class Meta:
        model = SimpleExample
        load_instance = True
```

ORM models and serializers are defined in `flask_rest_experiment/models.py` in this repository.

The `RestView` class defineds GET (query and retrieve), POST (create), PATCH (edit), and DELETE (delete) handlers for the endpoint. It extends from from the Flask [MethodView](https://flask.palletsprojects.com/en/2.3.x/views/) class and implements the logic to utilize the serializer and manipulate the ORM model.

The `RestView` class is defined in `flask_rest_experiment/rest.py`.


Extend from `RestView` to create an REST API for a given ORM model.

```
from .rest import RestView

class SimpleExampleView(RestView):
    model_class = SimpleExample
    serializer_class = SimpleExampleSerializer
```

Views extened from the `RestView` base class are defined in `flask_rest_experiment/views.py`.


The view class provides a class method to create the necessary routing for a Flask app to include our REST API as part of an app. Call the `add_url_rules` class method and specify the Flask app, the url for the endpoint set, and a name for the views.

```
app = Flask(__name__, instance_relative_config=True)

...

from .views import SimpleExampleView
SimpleExampleView.add_url_rules(app, '/simple-example', 'simple-example')
```

The flask application and necessary routing to use the defined API is defined in `flask_rest_experiment/app.py`.


## code

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
