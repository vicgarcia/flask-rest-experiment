import logging
from flask import Flask, _app_ctx_stack
from .database import create_engine, sessionmaker, scoped_session
from .rest import GET, POST, PATCH, DELETE

logger = logging.getLogger(__name__)


class config:
    DEBUG = True
    JSON_SORT_KEYS = False
    DATABASE_CONNECTION = 'sqlite:///flask_rest_experiment.db'


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('flask_rest_experiment.app.config')

    engine = create_engine(app.config['DATABASE_CONNECTION'])
    session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    app.db = scoped_session(session_maker, scopefunc=_app_ctx_stack.__ident_func__)
    # https://medium.com/analytics-vidhya/under-the-hood-of-flask-sqlalchemy-793f7b3f11c3

    from .views import SimpleExampleView
    SimpleExampleView.add_url_rules(app, '/simple-example', 'simple-example')

    from .views import ComplexExampleView
    ComplexExampleView.add_url_rules(app, '/complex-example', 'complex-example')

    return app
