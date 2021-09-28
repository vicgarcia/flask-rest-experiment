import logging
from flask import current_app, request
from .rest import RestView, SoftDeleteMixin, ParameterException
from .models import (
    SimpleExample, SimpleExampleSerializer,
    ComplexExample, ComplexType, ComplexExampleSerializer,
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
        if type_param and type_param in ComplexType.values():
            query = query.filter_by(type=str(type_param))
        elif type_param:
            raise ParameterException('must provide a valid type parameter')

        # allow search by date, between 'start' and 'end'
        start_param = request.args.get('start', None)
        end_param = request.args.get('end', None)
        if start_param and end_param:
            query = query.filter(self.model_class.date.between(start_param, end_param))
        elif (start_param and not end_param) or (end_param and not start_param):
            raise ParameterException('must provide both start and end parameters')

        return query
