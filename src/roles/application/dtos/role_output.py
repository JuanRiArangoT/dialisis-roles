from datetime import datetime

from pydantic import BaseModel


class RoleOutputDTO(BaseModel):
    id: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime