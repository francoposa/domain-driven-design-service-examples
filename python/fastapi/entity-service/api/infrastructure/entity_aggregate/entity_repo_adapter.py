from typing import Iterable, Mapping

from databases.backends.postgres import Record

from api.domain.entity_aggregate.entity import ChildEntity, Entity


class EntityRepoAdapter:
    def from_entity(self, entity: Entity) -> Mapping:
        entity_data = entity.dict(exclude={"bar_value", "child_entities"})
        entity_data.update(
            {
                "bar_value_object_attribute_0": entity.bar_value.attribute_0,
                "bar_value_object_attribute_1": entity.bar_value.attribute_1,
            }
        )
        return entity_data

    def to_entity(
        self, entity_data: Record, child_entities_data: Iterable[Record]
    ) -> Entity:
        entity_data_raw = dict(entity_data)
        entity_data_raw.update(
            {
                "bar_value": {
                    "attribute_0": getattr(entity_data, "bar_value_object_attribute_0"),
                    "attribute_1": getattr(entity_data, "bar_value_object_attribute_1"),
                },
                "child_entities": [
                    dict(child_entity_data) for child_entity_data in child_entities_data
                ],
            }
        )
        entity = Entity.parse_obj(entity_data_raw)
        return entity
