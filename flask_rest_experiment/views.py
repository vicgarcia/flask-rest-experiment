import logging
from flask import current_app, request
from .rest import RestView, SoftDeleteMixin
from .models import (
    SimpleExample, SimpleExampleSerializer,
    ComplexExample, ComplexExampleSerializer,
)

logger = logging.getLogger(__name__)


class SimpleExampleView(RestView):
    model_class = SimpleExample
    serializer_class = SimpleExampleSerializer


class ComplexExampleView(RestView, SoftDeleteMixin):
    model_class = ComplexExample
    serializer_class = ComplexExampleSerializer

    # override get_objects_query to add search params on the list endpoint

    def get_objects_query(self):
        query = super().get_objects_query()

        # allow search by 'type'
        type_param = request.args.get('type', None)
        if type_param:
            query = query.filter_by(type=str(type_param))

        # allow search by date, between 'start' and 'end'
        start_param = request.args.get('start', None)
        end_param = request.args.get('end', None)
        if start_param and end_param:
            query = query.filter(self.model_class.date.between(start_param, end_param))

        # idea: use a custom exception type to set message + raise on error
        #       catch the exception and turn the message into error response
        #       similar to the way serializers raise ValidationError

        return query
