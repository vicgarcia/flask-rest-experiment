from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from marshmallow import ValidationError

connection_string = 'sqlite:///flask_rest_experiment.db'
engine = create_engine(connection_string)

create_session = sessionmaker(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
