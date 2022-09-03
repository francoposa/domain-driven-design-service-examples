import uuid
from typing import Dict, List, Mapping, Optional

import pydantic
from databases import Database
from databases.backends.postgres import Record
from sqlalchemy.sql import Insert

from api.domain.entity_aggregate.entity import ChildEntity, Entity, EntityList
from api.domain.entity_aggregate.entity_repo import IEntityRepo
from api.infrastructure.datastore.postgres.tables import (
    CHILD_ENTITY_TABLE,
    ENTITY_CHILD_ENTITY_TABLE,
    ENTITY_TABLE,
)
from api.infrastructure.entity_aggregate.entity_repo_adapter import EntityRepoAdapter


class PGEntityRepo(IEntityRepo):
    _entity_table = ENTITY_TABLE
    _child_entity_table = CHILD_ENTITY_TABLE
    _entity_child_entity_table = ENTITY_CHILD_ENTITY_TABLE
    _entity_adapter = EntityRepoAdapter()

    def __init__(self, db_client: Database):
        self._db_client = db_client

    async def get(self, entity_id: pydantic.UUID4) -> Entity:
        pass

    async def where(
        self, page: Optional[int] = None, size: Optional[int] = None
    ) -> EntityList:
        pass

    async def create(self, entity: Entity) -> Entity:
        serialized_entity: Mapping = self._entity_adapter.from_entity(entity)
        serialized_child_entities: List[Mapping] = [
            child_entity.dict() for child_entity in entity.child_entities
        ]
        serialized_entity_child_entities = [
            {
                "entity_child_entity_id": uuid.uuid4(),
                "entity_id": entity.entity_id,
                "child_entity_id": child_entity.child_entity_id,
            }
            for child_entity in entity.child_entities
        ]
        child_entity_insert: Insert = (
            self._child_entity_table.insert()
            .values(serialized_child_entities)
            .returning(*[column for column in self._child_entity_table.columns])
        )
        entity_insert: Insert = (
            self._entity_table.insert()
            .values(serialized_entity)
            .returning(*[column for column in self._entity_table.columns])
        )
        entity_child_entity_insert: Insert = (
            self._entity_child_entity_table.insert()
            .values(serialized_entity_child_entities)
            .returning(*[column for column in self._entity_child_entity_table.columns])
        )
        async with self._db_client.transaction():
            db_entity: Record = await self._db_client.fetch_one(entity_insert)
            # we assume the child entities don't exist yet in a standard create entity flow;
            # child entities only exist in the context of the parent entity
            db_child_entities: List[Record] = await self._db_client.fetch_all(
                child_entity_insert
            )
            _db_entity_child_entities: List[Record] = await self._db_client.fetch_all(
                entity_child_entity_insert
            )
        return self._entity_adapter.to_entity(db_entity, db_child_entities)

    async def create_or_update(self, entity: Entity) -> Entity:
        pass

    async def update(self, entity: Entity) -> Entity:
        pass

    async def delete(self, entity_id: pydantic.UUID4) -> Entity:
        pass
