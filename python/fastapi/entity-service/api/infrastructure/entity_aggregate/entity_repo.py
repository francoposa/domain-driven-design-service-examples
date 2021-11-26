import pydantic

from api.domain.entity_aggregate.entity import Entity, EntityList
from api.domain.entity_aggregate.entity_repo import IEntityRepo


class StubEntityRepo(IEntityRepo):
    async def get(self, entity_id: pydantic.UUID4) -> Entity:
        pass

    async def list(self, page: int = 0, size: int = 0) -> EntityList:
        pass

    async def create(self, entity: Entity) -> Entity:
        pass

    async def update(self, entity: Entity) -> Entity:
        pass

    async def create_or_update(self, entity: Entity) -> Entity:
        pass

    async def delete(self, entity_id: pydantic.UUID4) -> Entity:
        pass
