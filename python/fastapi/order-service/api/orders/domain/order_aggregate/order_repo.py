import uuid
from abc import ABC, abstractmethod
from typing import List

from api.orders.domain.order_aggregate.order import Order


class IOrderRepo(ABC):
    """IOrderRepo defines the interface for Repository implementations providing
    Create-Read-Update-Delete operations for the order domain aggregate root

    Implement this interface to provide CRUD access to resource storage
    where the interface methods are appropriate, such as a REST API,
    relational/document DB, file system, in-memory map/tree, etc.
    """

    @abstractmethod
    def get(self, order_id: uuid.UUID) -> Order:
        pass

    @abstractmethod
    def list(self, page: int = 0, size: int = 0) -> List[Order]:
        pass
