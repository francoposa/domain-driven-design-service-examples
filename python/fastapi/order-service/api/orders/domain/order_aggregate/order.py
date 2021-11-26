from __future__ import annotations

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
    items: Tuple[ProductOrderItem, ...]  # tuple for immutability

    @property
    def total(self) -> Decimal:
        return sum([item.total for item in self.items])


class ProductOrderItem:
    class Config:
        frozen = True

    order_id: UUID4
    product_id: UUID4
    quantity: Decimal
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return self.quantity * self.unit_price


Order.update_forward_refs()
