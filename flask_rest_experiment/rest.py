import logging
from flask import current_app, json, request, jsonify
from flask.views import MethodView
from .database import ValidationError

logger = logging.getLogger(__name__)


GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'


class NotFoundException(Exception):
    pass


class RestView(MethodView):
    model_class = None
    serializer_class = None

    def get_object_query(self, obj_id):
        return current_app.db.query(self.model_class).filter_by(id=obj_id)

    def get_object(self, obj_id):
        query = self.get_object_query(obj_id)
        obj = query.first()
        if not obj:
            raise NotFoundException
        return obj

    def get_objects_query(self):
        return current_app.db.query(self.model_class)

    def post(self):
        logger.debug(f'{self.__class__.__name__}.post request.json={request.json}')
        try:
            serializer = self.serializer_class()
            obj = serializer.load(request.json, session=current_app.db)
            current_app.db.add(obj)
            current_app.db.commit()
            return serializer.dumps(obj)
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception as e:
            logger.exception(f'{self.__class__.__name__}.post exception')
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def get(self, obj_id):
        logger.debug(f'{self.__class__.__name__}.get request.args={dict(request.args)} obj_id={obj_id}')
        try:
            serializer = self.serializer_class()
            if obj_id is not None:
                obj = self.get_object(obj_id)
                return serializer.dumps(obj)
            else:
                limit = int(request.args.get('limit', 10))
                offset = int(request.args.get('offset', 0))
                query = self.get_objects_query()
                return jsonify({
                    'data': serializer.dump(query.limit(limit).offset(offset), many=True),
                    'total': query.count(),
                    'limit': limit,
                    'offset': offset,
                })
        except ValueError:
            return jsonify({'error': 'invalid limit/offset parameters'}), 400
        except NotFoundException:
            return '', 404
        except Exception as e:
            logger.exception(f'{self.__class__.__name__}.get exception')
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def patch(self, obj_id):
        logger.debug(f'{self.__class__.__name__}.patch request.json={request.json}')
        try:
            serializer = self.serializer_class()
            obj = self.get_object(obj_id)
            obj = serializer.load(request.json, session=current_app.db, instance=obj, partial=True)
            current_app.db.add(obj)
            current_app.db.commit()
            return serializer.dumps(obj)
        except NotFoundException:
            return '', 404
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception as e:
            logger.exception(f'{self.__class__.__name__}.patch exception')
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def delete(self, obj_id):
        logger.debug(f'{self.__class__.__name__}.delete obj_id={obj_id}')
        try:
            obj = self.get_object(obj_id)
            current_app.db.delete(obj)
            current_app.db.commit()
            return '', 204
        except NotFoundException:
            return '', 404
        except Exception as e:
            logger.exception(f'{self.__class__.__name__}.delete exception')
            return jsonify({'error': 'an unhandled error occurred'}), 500

    @classmethod
    def add_url_rules(cls, app, base_url, view_name):
        as_view = cls.as_view(view_name)
        app.add_url_rule(f"{base_url}", view_func=as_view, methods=[GET], defaults={'obj_id': None})
        app.add_url_rule(f"{base_url}", view_func=as_view, methods=[POST])
        app.add_url_rule(f"{base_url}/<int:obj_id>", view_func=as_view, methods=[GET, PATCH, DELETE])


class SoftDeleteMixin:

    def get_object_query(self, obj_id):
        return current_app.db.query(self.model_class).filter_by(deleted=False, id=obj_id)

    def get_objects_query(self):
        return current_app.db.query(self.model_class).filter_by(deleted=False)

    def delete(self, obj_id):
        try:
            obj = self.get_object(obj_id)
            obj.deleted = True
            current_app.db.add(obj)
            current_app.db.commit()
            return '', 204
        except NotFoundException:
            return '', 404
        except Exception as e:
            logger.exception(f'{self.__class__.__name__}.delete exception')
            return jsonify({'error': 'an unhandled error occurred'}), 500
