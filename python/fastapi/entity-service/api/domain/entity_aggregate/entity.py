from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import List, Optional, Set

import pydantic


class Entity(pydantic.BaseModel):
    """Entity is the top-level domain entity for the aggregate root

    A domain entity has a business domain meaning outside of a given service's
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

    entity_id: pydantic.UUID4
    related_entity_id: Optional[pydantic.UUID4]
    foo_value: FooValueObject
    # Set gives us a way to have an immutable collection, meaning you cannot update `bar_values`
    # without reassigning to a new Set, which triggers the `validate_bar_values_count` validator
    # to enforce valid state regarding the content of `bar_values`.
    # See `validate_bar_values_count` for further info and alternate ways to enforce invariants.
    bar_values: Set[BarValueObject]

    @classmethod
    @property
    def MAX_BAR_VALUE_COUNT(cls):  # pylint: disable=invalid-name
        """MAX_B_VALUE_COUNT is set based on endless user testing which has revealed the
        number of bar values which create optimal user experience due to reasons.

        This limit is just an example of some arbitrary business rule, which in turn
        means that there is a limitation on valid entity state that must be maintained.
        """
        return 3

    @pydantic.validator("bar_values")
    def validate_bar_values_count(cls, bar_values: Set[BarValueObject]):
        """validate_bar_values_count uses Pydantic tooling to enforce valid Entity states

        Domain entities are responsible for "maintaining their invariants", essentially
        meaning to enforcing only valid states.
        Pydantic validators, along with the Config.validate_assignment property are helpful
        for this purpose. Enums are another tool to enforce valid states.
        Non-pydantic classes would use getters and setters to control access to private attributes,
        and keep validation logic in the setters.
        """
        if len(bar_values) > cls.MAX_BAR_VALUE_COUNT:
            raise ValueError(f"Entity cannot have more than {cls.MAX_BAR_VALUE_COUNT} bar values")

        return bar_values


class FooValueObject(pydantic.BaseModel):
    """FooValueObject is a value object which can be assigned to an Entity

    A value object is an immutable collection of attributes with no identity.
    Changing the attributes of value objects makes it a different value.

    An example of a value object is an Address.
    An Address can be composed of attributes such as city, state, street, etc.
    Changing any of these attributes makes it a completely different Address.
    Multiple Users or Orders can share an Address without issue.

    https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/implement-value-objects
    """

    class Config:  # pylint: disable=missing-class-docstring
        arbitrary_types_allowed = True
        frozen = True

    attribute_0: str
    attribute_1: int
    attribute_2: Decimal


class BarValueObject(str, Enum):
    """BarValueObject is another example of value object.

    Value objects do not need to be comprised of attributes, they can just be a single value.
    In this example, we use a string enum class to restrict those possible arbitrary values.

    An example of a enumerated single-value value object would be taxonomy or labeling,
    where the user must choose from pre-defined labels or categories.

    https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/implement-value-objects
    """

    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"
    DELTA = "delta"
    EPSILON = "epsilon"


class EntityList(pydantic.BaseModel):
    class Config:
        allow_mutation = False

    entities: List[Entity]
    page: int
    size: int


Entity.update_forward_refs()
EntityList.update_forward_refs()
