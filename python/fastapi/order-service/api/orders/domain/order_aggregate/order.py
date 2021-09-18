from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Tuple

import pydantic
from pydantic import UUID4


class Order(pydantic.BaseModel):
    class Config:
        frozen = True
        arbitrary_types_allowed = True

    order_id: UUID4
    customer_id: UUID4
    items: Tuple[OrderItem, ...]  # tuple for immutability

    @property
    def total(self) -> Decimal:
        return sum([item.total for item in self.items])


class OrderItem(pydantic.BaseModel, ABC):
    class Config:
        frozen = True

    @property
    @abstractmethod
    def total(self) -> Decimal:
        pass


class ProductOrderItem(OrderItem):
    product_id: UUID4
    quantity: Decimal
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return self.quantity * self.unit_price


Order.update_forward_refs()
