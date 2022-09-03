from __future__ import annotations

import uuid
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Set, Tuple

import pydantic
from pydantic import Field

from api.domain.utils.pydantic_utils import CreatedAtUpdatedAtBaseModel


class Entity(CreatedAtUpdatedAtBaseModel):
    """Entity is the top-level domain entity for the aggregate root

    A domain entity has a business domain meaning beyond a given service's
    bounded context. It has identity which does not change over time, context,
    or when its attributes change.

    A simple example of a domain entity is a "User" or "Customer" object.
    This entity represents a person, which can change names, addresses, roles,
    or relationships, and it is still the same entity.
    Different contexts will need to use and model different attributes of User/Customer.
    A User domain service may maintain the core view of all User entity attributes,
    while an Order domain service may need just the credit card info and shipping addresses.

    https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
    """

    class Config:  # pylint: disable=missing-class-docstring
        arbitrary_types_allowed = True
        validate_assignment = True

    entity_id: pydantic.UUID4 = Field(default_factory=uuid.uuid4)
    # Tuple gives us a way to have an immutable collection, meaning you cannot update `child_entities`
    # without reassigning to a new Tuple, which triggers the `validate_child_entities_count` validator
    # to enforce valid state regarding the content of `child_entities`.
    # See `validate_child_entities_count` for further info and alternate ways to enforce invariants.
    child_entities: Tuple[ChildEntity, ...]
    bar_value: BarValueObject
    is_active: bool

    @classmethod
    @property
    def MAX_CHILD_ENTITY_COUNT(cls) -> int:  # pylint: disable=invalid-name
        """MAX_CHILD_ENTITY_COUNT is set based on endless user testing which has revealed the
        number of child entity values which create optimal user experience due to reasons.

        This limit is just an example of some arbitrary business rule, which in turn
        means that there is a limitation on valid entity state that must be maintained.
        """
        return 3

    @pydantic.validator("child_entities")
    def validate_child_entities_count(cls, child_entities: Tuple[ChildEntity]):
        """validate_child_entities_count uses Pydantic tooling to enforce valid Entity states

        Domain entities are responsible for "maintaining their invariants", essentially
        meaning to enforcing only valid states.
        Pydantic validators, along with the Config.validate_assignment property are helpful
        for this purpose. Enums are another tool to enforce valid states.
        Non-pydantic classes would use getters and setters to control access to private attributes,
        and keep validation logic in the setters.
        """
        if len(child_entities) > cls.MAX_CHILD_ENTITY_COUNT:
            raise ValueError(
                f"Entity cannot have more than {cls.MAX_CHILD_ENTITY_COUNT} child entities"
            )

        return child_entities


class ChildEntity(pydantic.BaseModel):
    """ChildEntity is an example of a child entity.

    Aggregate roots can contain multiple child entities.
    Child entities must be only be changed through the parent entity's aggregate root
    in order to maintain all invariants and consistency rules of the aggregate root.

    In our data model:
    * each Entity can have multiple ChildEntities
    * each ChildEntity can only belong to one Entity
    This is a one-to-many relationship from the Entity to the Child Entities

    https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model#the-aggregate-root-or-root-entity-pattern
    """

    class Config:
        frozen = True

    child_entity_id: pydantic.UUID4 = Field(default_factory=uuid.uuid4)
    attribute_a: str
    attribute_b: int
    attribute_c: Decimal


class BarValueObject(pydantic.BaseModel):
    """BarValueObject is a value object which can be assigned to an Entity

    A value object is an immutable collection of attributes with no identity.
    Changing the attributes of value objects makes it a different value.

    An example of a value object is an Address.
    An Address can be composed of attributes such as city, state, street, etc.
    Changing any of these attributes makes it a completely different Address.
    Multiple Users or Orders can share an Address without issue.
    This "shared" Address value object can be treated as multiple copies of the same object;
    there is no need for the shared Address object to be a singleton referred to by an id.

    https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/implement-value-objects
    https://stackoverflow.com/questions/1930479/how-to-model-value-object-relationships
    """

    class Config:  # pylint: disable=missing-class-docstring
        frozen = True

    attribute_0: str
    attribute_1: int


class EntityList(pydantic.BaseModel):
    class Config:
        allow_mutation = False

    entities: List[Entity]
    page: int
    size: int


Entity.update_forward_refs()
EntityList.update_forward_refs()
