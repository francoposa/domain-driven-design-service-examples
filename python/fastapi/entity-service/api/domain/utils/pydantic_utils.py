import datetime
from typing import Optional

import pydantic

from api.domain.utils.datetime_utils import datetime_now_with_utc_timezone


class CreatedAtUpdatedAtBaseModel(pydantic.BaseModel):

    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    def __init__(self, **data):
        now = datetime_now_with_utc_timezone()
        # field default factory functions are called independently, which results
        # in slightly different timestamps for created_at and updated_at
        # we set these pre-init to allow both to have the same value
        if not data.get("created_at", None):
            data["created_at"] = now
            # if no created_at, assume any presence of updated_at is incorrect
            data["updated_at"] = now
        if not data.get("updated_at", None):
            data["updated_at"] = now

        # handling edits before super.__init__ allow the model to be immutable
        super().__init__(**data)
