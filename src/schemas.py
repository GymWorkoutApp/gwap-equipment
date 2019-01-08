from gwa_framework.schemas.base import BaseSchema
from schematics.types import StringType


class EquipmentInputSchema(BaseSchema):
    equipment_id = StringType(required=False, serialized_name='equipmentId')
    description = StringType(required=True, serialized_name='description', max_length=100, min_length=0)


class EquipmentOutputSchema(BaseSchema):
    equipment_id = StringType(required=True, serialized_name='equipmentId')
    description = StringType(required=True, serialized_name='description')

