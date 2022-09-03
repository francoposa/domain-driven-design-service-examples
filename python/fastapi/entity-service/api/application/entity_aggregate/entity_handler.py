import pydantic
from fastapi import HTTPException

from api.domain.entity_aggregate.entity import Entity, EntityList
from api.domain.entity_aggregate.entity_errors import EntityNotFoundError
from api.domain.entity_aggregate.entity_service import EntityService


class EntityHandler:
    def __init__(self, service: EntityService):
        self._service = service

    async def get(self, entity_id: pydantic.UUID4) -> Entity:
        try:
            return await self._service.get(entity_id)
        except EntityNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    async def list(self, page: int = 0, size: int = 20) -> EntityList:
        return await self._service.where(page=page, size=size)

    async def create(self, entity: Entity) -> Entity:
        return await self._service.create(entity)
