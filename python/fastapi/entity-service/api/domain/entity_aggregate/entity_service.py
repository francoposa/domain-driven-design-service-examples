from typing import Optional

import pydantic

from api.domain.entity_aggregate.entity import Entity, EntityList
from api.domain.entity_aggregate.entity_repo import IEntityRepo


class EntityService:
    """EntityService encapsulates all Entity aggregate root domain logic and provides
    an interface for all other components to interact with the Entity aggregate root.

    EntityService is an example implementation of the Service pattern

    * All operations performed by an API endpoint, user interface, message queue handler,
        or otherwise should be done using the public EntityService interface.
    * Services contain only "business"/domain logic or abstractions of underlying infrastructure
        concepts, such as the "Unit of Work" pattern as an abstraction of database transactions.
    * Services wrap around Repository implementations and should call the public methods of a
        Repository in order to persist any changes to application state
    * Services do not perform the Repository's role of interacting with the infrastructure layer
    """

    def __init__(self, repo: IEntityRepo):
        self._repo = repo

    async def get(self, entity_id: pydantic.UUID4) -> Entity:
        pass

    async def where(
        self, page: Optional[int] = None, size: Optional[int] = None
    ) -> EntityList:
        pass

    async def create(self, entity: Entity) -> Entity:
        return await self._repo.create(entity)

    async def create_or_update(self, entity: Entity) -> Entity:
        pass

    async def update(self, entity: Entity) -> Entity:
        pass

    async def delete(self, entity_id) -> Entity:
        pass
