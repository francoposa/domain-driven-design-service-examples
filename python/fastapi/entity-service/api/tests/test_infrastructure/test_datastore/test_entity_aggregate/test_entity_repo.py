from decimal import Decimal

import pytest

from api.domain.entity_aggregate.entity import BarValueObject, ChildEntity, Entity
from api.tests.stubs.entity_aggregate.entity import stub_entities

pytestmark = pytest.mark.asyncio


async def test_create__success(pg_entity_repo):
    # Get baseline
    entity_count = len(stub_entities)

    # Create an entity
    new_entity = entity_0 = Entity(
        bar_value=BarValueObject(
            attribute_0="0",
            attribute_1=1,
        ),
        child_entities=(
            ChildEntity(attribute_a="42", attribute_b=42, attribute_c=Decimal("42.0")),
        ),
        is_active=True,
    )
    created_entity = await pg_entity_repo.create(new_entity)

    # Assert that the entity took the id we generated within the app
    assert created_entity.entity_id == new_entity.entity_id
    #
    # # Assert we have one more user in the repo
    # new_user_count = len(await aiopg_user_repo.where())
    # assert new_user_count == old_user_count + 1
