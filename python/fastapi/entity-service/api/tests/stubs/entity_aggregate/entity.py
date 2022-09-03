from decimal import Decimal
from uuid import uuid4

from api.domain.entity_aggregate.entity import BarValueObject, ChildEntity, Entity

child_entity_0 = ChildEntity(
    attribute_a="0",
    attribute_b=0,
    attribute_c=Decimal("0.0"),
)

child_entity_1 = ChildEntity(
    attribute_a="1",
    attribute_b=1,
    attribute_c=Decimal("1.0"),
)

child_entity_2 = ChildEntity(
    attribute_a="2",
    attribute_b=2,
    attribute_c=Decimal("2.0"),
)


entity_0 = Entity(
    bar_value=BarValueObject(
        attribute_0="0",
        attribute_1=1,
    ),
    child_entities=(child_entity_0, child_entity_1, child_entity_2),
    is_active=True,
)

stub_entities = [entity_0]
