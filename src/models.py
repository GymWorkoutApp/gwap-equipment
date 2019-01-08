from uuid import uuid4

from gwa_framework.models.base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class EquipmentModel(BaseModel):
    __tablename__ = 'equipments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    description = Column(String(100), nullable=False)