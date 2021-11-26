"""Domain-layer errors offer user-facing error messages.

These messages should be informative and helpful to the user, as well as hide implementation
details such as database error messages or anything you would not want a user to know.
"""


class EntityNotFoundError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(self)

    def __str__(self):
        return f"Entity not found for: {self.field}={self.value}"
