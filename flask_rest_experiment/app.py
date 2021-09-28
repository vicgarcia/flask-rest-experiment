import logging
from flask import Flask, _app_ctx_stack
from .database import scoped_session, SessionLocal
from .rest import GET, POST, PATCH, DELETE

logger = logging.getLogger(__name__)


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config['JSON_SORT_KEYS'] = False

    app.db = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    from .views import SimpleExampleView
    SimpleExampleView.add_url_rules(app, '/simple-example', 'simple-example')

    from .views import ComplexExampleView
    ComplexExampleView.add_url_rules(app, '/complex-example', 'complex-example')

    return app
