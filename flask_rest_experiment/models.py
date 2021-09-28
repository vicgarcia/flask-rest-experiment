from datetime import datetime
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_enum import EnumField as enum_field


Base = declarative_base()


# a simple example ...

class SimpleExample(Base):
    __tablename__ = 'simple_examples'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(40), nullable=False)


class SimpleExampleSerializer(SQLAlchemyAutoSchema):

    class Meta:
        model = SimpleExample
        load_instance = True


# a more complex example ...

class ComplexType(Enum):
    one = 'one'
    two = 'two'


class ComplexExample(Base):
    __tablename__ = 'complex_examples'

    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(40), nullable=False)
    date = sa.Column(sa.Date())
    type = sa.Column(sa.Enum(ComplexType))
    created = sa.Column(sa.DateTime(), default=datetime.utcnow)
    deleted = sa.Column(sa.Boolean(), default=False)


class ComplexExampleSerializer(SQLAlchemyAutoSchema):
    created = auto_field(dump_only=True)
    type = enum_field(ComplexType)

    class Meta:
        model = ComplexExample
        load_instance = True
        fields = ('id', 'name', 'date', 'type', 'created')
        ordered = True
        datetimeformat = '%Y-%m-%d %H:%M:%S'
