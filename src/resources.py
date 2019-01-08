from typing import Dict
from uuid import uuid4

from gwa_framework.resource.base import BaseResource
from gwa_framework.utils.decorators import validate_schema

from src.cache import cache
from src.database import master_async_session, read_replica_async_session
from src.models import EquipmentModel
from src.schemas import EquipmentInputSchema, EquipmentOutputSchema


class EquipmentResource(BaseResource):
    cache = cache
    method_decorators = {
        'create': [validate_schema(EquipmentInputSchema)],
        'update': [validate_schema(EquipmentInputSchema)],
    }

    def create(self, request_model: 'EquipmentInputSchema') -> Dict:
        goal = EquipmentModel()
        goal.id = request_model.equipment_id or str(uuid4())
        goal.description = request_model.description
        with master_async_session() as session:
            session.add(goal)
            output = EquipmentOutputSchema()
            output.equipment_id = goal.id
            output.description = goal.description
            output.validate()
            return output.to_primitive()

    def update(self, request_model: 'EquipmentInputSchema', equipment_id=None):
        goal = EquipmentModel()
        goal.id = equipment_id
        goal.description = request_model.description
        with master_async_session() as session:
            session.merge(goal)
            output = EquipmentOutputSchema()
            output.equipment_id = goal.id
            output.description = goal.description
            output.validate()
            return output.to_primitive()

    def list(self, args=None, kwargs=None):
        with read_replica_async_session() as session:
            results = []
            for goal in session.query(EquipmentModel).all():
                schema = EquipmentOutputSchema()
                schema.equipment_id = goal.id
                schema.description = goal.description
                results.append(schema.to_primitive())
        return results

    def retrieve(self, equipment_id):
        with read_replica_async_session() as session:
            goal = session.query(EquipmentModel).filter_by(id=equipment_id).first()
            schema = EquipmentOutputSchema()
            schema.equipment_id = goal.id
            schema.description = goal.description
            return schema.to_primitive()

    def destroy(self, equipment_id):
        with master_async_session() as session:
            session.query(EquipmentModel).filter_by(id=equipment_id).delete()
            return None


resources_v1 = [
    {'resource': EquipmentResource, 'urls': ['/equipments/<equipment_id>'], 'endpoint': 'Equipments EquipmentId',
     'methods': ['GET', 'PUT', 'PATCH', 'DELETE']},
    {'resource': EquipmentResource, 'urls': ['/equipments'], 'endpoint': 'Equipments',
     'methods': ['POST', 'GET']},
]
